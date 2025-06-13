from asgiref.sync import sync_to_async
from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F
from apps.bot.utils.translations import get_translation
from apps.users.models import User

router = Router()


class RegisterState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()


@sync_to_async
def user_exists(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).exists()


@router.message(F.text == "/start")
async def start(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    if not await user_exists(message.from_user.id):
        await message.answer(get_translation("welcome", language))
        await state.set_state(RegisterState.waiting_for_name)
    else:
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text=get_translation("categories", language))],
                [types.KeyboardButton(text=get_translation("basket", language)),
                 types.KeyboardButton(text=get_translation("orders", language))],
                [types.KeyboardButton(text=get_translation("choose_language", language))],
            ],
            resize_keyboard=True
        )
        await message.answer(get_translation("welcome", language), reply_markup=keyboard)


@router.message(RegisterState.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    await state.update_data(full_name=message.text)
    await message.answer(
        get_translation("enter_phone_number", language),
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text=get_translation("send_phone", language), request_contact=True)]],
            resize_keyboard=True
        )
    )
    await state.set_state(RegisterState.waiting_for_phone)


@router.message(RegisterState.waiting_for_phone, F.contact)
async def get_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    if not message.contact:
        await message.answer(get_translation("send_phone_error", language))
        return

    phone_number = message.contact.phone_number
    full_name = data.get("full_name", "")

    await sync_to_async(User.objects.create)(
        telegram_id=message.from_user.id,
        phone_number=phone_number,
        full_name=full_name,
    )

    await message.answer(get_translation("registration_success", language), reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=get_translation("categories", language))],
            [types.KeyboardButton(text=get_translation("basket", language)),
             types.KeyboardButton(text=get_translation("orders", language))],
            [types.KeyboardButton(text=get_translation("choose_language", language))],
        ],
        resize_keyboard=True
    )
    await message.answer(get_translation("welcome", language), reply_markup=keyboard)
