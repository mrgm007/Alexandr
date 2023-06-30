from aiogram import types
from dispatcher import dp, bot, db
import asyncpg
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from kayboard.menu import user_menu, admin_menu, settings_users_admin, settings_buttons
from kayboard.inlyne_menu import del_btn_user_menu, cansel_menu, add_staff_inlyne
from .state import add_state
from aiogram.dispatcher.storage import FSMContext
import sqlite3
import os
import datetime

today = datetime.date.today()

@dp.message_handler(commands ="start")
async def start(message: types.Message):
   # await db.drop_users()
    user_id = message.from_user.id
    if user_id == 417416236:
        status = "Admin"
        await db.add_status_for_user(user_id=user_id, status=status)
        await message.answer(text='Александр, вы назначены Админом')
    chek_admin_status = await db.get_status_user(user_id=user_id)
    if chek_admin_status is not None:
        chek_admin_status = chek_admin_status.get("status")
    else:
        print(chek_admin_status)
    try:
        await db.add_user(user_id=message.from_user.id, user_name=message.from_user.first_name,
                        full_name=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError as Err:
        print(Err)
    if chek_admin_status == "Admin" or chek_admin_status == "User":
        await message.answer(text='Hey bro🖐', reply_markup=user_menu)
    else:
        await message.answer(text='Hey bro🖐')


@dp.message_handler(text =["☑️ Кінг+автореги OCTO", "✅ Фарм акк Facebook OCTO", "Кінг+автореги  ADS", "Фарм акк Facebook ADS"])
async def get_staff(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin" or chek_admin_status == "User":
        type_item = message.text
        category = ""
        buttons = []

        if type_item == "☑️ Кінг+автореги OCTO":
            category = "acc_fb_one"
        elif type_item == "✅ Фарм акк Facebook OCTO":
            category = "acc_fb_two"
        elif type_item == "Кінг+автореги  ADS":
            category = "acc_fb_three"
        elif type_item == "Фарм акк Facebook ADS":
            category = "acc_fb_four"

        rows = await db.select_buttons(category)
        for row in rows:
            txt = (''.join(str(item) for item in row))
            buttons.append(InlineKeyboardButton(f"{txt}", callback_data=f"get_staff{row[0]}"))
        keyboard = InlineKeyboardMarkup().add(*buttons)
        await message.answer(text=f"Выберете тип акков из категории \"{type_item}\"", reply_markup=keyboard)



#Нужно дописать функцию которая будет принимать callback_data=f"del_for_basket{row[0]}")


# Admin menu
# Admin menu
# Admin menu
# Admin menu


@dp.message_handler(text="/admin_panel")
async def admin_start(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        text1 = "Админ панель включена"
        await message.answer(text=text1, reply_markup=admin_menu)



@dp.message_handler(text="Редактировать пользователей")
async def edit_users(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        text1 = "Меню редактирования пользователей включено"
        await message.answer(text=text1, reply_markup=settings_users_admin)


@dp.message_handler(text="Редактировать кнопки")
async def edit_buttons(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        text1 = "Меню редактирования кнопок включено"
        await message.answer(text=text1, reply_markup=settings_buttons)


@dp.message_handler(text=["Добавить кнопку в ☑️ Кінг+автореги OCTO", "Добавить кнопку в ✅Фарм акк Facebook OCTO", "Добавить кнопку в Кінг+автореги  ADS", "Добавить кнопку в Фарм акк Facebook ADS"])
async def add_batons(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        types_item_text = message.text
        await state.update_data(types_item_text=types_item_text)
        text = "Напишите как будет называться кнопка"
        await add_state.button_name_state.set()
        await message.answer(text=text, reply_markup=cansel_menu)



@dp.message_handler(text="Удалить кнопку")
async def show_edit_buttons(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        text = "Выберете пункт "
        await message.answer(text=text, reply_markup=del_btn_user_menu)



@dp.message_handler(text="Показать всех пользователей")
async def show_edit_buttons(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        rows = await db.select_all_users()
        data_user = ["User_id: ", "Ник: ", "Юзернейм: @", "Статус: "]
        for row in rows:
            buttons = []
            txt = '\n'.join([f"{data_user[i]}{row[i]}" for i in range(len(row))])
            #txt = ('\n'.join(str(item) for item in row))
            buttons.append(InlineKeyboardButton(f"Удалить", callback_data=f"del_users{row[0]}"))
            buttons.append(InlineKeyboardButton("Зарегистрировать", callback_data=f"register_user{row[0]}"))
            buttons.append(InlineKeyboardButton("Сделать Админом", callback_data=f"register_admin{row[0]}"))
            keyboard = InlineKeyboardMarkup().add(*buttons)
            await message.answer(txt, reply_markup=keyboard)


@dp.message_handler(text=["Показать загегистрированных", "Показать Админов"])
async def show_edit_buttons(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        status = ""
        if message.text == "Показать загегистрированных":
            status = "User"
        elif message.text == "Показать Админов":
            status= "Admin"
        rows = await db.select_user_for_status(status)
        data_user = ["User_id: ", "Ник: ", "Юзернейм: @", "Статус: "]
        for row in rows:
            buttons = []
            txt = '\n'.join([f"{data_user[i]}{row[i]}" for i in range(len(row))])
            #txt = ('\n'.join(str(item) for item in row))
            buttons.append(InlineKeyboardButton(f"Удалить", callback_data=f"del_users{row[0]}"))
            buttons.append(InlineKeyboardButton("Зарегистрировать", callback_data=f"register_user{row[0]}"))
            buttons.append(InlineKeyboardButton("Сделать Админом", callback_data=f"register_admin{row[0]}"))
            keyboard = InlineKeyboardMarkup().add(*buttons)
            await message.answer(txt, reply_markup=keyboard)



@dp.message_handler(text="Добавить стаф")
async def show_edit_buttons(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        text = "Выберете пункт в который вы хотите добавить расходники "
        await message.answer(text=text, reply_markup=add_staff_inlyne)


@dp.message_handler(text="История")
async def show_edit_buttons(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        rows = await db.select_all_history()
        data_user = ["User_id: ", "Юзернейм: @", "Ник: ", "Статус: ", "Акк: ", "Кнопка: "]
        for row in rows:
            txt = '\n'.join([f"{data_user[i]}{row[i]}" for i in range(len(data_user))])
            await message.answer(txt)




@dp.message_handler(text="Удалить историю")
async def show_edit_buttons(message: types.Message):
    user_id = message.from_user.id
    if user_id == 417416236:
        await db.delete_all_history()
        await message.answer("История удалена")
    else:
        await message.answer("Вы не можете удалять историю")



@dp.message_handler(text="Товар взятый ранее")
async def show_edit_buttons(message: types.Message):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    chat_id = message.chat.id
    if chek_admin_status == "Admin" or chek_admin_status == "User":
        rows = await db.show_history_user(user_id)
        data_user = ["User_id: ", "Юзернейм: @", "Ник: ", "Статус: ", "Акк: ", "Кнопка: "]
        for row in rows:
            txt = '\n'.join([f"{data_user[i]}{row[i]}" for i in range(len(data_user))])
            await message.answer(txt)



