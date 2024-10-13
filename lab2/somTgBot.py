from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

tasks = []

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я ваш бот Степан.')

async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Доступные команды:\n"
        "/start - Приветствие\n"
        "/help - Список команд\n"
        "/add <задача> - Добавить задачу\n"
        "/delete <номер задачи> - Удалить задачу\n"
        "/list - Показать все задачи"
    )
    await update.message.reply_text(help_text)


async def add_task(update: Update, context: CallbackContext) -> None:
    task_text = ' '.join(context.args)
    if task_text:
        tasks.append(task_text)
        await update.message.reply_text(f'Задача "{task_text}" добавлена.')
    else:
        await update.message.reply_text("Введите задачу после команды /add.")

async def delete_task(update: Update, context: CallbackContext) -> None:
    try:
        task_index = int(context.args[0]) - 1
        if 0 <= task_index < len(tasks):
            deleted_task = tasks.pop(task_index)
            await update.message.reply_text(f'Задача "{deleted_task}" удалена.')
        else:
            await update.message.reply_text("Некорректный номер задачи.")
    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйста, укажите правильный номер задачи после /delete.")

async def list_tasks(update: Update, context: CallbackContext) -> None:
    if tasks:
        task_list = '\n'.join([f"{i + 1}. {task}" for i, task in enumerate(tasks)])
        await update.message.reply_text(f"Ваши задачи:\n{task_list}")
    else:
        await update.message.reply_text("У вас нет задач.")

async def echo_message(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Вы написали: {update.message.text}')

def main():
    application = Application.builder().token("YOUR_TOKEN_HERE").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("delete", delete_task))
    application.add_handler(CommandHandler("list", list_tasks))


    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    application.run_polling()

if __name__ == '__main__':
    main()