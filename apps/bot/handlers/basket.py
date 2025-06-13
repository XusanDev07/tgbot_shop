from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apps.orders.models import Basket
from apps.users.models import User
from apps.shop.models import ProductColor
from asgiref.sync import sync_to_async
from apps.bot.utils.translations import get_translation

router = Router()


@sync_to_async
def get_user_by_tg_id(tg_id):
    return User.objects.filter(telegram_id=tg_id).first()


@sync_to_async
def get_color_by_id(color_id):
    return ProductColor.objects.filter(id=color_id).first()


@sync_to_async
def get_basket_item(user, color):
    return Basket.objects.filter(user=user, color=color).first()


@sync_to_async
def create_basket(user, color):
    return Basket.objects.create(user=user, color=color, quantity=1)


@sync_to_async
def get_user_basket(user):
    return list(Basket.objects.select_related("color", "color__product").filter(user=user))


@sync_to_async
def delete_basket_item(item):
    item.delete()


@router.message(lambda msg: msg.text in [get_translation('basket', 'uz'), get_translation('basket', 'ru')])
async def show_basket(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    data = await state.get_data()
    language = data.get("language", "uz")

    if not user:
        await message.answer(get_translation('unautarization', language))
        return

    basket_items = await get_user_basket(user)

    if not basket_items:
        await message.answer(get_translation('basket_isnull', language))
        return

    total = 0
    for item in basket_items:
        color = item.color
        product = color.product
        item_text = (
            f"📦 {getattr(product, f'name_{language}')} ({color.name})\n"
            f"📌 {item.quantity} x {color.price} = {item.quantity * color.price} so'm"
        )
        total += item.quantity * color.price

        builder = InlineKeyboardBuilder()
        builder.button(text=get_translation("delete", language), callback_data=f"delete_{item.id}")
        builder.adjust(1)

        await message.answer(item_text, reply_markup=builder.as_markup())

    await message.answer(f"{get_translation('total', language)}: {total} so'm")


@router.callback_query(F.data.startswith("delete_"))
async def delete_from_basket(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    item_id = int(call.data.split("_")[1])
    tg_id = call.from_user.id
    user = await sync_to_async(User.objects.filter(telegram_id=tg_id).first)()

    item = await sync_to_async(Basket.objects.filter(id=item_id, user=user).first)()
    if item:
        await sync_to_async(item.delete)()
        await call.message.edit_text(get_translation("item_deleted", language))
    else:
        await call.message.answer(get_translation("item_not_found", language))


@router.callback_query(lambda c: c.data.startswith("addbasket_"))
async def add_to_basket(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    tg_id = call.from_user.id
    color_id = int(call.data.split("_")[1])

    user = await get_user_by_tg_id(tg_id)
    color = await get_color_by_id(color_id)

    if not user:
        await call.message.answer(get_translation("unautarization", language))
        return

    if not color:
        await call.message.answer(get_translation("item_not_found", language))
        return

    basket_item = await get_basket_item(user, color)

    if basket_item:
        basket_item.quantity += 1
        await sync_to_async(basket_item.save)()
    else:
        await create_basket(user, color)

    await call.answer(get_translation("item_added", language), show_alert=False)
