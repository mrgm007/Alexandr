from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.storage import FSMContext
from .state import add_state, get_staff_state
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from kayboard.inlyne_menu import cansel_menu
from dispatcher import dp, db, bot
from aiogram.types import CallbackQuery



@dp.callback_query_handler(text=["acc_fb_one", "acc_fb_two", "acc_fb_three", "acc_fb_four"])
async def select_delete_button(call: CallbackQuery):
    category = call.data
    rows = await db.select_buttons(category)
    for row in rows:
        row = row.get("buttons")
        await call.message.answer(text=row, reply_markup=InlineKeyboardMarkup(). \
                             add(InlineKeyboardButton(f"Удалить кнопку", callback_data=f"del_button{row}")))






@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_button'))
async def delete_button(call: CallbackQuery):
    button_name = call.data.replace('del_button', "")
    row = await db.get_staff_in_db(button_name=button_name)
    if row is None:
        await db.delete_buttons(buttons=button_name)
        await call.answer('Кнопка удалена')
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
    else:
        await call.message.answer("В этой кнопке ещё остался товар, заберите его, потом уже удалите кнопку.")



@dp.callback_query_handler(state="*", text='cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Отменено")
    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_users'))
async def delete_button(call: CallbackQuery):
    user_id = call.data.replace('del_users', "")
    user_id = int(user_id)
    await db.delete_user(user_id=user_id)
    await call.answer('Пользователь удалён')
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('register_user'))
async def add_status_user(call: CallbackQuery):
    status = "User"
    user_id = call.data.replace('register_user', "")
    user_id = int(user_id)
    await db.add_status_for_user(user_id=user_id, status=status)
    await call.answer('Пользователь зарегистрирован')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('register_admin'))
async def add_status_admin(call: CallbackQuery):
    status = "Admin"
    user_id = call.data.replace('register_admin', "")
    user_id = int(user_id)
    await db.add_status_for_user(user_id=user_id, status=status)
    await call.answer('Пользователь добавлен админом')


@dp.callback_query_handler(text=["add_staff_acc_fb_one", "add_staff_acc_fb_two", "add_staff_acc_fb_three", "add_staff_acc_fb_four"])
async def add_staff_in_btn(call: CallbackQuery):
    user_id = call.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        category = ""
        if call.data == "add_staff_acc_fb_one":
            category = "acc_fb_one"
        elif call.data == "add_staff_acc_fb_two":
            category = "acc_fb_two"
        elif call.data == "add_staff_acc_fb_three":
            category = "acc_fb_three"
        elif call.data == "add_staff_acc_fb_four":
            category = "acc_fb_four"
        rows = await db.select_buttons(category)
        for row in rows:
            txt = (''.join(str(item) for item in row))
            await call.message.answer(text="Выберете для добавления сатафа", reply_markup=InlineKeyboardMarkup(). \
                                 add(InlineKeyboardButton(txt, callback_data=f"add_staf{row[0]}")))



@dp.callback_query_handler(lambda x: x.data and x.data.startswith('add_staf'))
async def add_staff(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        button = call.data.replace('add_staf', "")
        await state.update_data(button=button)
        await add_state.add_staff_state.set()
        await call.message.answer(text=f"Начните добавление торавара в кнопку {button}!", reply_markup=cansel_menu)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('get_staff'))
async def call_get_staff(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")

    try:
        if chek_admin_status == "User" or "Admin":
            button = call.data.replace('get_staff', "")
            count_staff = await db.get_count_staff_in_db(button_name=button)
            count = count_staff[0]
            text = "Напишите число акков которое вы хотите взять \n" \
                   f"Доступное количество: {count} "
            await state.update_data(button=button)
            await get_staff_state.get_acc_state.set()
            await call.message.answer(text=text)
    except TypeError as err:
        await call.message.answer("Стаф в этой кнопке закончился 🫤")

