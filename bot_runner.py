import logging
import os
import subprocess
from pathlib import Path

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AUTHORIZED_ID = int(os.environ.get("OWNER_ID", "0"))
REPO_ROOT = Path(__file__).resolve().parent

ALLOWED_CMDS = {
    "status": ["bash", str(REPO_ROOT / "scripts" / "status.sh")],
    "deploy": ["bash", "-lc", f"cd {REPO_ROOT} && git pull --ff-only && git log -1 --oneline"],
    "deploy_safe": ["bash", str(REPO_ROOT / "scripts" / "deploy_safe.sh")],
    "hq_status": ["bash", str(REPO_ROOT / "scripts" / "hq_status.sh")],
    "hq_rebase": ["bash", str(REPO_ROOT / "scripts" / "hq_rebase.sh")],
    "hq_commands": ["bash", str(REPO_ROOT / "scripts" / "hq_commands.sh")],
    # Use repo venv python for stability on VM
    "drive_scan": ["bash", "-lc", f"cd {REPO_ROOT} && ./venv/bin/python scripts/drive_scan.py"],
    "kakao_inventory": ["bash", "-lc", f"cd {REPO_ROOT} && ./venv/bin/python scripts/kakao_inventory.py"],
    "report_inventory": ["bash", "-lc", f"cd {REPO_ROOT} && ./venv/bin/python scripts/report_inventory.py"],
    "report_status": ["bash", "-lc", f"cd {REPO_ROOT} && ./venv/bin/python scripts/report_status.py"],
    "algebra2_status": ["bash", str(REPO_ROOT / "scripts" / "algebra2_status.sh")],
    "algebra2_backup": ["bash", str(REPO_ROOT / "scripts" / "algebra2_backup.sh")],
    "algebra2_diff": ["bash", str(REPO_ROOT / "scripts" / "algebra2_diff.sh")],
    "algebra2_test": ["bash", str(REPO_ROOT / "scripts" / "algebra2_test.sh")],
    "algebra2_clean": ["bash", str(REPO_ROOT / "scripts" / "algebra2_clean.sh")],
    "algebra2_patch_omr": ["bash", str(REPO_ROOT / "scripts" / "algebra2_patch_omr.sh")],
    "algebra2_patch_materials": ["bash", str(REPO_ROOT / "scripts" / "algebra2_patch_materials.sh")],
    "algebra2_patch_omr_layout": ["bash", str(REPO_ROOT / "scripts" / "algebra2_patch_omr_layout.sh")],
    "algebra2_patch_answer_matrix": ["bash", str(REPO_ROOT / "scripts" / "algebra2_patch_answer_matrix.sh")],
    "algebra2_audit_mobile_lang": ["bash", str(REPO_ROOT / "scripts" / "algebra2_audit_mobile_lang.sh")],
    "pc_ping": ["bash", str(REPO_ROOT / "scripts" / "pc_ping.sh")],
    "pc_status": ["bash", str(REPO_ROOT / "scripts" / "pc_status.sh")],
    "pc_bridge_status": ["bash", str(REPO_ROOT / "scripts" / "pc_bridge_status.sh")],
    "ebook_status": ["bash", str(REPO_ROOT / "scripts" / "ebook_status.sh")],
}

ALIASES = {
    "drive": "drive_scan",
    "scan": "drive_scan",
    "kakao": "kakao_inventory",
    "report_inventory": "report_inventory",
    "report_status": "report_status",
    "safe": "deploy_safe",
    "hq": "hq_status",
    "commands": "hq_commands",
    "algebra2": "algebra2_status",
    "a2": "algebra2_status",
    "a2_status": "algebra2_status",
    "a2_backup": "algebra2_backup",
    "a2_diff": "algebra2_diff",
    "a2_test": "algebra2_test",
    "a2_clean": "algebra2_clean",
    "a2_patch_omr": "algebra2_patch_omr",
    "a2_patch_materials": "algebra2_patch_materials",
    "a2_patch_omr_layout": "algebra2_patch_omr_layout",
    "a2_patch_answer_matrix": "algebra2_patch_answer_matrix",
    "a2_audit": "algebra2_audit_mobile_lang",
    # Korean aliases
    "상태": "hq_status",
    "목록": "hq_commands",
    "동기화": "deploy_safe",
    "복구": "hq_rebase",
    "카톡정리": "kakao_inventory",
    "리포트정리": "report_inventory",
    "리포트상태": "report_status",
    "알지상태": "algebra2_status",
    "알지백업": "algebra2_backup",
    "알지확인": "algebra2_diff",
    "알지검사": "algebra2_test",
    "알지정리": "algebra2_clean",
    "정오답패치": "algebra2_patch_answer_matrix",
    "오엠알패치": "algebra2_patch_omr_layout",
    "교재패치": "algebra2_patch_materials",
    "PC핑": "pc_ping",
    "PC상태": "pc_status",
    "PC목록": "pc_bridge_status",
    "PC결과": "pc_bridge_status",
    "피씨핑": "pc_ping",
    "피씨상태": "pc_status",
    "이북상태": "ebook_status",
    "eBook상태": "ebook_status",
    "ebook": "ebook_status",
    "ebook_status": "ebook_status",
}

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")

app = ApplicationBuilder().token(BOT_TOKEN).build()


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_ID:
        await update.message.reply_text("⛔ Unauthorized")
        return

    if not context.args:
        await update.message.reply_text(
            "사용법: /run <status|deploy|deploy_safe|hq_status|hq_rebase|hq_commands|"
            "drive_scan|kakao_inventory|report_inventory|report_status|"
            "algebra2_status|algebra2_backup|algebra2_diff|algebra2_test|algebra2_clean|"
            "algebra2_patch_omr|algebra2_patch_materials|algebra2_patch_omr_layout|"
            "algebra2_patch_answer_matrix|algebra2_audit_mobile_lang>"
        )
        return

    cmd_key = context.args[0].strip().lower()
    cmd_key = ALIASES.get(cmd_key, cmd_key)
    command = ALLOWED_CMDS.get(cmd_key)
    if not command:
        await update.message.reply_text(
            "사용 가능: /run 상태, /run 목록, /run 동기화, /run 복구, "
            "/run drive_scan, /run 카톡정리, /run 리포트정리, /run 리포트상태, "
            "/run 알지백업, /run 알지검사, /run 알지확인, /run 정오답패치, /run 오엠알패치, /run 교재패치"
        )
        return

    await update.message.reply_text(f"⏳ {cmd_key} 실행 중...")
    try:
        proc = subprocess.run(
            command,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=1800,
        )
        output = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
        output = output[-3500:] if output else "no output"
        status = "✅ 완료" if proc.returncode == 0 else "❌ 실패"
        await update.message.reply_text(f"{status} ({proc.returncode})\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⛔ 오류: {e}")


app.add_handler(CommandHandler("run", run))

if __name__ == "__main__":
    app.run_polling()

