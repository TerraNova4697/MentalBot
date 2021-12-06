from aiogram.types import CallbackQuery

from filters import IsWorkerInitialized
from keyboards.default.workers_main_keyboard import workers_main_keyboard
from keyboards.inline.worker.worker_callback_data import i_am_worker_button_callback
from loader import dp, bot


@dp.callback_query_handler(i_am_worker_button_callback.filter(action="to_worker_branch"), IsWorkerInitialized())
async def inited_worker(call: CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Вы можете выбрать следующее:",
                           reply_markup=workers_main_keyboard)
