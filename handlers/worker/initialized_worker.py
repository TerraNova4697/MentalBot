from aiogram.types import CallbackQuery

from filters import IsWorkerInitialized
from keyboards.inline.worker.worker_callback_data import i_am_worker_button_callback
from loader import dp


@dp.callback_query_handler(i_am_worker_button_callback.filter(action="to_worker_branch"), IsWorkerInitialized())
async def inited_worker(call: CallbackQuery):
    await call.answer(text="Hi, worker! Work harder!")
