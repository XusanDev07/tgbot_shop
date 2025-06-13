from asgiref.sync import sync_to_async

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.router import Router
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from apps.shop.models import Category
from apps.bot.utils.translations import translations, get_translation

router = Router()


@router.message(
    lambda msg: msg.text == translations['uz']['categories'] or msg.text == translations['ru']['categories'])
async def show_categories(message: types.Message, state: FSMContext):
    root_categories = await sync_to_async(list)(Category.objects.filter(parent__isnull=True))
    data = await state.get_data()
    language = data.get("language", "uz")

    keyboard = [
        [InlineKeyboardButton(text=getattr(cat, f"name_{language}"), callback_data=f"catroot_{cat.id}")]
        for cat in root_categories
    ]

    await message.answer(get_translation('categories', language),
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


@router.callback_query(lambda call: call.data.startswith("catroot_"))
async def show_subcategories(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cat_id = int(call.data.split("_")[1])

    subcategories = await sync_to_async(list)(Category.objects.filter(parent_id=cat_id))
    language = data.get("language", "uz")

    if subcategories:
        keyboard = [
            [InlineKeyboardButton(text=getattr(sub, f"name_{language}"), callback_data=f"catsub_{sub.id}")]
            for sub in subcategories
        ]
        await call.message.edit_text(get_translation('subcategories', language),
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        else:
        # Ichki kategoriya yo‘q bo‘lsa, mahsulot ko‘rsatish uchun yuboramiz
        await call.message.edit_text(get_translation('already_exist', language))
        await show_products(call, cat_id=cat_id)
