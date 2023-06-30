from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from dispatcher import dp, db, bot
from aiogram import types
import asyncpg
from kayboard.inlyne_menu import cansel_menu

class add_state(StatesGroup):
    button_name_state = State()
    add_staff_state = State()

@dp.message_handler(state=add_state.button_name_state)
async def add_button_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        try:
            types_item_text = await state.get_data('types_item_text')
            get_types_item = types_item_text.get("types_item_text")
            button = message.text
            category = ""
            if get_types_item == "Добавить кнопку в ☑️ Кінг+автореги OCTO":
                category = "acc_fb_one"
            elif get_types_item == "Добавить кнопку в ✅Фарм акк Facebook OCTO":
                category = "acc_fb_two"
            elif get_types_item == "Добавить кнопку в Кінг+автореги  ADS":
                category = "acc_fb_three"
            elif get_types_item == "Добавить кнопку в Фарм акк Facebook ADS":
                category = "acc_fb_four"
            await db.add_button_file_id(button, category)
            await message.answer(F"Кнопка {button} добавленна")
            await state.finish()
        except asyncpg.exceptions.UniqueViolationError:
            await message.answer("Такая кнопка уже есть отправьте другую", reply_markup=cansel_menu)





@dp.message_handler(state=add_state.add_staff_state)
async def add_button_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chek_admin_status = await db.get_status_user(user_id=user_id)
    chek_admin_status = chek_admin_status.get("status")
    if chek_admin_status == "Admin":
        call_button = await state.get_data('button')
        button = call_button.get("button")
        file_name = message.text
        await db.add_staff_in_db(file_name=file_name, button_name=button)
        await message.answer(F"Расходник добавлен, если вы всё добавили нажмите \"Отмена\".", reply_markup=cansel_menu)


class get_staff_state(StatesGroup):
    get_acc_state = State()


@dp.message_handler(state=get_staff_state.get_acc_state)
async def add_staff_state(message: types.Message, state: FSMContext):
    count = message.text
    if count.isdigit() == False:
        error_text = "Введите число! Я не понимаю текст.\n" \
                     "Напишите количество например: 3301"
        await message.answer(text=error_text, reply_markup=cansel_menu)
       # await state.storage.reset()
        await get_staff_state.get_acc_state.set()
    else:
        count = int(count)
        for i in range(count):
            user_id = message.from_user.id
            chek_admin_status = await db.get_status_user(user_id=user_id)
            chek_admin_status = chek_admin_status.get("status")
            try:
                user_id = message.from_user.id
                user_name = message.from_user.username
                full_name = message.from_user.full_name
                status_not_str = await db.get_status_user(user_id=user_id)
                status = ''.join(status_not_str[0])
                button_name = await state.get_data('button')
                button_name = button_name['button']
                document = await db.get_staff_in_db(button_name=button_name)
                file_name = document.get("file_name")
                chat_id = message.chat.id
                user_id = int(user_id)
                await bot.send_message(chat_id=chat_id, text=file_name)
                await db.add_history(user_id=user_id, user_name=user_name, full_name=full_name, status=status, file_name=file_name, button_name=button_name)
                await db.delete_user_staff(file_name)
            except AttributeError as err:
                await message.answer("Стаф в этой кнопке закончился 🫤")
                break
        await state.finish()
