from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar,SimpleCalendarCallback
from datetime import datetime
router=Router()

@router.message()
def get_inline_key():
    build=InlineKeyboardBuilder()
    build.button(text='14:00-18:00',callback_data='one')
    build.button(text='18:00-22:00',callback_data='two')
    build.button(text='Изменить дату записи', callback_data='three')
    build.adjust(2, 1)
    return build.as_markup()

@router.message()
def get_start_bot():
    build=InlineKeyboardBuilder()
    build.button(text='Посмотреть мои работы', callback_data='work',)
    build.button(text='Записаться на выпрямление', callback_data='save')
    build.button(text='Отменить запись', callback_data='cancel')
    build.adjust(1,1,1)
    return build.as_markup()

@router.message()
def get_calendar():
    calendar=SimpleCalendar()
    return calendar.start_calendar()

@router.message()
def get_cancel():
    build = InlineKeyboardBuilder()
    build.button(text='Отменить запись', callback_data='cancel_1')
    build.adjust(1)
    return build.as_markup()

@router.message()
def get_end():
    build = InlineKeyboardBuilder()
    build.button(text='Записаться на другую дату', callback_data='other_date')
    build.button(text='Пока не хочу делать эту процедуру', callback_data='change')
    build.adjust(1,1)
    return build.as_markup()


