from asgiref.sync import sync_to_async
from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from aiogram.fsm.context import FSMContext
from apps.shop.models import Product, ProductColor
from apps.bot.utils.translations import get_translation

router = Router()


@router.callback_query(lambda call: call.data.startswith("catsub_"))
async def show_products(call: types.CallbackQuery, state: FSMContext, cat_id: int = None):
    if cat_id is None:
        cat_id = int(call.data.split("_")[1])

    data = await state.get_data()
    language = data.get("language", "uz")

    products = await sync_to_async(list)(Product.objects.filter(categories__id=cat_id))

    if not products:
        await call.message.answer(get_translation("no_products", language))
        return

    for product in products:
        text = f"📦 {getattr(product, f'name_{language}')}"
        photo_url = "https://3c48-94-232-25-59.ngrok-free.app/" + product.main_image.url
        btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=get_translation("view", language), callback_data=f"prod_{product.id}")]]
        )
        await call.message.answer_photo(photo=photo_url, caption=text, reply_markup=btn)


@router.callback_query(lambda c: c.data.startswith("prod_"))
async def show_product_detail(call: types.CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[1])

    data = await state.get_data()
    language = data.get("language", "uz")

    product = await sync_to_async(
        lambda: Product.objects.prefetch_related('colors__images').get(id=product_id)
    )()

    caption = f"📦 {getattr(product, f'name_{language}')}\n\n{get_translation('choose_color', language)}"
    buttons = []

    for color in product.colors.all():
        buttons.append(
            [InlineKeyboardButton(text=f"{color.name} - {color.price} {get_translation('currency', language)}",
                                  callback_data=f"color_{color.id}")]
        )
    photo_url = "https://3c48-94-232-25-59.ngrok-free.app" + product.main_image.url
    await call.message.answer_photo(
        photo=photo_url,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@router.callback_query(lambda c: c.data.startswith("color_"))
async def color_selected(call: types.CallbackQuery, state: FSMContext):
    color_id = int(call.data.split("_")[1])

    data = await state.get_data()
    language = data.get("language", "uz")

    color = await sync_to_async(ProductColor.objects.get)(id=color_id)

    caption = (
        f"🖍 {get_translation('color', language)}: {color.name}\n"
        f"💰 {get_translation('price', language)}: {color.price} {get_translation('currency', language)}\n\n"
        f"{get_translation('add_to_basket', language)}"
    )

    btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_translation("add_to_basket_btn", language),
                              callback_data=f"addbasket_{color.id}")]
    ])

    img = await sync_to_async(lambda: color.images.first())()
    photo_url = "https://3c48-94-232-25-59.ngrok-free.app" + img.image.url if img else None
    if img:
        await call.message.answer_photo(
            photo=photo_url,
            caption=caption,
            reply_markup=btn
        )
    else:
        await call.message.answer(caption, reply_markup=btn)
