
import os, subprocess, textwrap, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
AUTHORIZED_ID = int(os.environ.get("OWNER_ID", "0"))

ALLOWED_CMDS = {
    "deploy": "./scripts/deploy.ps1",
    "status": "./scripts/status.ps1"
}

logging.basicConfig(level=logging.INFO)
app = ApplicationBuilder().token(BOT_TOKEN).build()

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_ID:
        await update.message.reply_text("🔒 Unauthorized")
        return
    if not context.args:
        await update.message.reply_text("Usage: /run <deploy|status>")
        return
    cmd_key = context.args[0]
    script = ALLOWED_CMDS.get(cmd_key)
    if not script:
        await update.message.reply_text("Unknown command")
        return
    await update.message.reply_text(f"⏳ Running {cmd_key} ...")
    proc = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script],
                          capture_output=True, text=True)
    await update.message.reply_text(f"Done ({proc.returncode})\n```{proc.stdout[-1900:]}```",
                                    parse_mode="Markdown")

app.add_handler(CommandHandler("run", run))

if __name__ == "__main__":
    app.run_polling()
