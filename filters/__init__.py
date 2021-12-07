from aiogram import Dispatcher

from loader import dp
# from .is_admin import AdminFilter

from .uninitialized_worker import IsWorkerInitialized
from .is_owner import IsOwner, IsOwnerCall
from .is_not_owner import IsNotOwner


if __name__ == "filters":
    dp.filters_factory.bind(IsWorkerInitialized)
    dp.filters_factory.bind(IsOwner)
    dp.filters_factory.bind(IsOwnerCall)
    dp.filters_factory.bind(IsNotOwner)
    pass
