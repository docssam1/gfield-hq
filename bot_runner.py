import os
import subprocess
import logging
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AUTHORIZED_ID = int(os.environ.get("OWNER_ID", "0"))
REPO_ROOT = Path(__file__).resolve().parent

ALLOWED_CMDS = {
    "status": ["bash", str(REPO_ROOT / "scripts" / "status.sh")],
    "deploy": ["bash", "-lc", f"cd {REPO_ROOT} && git pull --ff-only && git log -1 --oneline"],
    "algebra2_status": ["bash", str(REPO_ROOT / "scripts" / "algebra2_status.sh")],
    "algebra2_backup": ["bash", str(REPO_ROOT / "scripts" / "algebra2_backup.sh")],
}

ALIASES = {
    "algebra2": "algebra2_status",
    "a2": "algebra2_status",
    "a2_status": "algebra2_status",
    "a2_backup": "algebra2_backup",
}

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")

app = ApplicationBuilder().token(BOT_TOKEN).build()

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_ID:
        await update.message.reply_text("🔒 Unauthorized")
        return

    if not context.args:
        await update.message.reply_text("사용법: /run <status|deploy|algebra2_status|algebra2_backup>")
        return

    cmd_key = context.args[0].lower().strip()
    cmd_key = ALIASES.get(cmd_key, cmd_key)
    command = ALLOWED_CMDS.get(cmd_key)
    if not command:
        await update.message.reply_text("사용 가능: /run status, /run deploy, /run algebra2_status, /run algebra2_backup")
        return

    await update.message.reply_text(f"⏳ {cmd_key} 실행 중...")

    try:
        proc = subprocess.run(
            command,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=180,
        )
        output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        output = output[-3000:] if output else "no output"
        status = "✅ 완료" if proc.returncode == 0 else "❌ 실패"
        await update.message.reply_text(f"{status} ({proc.returncode})\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⛔ 오류: {e}")

app.add_handler(CommandHandler("run", run))

if __name__ == "__main__":
    app.run_polling()
