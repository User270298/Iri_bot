from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, FSInputFile
from keyboards_iri import get_inline_key, get_calendar, get_start_bot, get_cancel, get_end
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale
from sqlite_db import start_sql, search_bd_id, add_users, \
    delete_users, search_bd_date_time, shedul
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from settings import get_setting
admin_id=get_setting('Input').bots.admin_id
start_sql()

router = Router()
# scheduler=AsyncIOScheduler()
# scheduler.add_job(shedul, 'cron', hour=15, minute=00)
# scheduler.start()



photo = FSInputFile('cizgi-fiyat-katalog-35.jpg')
@router.message(Command(commands=['start']) )
async def get_start(message: Message, state: FSMContext):
    await message.answer(f'Привет {message.from_user.first_name}\n'
                         f'Спасибо, что ты выбрала меня😉')
    await message.answer_photo(photo=photo,
                               reply_markup=get_start_bot())


@router.callback_query(F.data == 'work')
async def my_work(callback: CallbackQuery):
    # await callback.message.answer_photo()
    await callback.message.answer('Пока что нет, но в скором времени появятся')


@router.callback_query(F.data == 'save')
@router.callback_query(F.data=='three')
@router.callback_query(F.data=='other_date')
async def get_start(callback: CallbackQuery):
    await callback.message.answer(f'На какую дату ты бы хотела записаться на выпрямление?',
                                  reply_markup=await get_calendar()
                                  )



@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery,
                                  callback_data: CallbackData,
                                  state: FSMContext
                                  ):
    calendar = SimpleCalendar(locale=await get_user_locale(callback_query.from_user), show_alerts=True)
    calendar.set_dates_range(datetime.now(), datetime(2024, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        global date_time
        date_time = date.strftime("%d.%m.%Y")
        await callback_query.message.answer(
            f'Ваша дата записи {date_time} \n'
            'Выберите время, которое Вам больше подходит',
            reply_markup=get_inline_key()
        )
        await callback_query.answer()


@router.callback_query(F.data == 'one')
async def process_one(callback_query: CallbackQuery):
    for i in search_bd_id(callback_query.from_user.id):
        if str(callback_query.from_user.id) == str(i[0]):
            await callback_query.message.answer(f'У вас уже есть запись', reply_markup=get_cancel())
            await callback_query.answer()
            return
    if search_bd_date_time(date_time, '14:00'):
        await callback_query.message.answer('На эту дату и время уже есть запись \n'
                                            'Запишитесь на другую дату', reply_markup=get_end())
        await callback_query.answer()
        return
    add_users(callback_query.from_user.id, date_time, '14:00')
    await callback_query.message.answer(f'Вы записались на {date_time} в 14:00')

    await callback_query.answer()


@router.callback_query(F.data == 'two')
async def process_one(callback_query: CallbackQuery):
    for i in search_bd_id(callback_query.from_user.id):
        if str(callback_query.from_user.id)==str(i[0]):
            await callback_query.message.answer(f'У вас уже есть запись', reply_markup=get_cancel())
            await callback_query.answer()
            return
    if search_bd_date_time(date_time, '14:00'):
        await callback_query.message.answer('На эту дату и время уже есть запись \n'
                                            'Запишитесь на другую дату', reply_markup=get_end())
        await callback_query.answer()
        return
    add_users(callback_query.from_user.id, date_time, '18:00')
    await callback_query.message.answer(f'Вы записались на {date_time} в 18:00')


@router.message()
async def send_echo(message: Message):
    await message.answer(f'Выберите дату и время😄 \n'
                         f'Если у вас есть вопросы нажмите /help\n'
                         f'Если хотите удалить или перенести запись нажмите'
                         f'/delete\n')




@router.callback_query(F.data == 'cancel')
@router.callback_query(F.data == 'cancel_1')
async def cancel(callback_query: CallbackQuery, state: FSMContext):
    for i in search_bd_id(callback_query.from_user.id):
        if str(callback_query.from_user.id)==str(i[0]):
            delete_users(callback_query.from_user.id)
            await callback_query.message.answer('Ваша запись отменена', reply_markup=get_end())
            await callback_query.answer()
            await state.clear()
            return
    await callback_query.message.answer(f'Вы пока не записались на процедуру)')
    await callback_query.answer()

@router.callback_query(F.data == 'change')
async def return_please(callback_query:CallbackQuery):
    await callback_query.message.answer('Спасибо что выбрала меня🙂\n'
                                        'Если хочешь записаться на процедуру нажми /start')


