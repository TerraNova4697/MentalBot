from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsOwner, IsManager, IsOwnerCall, IsManagerCall
from keyboards.inline.manager.choose_month_keyboard import create_choose_worker_keyboard, create_choose_month_keyboard, \
    create_choose_test_keyboard, calculate_points, create_navigation_keyboard
from keyboards.inline.manager.manager_callbackdatas import navigate_back_callback, choose_worker_for_answers_id, \
    choose_month_callback, choose_test_callback
from keyboards.inline.manager.navigate_back_button import navigate_back_button
from loader import dp, bot, db
from states.show_answers import ShowAnswers


@dp.message_handler(IsOwner(), text="Посмотреть ответы опросников")
@dp.message_handler(IsManager(), text="Посмотреть ответы опросников")
async def show_answers(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Введите фамилию сотрудника для просмотра его ответов",
                           reply_markup=navigate_back_button)
    await ShowAnswers.NameInput.set()


@dp.callback_query_handler(navigate_back_callback.filter(action="back"), IsOwnerCall(), state=ShowAnswers.NameInput)
@dp.callback_query_handler(navigate_back_callback.filter(action="back"), IsManagerCall(), state=ShowAnswers.NameInput)
async def input_name_back(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(IsOwner(), state=ShowAnswers.NameInput)
@dp.message_handler(IsManager(), state=ShowAnswers.NameInput)
async def find_worker(message: types.Message, state: FSMContext):
    try:
        workers = db.select_all_workers_by_name(name=message.text, status="Active")
        if len(workers) == 0:
            await bot.send_message(text="Я никого не нашел по Вашему запросу, попробуйте еще раз",
                                   chat_id=message.chat.id, reply_markup=navigate_back_button)
        else:
            await bot.send_message(chat_id=message.chat.id, text="Выберите сотрудника",
                                   reply_markup=create_choose_worker_keyboard(workers))
            await state.update_data({"name": message.text})
            await ShowAnswers.ChooseWorker.set()
            # await bot.send_message(chat_id=message.chat.id, text="Выберите месяц",
            #                        reply_markup=create_choose_month_keyboard(workers[0]))
    except Exception as err:
        print(err)


@dp.callback_query_handler(navigate_back_callback.filter(action="cancel"), IsOwnerCall(), state=ShowAnswers.ChooseWorker)
@dp.callback_query_handler(navigate_back_callback.filter(action="cancel"), IsManagerCall(),
                           state=ShowAnswers.ChooseWorker)
async def choose_worker(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(choose_worker_for_answers_id.filter(action="show_answers"), IsOwnerCall(),
                           state=ShowAnswers.ChooseWorker)
@dp.callback_query_handler(choose_worker_for_answers_id.filter(action="show_answers"), IsManagerCall(),
                           state=ShowAnswers.ChooseWorker)
async def choose_month(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    worker_id = callback_data.get("user_id")
    try:
        answers = db.select_all_answers_by_user_id(user_id=int(worker_id))
        if len(answers) == 0:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.message.chat.id, text="Данный пользователь еще не проходил опрос")
            await state.finish()
        else:
            await bot.edit_message_text(text="Выберите месяц", chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=create_choose_month_keyboard(answers))
            await ShowAnswers.ChooseMonth.set()
    except Exception as er:
        print(er)


@dp.callback_query_handler(navigate_back_callback.filter(action="cancel"), IsOwnerCall(), state=ShowAnswers.ChooseMonth)
@dp.callback_query_handler(navigate_back_callback.filter(action="cancel"), IsManagerCall(),
                           state=ShowAnswers.ChooseMonth)
async def choose_worker(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(navigate_back_callback.filter(action="back"), IsOwnerCall(), state=ShowAnswers.ChooseMonth)
@dp.callback_query_handler(navigate_back_callback.filter(action="back"), IsManagerCall(),
                           state=ShowAnswers.ChooseMonth)
async def choose_worker(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    name = data.get("name")
    workers = db.select_all_workers_by_name(name=name, status="Active")
    await bot.edit_message_text(chat_id=call.message.chat.id, text="Выберите сотрудника",
                                message_id=call.message.message_id,
                                reply_markup=create_choose_worker_keyboard(workers))
    await ShowAnswers.ChooseWorker.set()


@dp.callback_query_handler(choose_month_callback.filter(action="chosen_m"), IsOwnerCall(),
                           state=ShowAnswers.ChooseMonth)
@dp.callback_query_handler(choose_month_callback.filter(action="chosen_m"), IsManagerCall(),
                           state=ShowAnswers.ChooseMonth)
async def choose_test(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    month = callback_data.get("month")
    year = callback_data.get("year")
    user_id = callback_data.get("user_id")
    await state.update_data({"month": month})
    await state.update_data({"year": year})
    await state.update_data({"user_id": user_id})
    answers = db.select_all_answers_by_user_id(user_id=int(user_id), month=int(month), year=int(year))
    await bot.edit_message_text(text="Выберите опрос", chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=create_choose_test_keyboard(answers))
    await ShowAnswers.Answers.set()


@dp.callback_query_handler(navigate_back_callback.filter(action="cancel"), IsOwnerCall(), state=ShowAnswers.Answers)
@dp.callback_query_handler(navigate_back_callback.filter(action="cancel"), IsManagerCall(),
                           state=ShowAnswers.Answers)
async def choose_worker(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(navigate_back_callback.filter(action="back"), IsOwnerCall(), state=ShowAnswers.Answers)
@dp.callback_query_handler(navigate_back_callback.filter(action="back"), IsManagerCall(),
                           state=ShowAnswers.Answers)
async def choose_worker(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    worker_id = data.get("user_id")
    try:
        answers = db.select_all_answers_by_user_id(user_id=int(worker_id))
        await bot.edit_message_text(text="Выберите месяц", chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    reply_markup=create_choose_month_keyboard(answers))
        await ShowAnswers.ChooseMonth.set()
    except Exception as err:
        print(err)


@dp.callback_query_handler(choose_test_callback.filter(action="show_test"), IsOwnerCall(),
                           state=ShowAnswers.Answers)
@dp.callback_query_handler(choose_test_callback.filter(action="show_test"), IsManagerCall(),
                           state=ShowAnswers.Answers)
async def show_answers(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    answers_id = callback_data.get("answers_id")
    data = await state.get_data()
    user_id = data.get("user_id")
    worker = db.select_all_workers_by_name(user_id=int(user_id))
    name = f"{worker[0][1]} {worker[0][2]}"
    answer = db.select_all_answers_by_user_id(answers_id=answers_id)
    print(answer)
    native_date = answer[0][8]
    date = f"{native_date[-2:]}.{native_date[-5:-3]}.{native_date[0:4]}"
    answer1 = answer[0][2]
    answer2 = answer[0][3]
    answer3 = answer[0][4]
    answer4 = answer[0][5]
    answer5 = answer[0][6]
    answer6 = answer[0][7]
    average = calculate_points(answer1, answer2, answer3, answer4, answer6)
    text = f"Опрос от {date} сотрудника {name}:\n\n" \
           f"1. Оцените ваше настроение сегодня - {str(answer1)}\n" \
           f"2. Чувствуете ли вы приятную усталость от работы? - {str(answer2)}\n" \
           f"3. Насколько вы энергичны прямо сейчас? - {str(answer3)}\n" \
           f"4. Как вы оцениваете вашу продуктивность сегодня? - {str(answer4)}\n" \
           f"5. Если бы у вас появился сейчас час свободного времени, что бы вы сделали в первую очередь?\n" \
           f"-{answer5}\n" \
           f"6. Чувствовали ли вы заинтересованность и поддержку со стороны ваших коллег? - {str(answer6)}\n\n" \
           f"Средний балл: {str(average)}/5.0"
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text, reply_markup=create_navigation_keyboard())
    await ShowAnswers.Final.set()


@dp.callback_query_handler(navigate_back_callback.filter(action="cancel"), IsOwnerCall(), state=ShowAnswers.Final)
@dp.callback_query_handler(navigate_back_callback.filter(action="cancel"), IsManagerCall(),
                           state=ShowAnswers.Final)
async def cancel(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(navigate_back_callback.filter(action="back"), IsOwnerCall(), state=ShowAnswers.Final)
@dp.callback_query_handler(navigate_back_callback.filter(action="back"), IsManagerCall(),
                           state=ShowAnswers.Final)
async def navigate_back(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    month = data.get("month")
    year = data.get("year")
    user_id = data.get("user_id")
    answers = db.select_all_answers_by_user_id(user_id=int(user_id), month=int(month), year=int(year))
    await bot.edit_message_text(text="Выберите опрос", chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=create_choose_test_keyboard(answers))
    await ShowAnswers.Answers.set()


@dp.callback_query_handler(navigate_back_callback.filter(action="back2"), IsOwnerCall(), state=ShowAnswers.Final)
@dp.callback_query_handler(navigate_back_callback.filter(action="back2"), IsManagerCall(),
                           state=ShowAnswers.Final)
async def navigate_back2(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    name = data.get("name")
    workers = db.select_all_workers_by_name(name=name, status="Active")
    await bot.edit_message_text(chat_id=call.message.chat.id, text="Выберите сотрудника",
                                message_id=call.message.message_id,
                                reply_markup=create_choose_worker_keyboard(workers))
    await ShowAnswers.ChooseWorker.set()

