from aiogram.utils.callback_data import CallbackData

confirm_new_manager_callback = CallbackData("confirm", "action", "user_id")
decline_new_manager_callback = CallbackData("decline", "action", "user_id")

choose_manager_callback = CallbackData("choose_m", "action", "user_id")
choose_manager_cancel_callback = CallbackData("choose_m", "action")

confirm_manager_deleting_callback = CallbackData("confirm_del", "action", "user_id")
cancel_manager_deleting_callback = CallbackData("cancel_del", "action")
