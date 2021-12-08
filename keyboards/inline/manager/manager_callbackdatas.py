from aiogram.utils.callback_data import CallbackData

cancel_name_input = CallbackData("cancel_button", "action")
delete_worker_callback = CallbackData("delete_worker", "action", "user_id")
cancel_button_choose_worker_to_delete = CallbackData("c_choose", "action")

confirm_deleting_worker_callback = CallbackData("confirm", "action", "user_id")
navigate_back_callback = CallbackData("navigate", "action")

choose_worker_for_answers_id = CallbackData("choose", "action", "user_id")
choose_month_callback = CallbackData("chosen_m", "action", "month", "year", "user_id")

choose_test_callback = CallbackData("chosen_d", "action", "answers_id")

