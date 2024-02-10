from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
	keyboard = [
		[
			KeyboardButton(text="🧾 Katalog"),
			KeyboardButton(text="🛒 Savatcha"),
			KeyboardButton(text="⏳ Mahsulotlar tarixi"),

		]
	], 
	resize_keyboard = True
)


async def category_buttons(categories):
    keyboard = [
        [],
    ]    
    
    for i in categories:
        if len(keyboard[-1]) < 3:
            keyboard[-1].append(KeyboardButton(f"🔘{i[1]}"))
        else:
            keyboard.append([KeyboardButton(f"🔘{i[1]}")])
               
    keyboard.append([
		KeyboardButton("◀️ Oqraga")
	])
    
    
    cats = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    
    return cats

