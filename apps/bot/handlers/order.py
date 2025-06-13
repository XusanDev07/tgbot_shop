from asgiref.sync import sync_to_async
from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from apps.orders.models import Basket, Order, OrderItem
from apps.users.models import User
from apps.bot.utils.translations import get_translation

router = Router()


class OrderForm(StatesGroup):
    full_name = State()
    phone_number = State()
    address = State()


@router.message(lambda msg: msg.text in [get_translation('orders', 'uz'), get_translation('orders', 'ru')])
async def start_order(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    data = await state.get_data()
    language = data.get("language", "uz")

    user = await sync_to_async(User.objects.filter(telegram_id=tg_id).first)()
    basket = await sync_to_async(lambda: list(Basket.objects.select_related("user", "color").filter(user=user)))()

    if not basket:
        await message.answer(get_translation("basket_isnull", language))
        return

    await message.answer(get_translation("enter_full_name", language))
    await state.set_state(OrderForm.full_name)


@router.message(OrderForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    await state.update_data(full_name=message.text)
    await message.answer(get_translation("enter_phone_number", language))
    await state.set_state(OrderForm.phone_number)


@router.message(OrderForm.phone_number)
async def process_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    await state.update_data(phone_number=message.text)
    await message.answer(get_translation("enter_address", language))
    await state.set_state(OrderForm.address)


@router.message(OrderForm.address)
async def process_address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "uz")

    tg_id = message.from_user.id
    user = await sync_to_async(User.objects.get)(telegram_id=tg_id)
    basket_items = await sync_to_async(
        lambda: list(Basket.objects.select_related("user", "color").filter(user=user)))()

    order = await sync_to_async(Order.objects.create)(
        user=user,
        full_name=data["full_name"],
        phone_number=data["phone_number"],
        address=message.text,
        is_finished=False,
        status='pending'
    )

    for item in basket_items:
        product = await sync_to_async(lambda: item.color.product)()
        await sync_to_async(OrderItem.objects.create)(
            order=order,
            product=product,
            color=item.color,
            quantity=item.quantity,
            price=item.color.price
        )

    await sync_to_async(lambda: Basket.objects.filter(user=user).delete())()

    await message.answer(get_translation("order_accepted", language))
    await state.clear()
