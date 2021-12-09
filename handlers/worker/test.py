from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.manager.choose_month_keyboard import calculate_points
from keyboards.inline.worker.test import q1, q2, q3, q4, q6
from keyboards.inline.worker.worker_callback_data import q1_callback, q2_callback, q3_callback, q4_callback, \
    q5_callback, q6_callback
from loader import dp, bot, db
from states.test import Test
from datetime import date

from utils.google_sheets import update_statistics


def calculate_average(a, b, c, d, e):
    return str((a+b+c+d+e)/5)


def check_status(a, b, c, d, e):
    if a + b + c + d + e > 20:
        return "Мы рады, что вы чувствуете себя прекрасно! " \
               "У вас точно нет никаких препятствий на пути к блестящим результатам в работе!"
    elif a + b + c + d + e > 15:
        return "Ваше хорошее настроение радует нас! Надеемся оно будет только улучшаться. " \
               "Подумайте, что ещё Вы можете сделать, чтобы пребывать в отличном расположении духа?"
    elif a + b + c + d + e > 10:
        return "Ваше состояние удовлетворительно." \
               " Рекомендуем вам попробовать другие функции нашего бота, чтобы вовремя исправить его в лучшую сторону."
    elif a + b + c + d + e > 5:
        return "Вы часто чувствуете себя раздраженным и уставшим? \n" \
               "Задумайтесь, возможно, вы испытываете слишком много стресса. " \
               "Вам стоит больше отдыхать. Старайтесь делать перерывы в течение рабочего дня."
    else:
        return "Ваши результаты неутешительны. " \
               "Настоятельно рекомендуем обсудить ваши рабочие условия с руководителем." \
               " Если вас что-то не устраивает или мешает работать, то самое время решить этот вопрос," \
               " чтобы начать чувствовать себя лучше."


@dp.message_handler(text="Пройти опрос")
async def begin_test(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Оцените ваше настроение сегодня (1,2,3,4,5)",
                           reply_markup=q1)
    await Test.Q1.set()


@dp.callback_query_handler(q1_callback.filter(question="one"), state=Test.Q1)
async def question_two(call: CallbackQuery, callback_data: dict, state: FSMContext):
    answer = callback_data.get("answer")
    await state.update_data(
        {
            "mood": int(answer)
        }
    )
    await bot.edit_message_text(text="Чувствуете ли вы приятную усталость от работы?  (1,2,3,4,5)",
                                chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=q2)
    await Test.Q2.set()


@dp.callback_query_handler(q2_callback.filter(question="two"), state=Test.Q2)
async def question_three(call: CallbackQuery, callback_data: dict, state: FSMContext):
    answer = callback_data.get("answer")
    await state.update_data(
        {
            "tired": int(answer)
        }
    )
    await bot.edit_message_text(text="Насколько вы энергичны прямо сейчас? (1,2,3,4,5)",
                                chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=q3)
    await Test.Q3.set()


@dp.callback_query_handler(q3_callback.filter(question="three"), state=Test.Q3)
async def question_four(call: CallbackQuery, callback_data: dict, state: FSMContext):
    answer = callback_data.get("answer")
    await state.update_data(
        {
            "energy": int(answer)
        }
    )
    await bot.edit_message_text(text="Как вы оцениваете вашу продуктивность сегодня? (1,2,3,4,5)",
                                chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=q4)
    await Test.Q4.set()


@dp.callback_query_handler(q4_callback.filter(question="four"), state=Test.Q4)
async def question_five(call: CallbackQuery, callback_data: dict, state: FSMContext):
    answer = callback_data.get("answer")
    await state.update_data(
        {
            "productivity": int(answer)
        }
    )
    sent_message = await bot.edit_message_text(
        text="Если бы у вас появился сейчас час свободного времени, что бы вы сделали в первую "
             "очередь? (здесь развёрнутый ответ)",
        chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.update_data(
        {
            "message_id": sent_message.message_id
        }
    )
    await Test.Q5.set()


@dp.message_handler(state=Test.Q5)
async def question_six(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(
        {
            "one_hour": answer
        }
    )
    data = await state.get_data()
    message_id = data.get("message_id")
    await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
    await bot.edit_message_text(text="Чувствовали ли вы заинтересованность и поддержку со стороны ваших коллег?"
                                     " (1,2,3,4,5)", chat_id=message.chat.id, message_id=message_id,
                                reply_markup=q6)
    await Test.Q6.set()


@dp.callback_query_handler(q6_callback.filter(question="six"), state=Test.Q6)
async def finish_test(call: CallbackQuery, callback_data: dict, state: FSMContext):
    colleagues = int(callback_data.get("answer"))
    data = await state.get_data()
    mood = data.get("mood")
    tired = data.get("tired")
    energy = data.get("energy")
    productivity = data.get("productivity")
    one_hour = data.get("one_hour")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    result = check_status(float(mood), float(tired), float(energy), float(productivity), float(colleagues))
    avr: str = calculate_points(mood, tired, energy, productivity, colleagues)
    await bot.send_message(chat_id=call.message.chat.id, text=result)
    await state.finish()
    curr_date = date.today()
    month = curr_date.month
    year = curr_date.year
    print(avr)
    print(type(year))
    db.add_answer(user_id=call.message.chat.id, mood=mood, tired=tired, energy=energy, productivity=productivity,
                  one_hour=one_hour, colleagues=colleagues, average=avr, date=str(curr_date), month=month, year=year)
    answers = db.select_all_answers_by_user_id(month=int(month), year=int(year))
    update_statistics(answers, month, year)
