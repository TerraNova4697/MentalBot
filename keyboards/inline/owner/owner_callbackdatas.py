from aiogram.utils.callback_data import CallbackData

confirm_new_manager_callback = CallbackData("confirm", "action", "user_id")
decline_new_manager_callback = CallbackData("decline", "action", "user_id")
