from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



butt_acc_fb_one = KeyboardButton("☑️ Кінг+автореги OCTO")
butt_acc_fb_two = KeyboardButton("✅ Фарм акк Facebook OCTO")
butt_acc_fb_three = KeyboardButton("Кінг+автореги  ADS")
butt_acc_fb_four = KeyboardButton("Фарм акк Facebook ADS")
my_staf = KeyboardButton("Товар взятый ранее")
user_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(butt_acc_fb_one, butt_acc_fb_two, butt_acc_fb_three, butt_acc_fb_four, my_staf)


#acc_fb = KeyboardButton("Акаунты ФБ")
#card = KeyboardButton("Карты - ФБ")
#proxy = KeyboardButton("Креативы")
#my_staf = KeyboardButton("Товар взятый ранее")
#user_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(acc_fb, card, proxy, my_staf)


cancel = KeyboardButton("Отеменить заказ")
cancel_fsm = ReplyKeyboardMarkup(resize_keyboard=True).add(cancel)

edit_users_admin = KeyboardButton("Редактировать пользователей")
edit_buttons = KeyboardButton("Редактировать кнопки")
add_staff = KeyboardButton("Добавить стаф")
exit_user_menu = KeyboardButton("/start")
show_history = KeyboardButton("История")
dell_history = KeyboardButton("Удалить историю")
admin_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(edit_users_admin, edit_buttons, show_history, add_staff, dell_history, exit_user_menu)


exit_admin_menu = KeyboardButton("/admin_panel")


show_users = KeyboardButton("Показать всех пользователей")
show_registr_users = KeyboardButton("Показать загегистрированных")
show_admin = KeyboardButton("Показать Админов")
settings_users_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(show_users, show_registr_users, show_admin, exit_admin_menu)



show_buttons = KeyboardButton("Удалить кнопку")
add_items_one = KeyboardButton("Добавить кнопку в ☑️ Кінг+автореги OCTO")
add_items_two = KeyboardButton("Добавить кнопку в ✅Фарм акк Facebook OCTO")
add_items_three = KeyboardButton("Добавить кнопку в Кінг+автореги  ADS")
add_items_four = KeyboardButton("Добавить кнопку в Фарм акк Facebook ADS")
settings_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(show_buttons, add_items_one, add_items_two, add_items_three, add_items_four, exit_admin_menu)

