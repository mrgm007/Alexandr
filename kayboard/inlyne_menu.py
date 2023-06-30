from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cansel_menu = InlineKeyboardMarkup(row_width=1)
cansel = InlineKeyboardButton(text="Отмена", callback_data="cancel")
cansel_menu.add(cansel)


del_btn_user_menu = InlineKeyboardMarkup(row_width=1)
del_btn_acc_fb_one = InlineKeyboardButton(text="☑️ Кінг+автореги OCTO", callback_data="acc_fb_one")
del_btn_acc_fb_two = InlineKeyboardButton(text="✅ Фарм акк Facebook OCTO", callback_data="acc_fb_two")
del_btn_acc_fb_three = InlineKeyboardButton(text="Кінг+автореги  ADS", callback_data="acc_fb_three")
del_btn_acc_fb_four = InlineKeyboardButton(text="Фарм акк Facebook ADS", callback_data="acc_fb_four")
del_btn_user_menu.add(del_btn_acc_fb_one, del_btn_acc_fb_two, del_btn_acc_fb_three, del_btn_acc_fb_four)


add_staff_inlyne = InlineKeyboardMarkup(row_width=1)
add_staff_acc_fb_one = InlineKeyboardButton(text="☑️ Кінг+автореги OCTO", callback_data="add_staff_acc_fb_one")
add_staff_acc_fb_two = InlineKeyboardButton(text="✅ Фарм акк Facebook OCTO", callback_data="add_staff_acc_fb_two")
add_staff_acc_fb_three = InlineKeyboardButton(text="Кінг+автореги  ADS", callback_data="add_staff_acc_fb_three")
add_staff_acc_fb_four = InlineKeyboardButton(text="Фарм акк Facebook ADS", callback_data="add_staff_acc_fb_four")
add_staff_inlyne.add(add_staff_acc_fb_one, add_staff_acc_fb_two, add_staff_acc_fb_three, add_staff_acc_fb_four)

