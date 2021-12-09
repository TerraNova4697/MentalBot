from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.variables import workers, managers, accessed_emails


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Создаем таблицы
    try:
        db.create_table_workers()
    except Exception as err:
        print(err)
    try:
        db.create_table_answers()
    except Exception as err:
        print(err)
    try:
        db.create_table_managers()
    except Exception as err:
        print(err)

    # Загружаем из Таблиц данные
    # Загружаем список айдишников работников
    list_of_workers = db.select_all_workers_user_id(status="Active")
    for user_id in list_of_workers:
        workers.append(user_id[0])
    # Загружаем список айдишников менеджеров
    list_of_managers = db.select_all_managers_user_id(status="Active")
    for user_id in list_of_managers:
        managers.append(user_id[0])
        if len(user_id[1]) > 0:
            accessed_emails.append(user_id[0])
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

