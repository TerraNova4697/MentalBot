from aiogram.utils.callback_data import CallbackData

cancel_name_input = CallbackData("cancel_button", "action")
delete_worker_callback = CallbackData("delete_worker", "action", "user_id")
cancel_button_choose_worker_to_delete = CallbackData("c_choose", "action")

confirm_deleting_worker_callback = CallbackData("confirm", "action", "user_id")

