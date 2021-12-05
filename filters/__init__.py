from aiogram import Dispatcher

from loader import dp
# from .is_admin import AdminFilter

from .uninitialized_worker import IsWorkerInitialized


if __name__ == "filters":
    dp.filters_factory.bind(IsWorkerInitialized)
    pass
