from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from apps.bot.utils.translations import get_translation

router = Router()


@router.message(lambda msg: msg.text == "🌐 Tilni tanlash")
async def choose_language(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🇺🇿 O'zbekcha"), types.KeyboardButton(text="🇷🇺 Русский")],
        ],
        resize_keyboard=True
    )
    await message.answer("Tilni tanlang:", reply_markup=keyboard)


@router.message(lambda msg: msg.text in ["🇺🇿 O'zbekcha", "🇷🇺 Русский"])
async def set_language(message: types.Message, state: FSMContext):
    language = "uz" if message.text == "🇺🇿 O'zbekcha" else "ru"
    await state.update_data(language=language)
    await message.answer(get_translation("language_set", language), reply_markup=types.ReplyKeyboardRemove())
