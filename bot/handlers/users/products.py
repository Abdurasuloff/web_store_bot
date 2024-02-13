from aiogram import types
from loader import dp, db, bot
from keyboards.default.buttons import category_buttons, menu
from keyboards.inline.products_buttons import subcategories_keyboard, sub_category_callback, products_keyboard, product_callback, shop_keyboard, shopping_callback, buy_product, buy_product_callback, back_button, back_callback
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import ReplyKeyboardRemove
from utils.misc.product import Product
from aiogram.types import LabeledPrice
from data.shipping_methods import *
from data.config import ADMINS


@dp.message_handler(text='🧾 Katalog')
async def show_category(message: types.Message):
   
    categories = db.select_all_categories()
    
    button = await category_buttons(categories)
    
    await message.delete()
    await message.answer("Kategoriya tanlang 🔽", reply_markup=button )
    

@dp.message_handler(Text(startswith="🔘"))
async def show_subcategory(message: types.Message):
   
    try:
        category_name = message.text[1:]
        category = db.select_category(name=category_name)

        subcategories = db.select_subcategories(category_id=str(category[0]))
        
        button = await subcategories_keyboard(subcategories)
        
        await message.delete()
        await message.answer("Kategoriya tanlang 🔽",  reply_markup=button)
        
    except Exception as err:
        print(err)
        
        await message.answer("Noto'g'ri kategoriya.")


@dp.message_handler(Text(equals='◀️ Oqraga'))
async def back_katalog(message: types.Message):
   
    await message.delete()
    text = await message.answer("Siz bosh menyudasiz:", reply_markup=menu )
    

# @dp.callback_query_handler(Text(startswith="back:"))
# async def back_menu(call: types.CallbackQuery):
#     await call.message.delete()
    
    
@dp.callback_query_handler(sub_category_callback.filter())
async def back_menu(call: types.CallbackQuery, callback_data:dict):
    # await call.message.delete()
    await call.answer(cache_time=60)
   
        
    # category_id = callback_data['category']
    subcategory_id = str(callback_data['id'])
    
    products  = db.select_products(sub_category_id=subcategory_id)
    
    subcat = db.select_subcategory(id=subcategory_id)
    
    button =  await products_keyboard(products, category_id=subcat[2])
    
    await call.message.edit_text("Mahsulot tanlang:", reply_markup=button)
    # await call.message.edit_reply_markup(button)
    # await call.message.answer(text="Mahsulot tanlang:", reply_markup=button, )
        
   
    
    
@dp.callback_query_handler(product_callback.filter())
async def show_product(call: types.CallbackQuery, callback_data:dict):
    
    
    await call.answer()
    
    product = db.select_product(id=str(callback_data['id']))
   
   
    text = f"<b>Nomi:</b> {product[1]} \n\n"
    text += f"<b>Ma'lumot: </b> {product[2]}\n\n"
    text += f"<b>Narxi: </b> {product[3]} so'm\n\n" 
    
    product_image = product[-1]
    
    product_url = "https://storetgbot.pythonanywhere.com/media/" + str(product_image)
    
    keyboard = await shop_keyboard(product[0], call.from_user.id, subcategory_id=product[4])
    
    # print(product["image"])
    await call.message.delete()
    # print(product[-1])
    try:
        await call.message.answer_photo(product_url, caption=text, reply_markup=keyboard)
    except:
        await call.message.answer_photo(product_image, caption=text,  reply_markup=keyboard)
    finally:
        await call.message.answer(text, reply_markup=keyboard)
    
    
  
@dp.callback_query_handler(shopping_callback.filter())
async def add_to_cart(call: types.CallbackQuery, callback_data:dict):
    print(callback_data)
    
    product_id = callback_data['product_id']
    user_id = callback_data['user_id']
    

    
    #===========================================================
        #   MAHSULOTNI SAVATGA QO"SHAMIZ
    #===========================================================
    status =  db.add_product_to_cart(user_id, product_id)
    if status == "error":
        await call.answer("⛔️ Mahsulot qo'shib bo'lmadi")
    
    elif status == "added-before":
        
        await call.answer("❇️ Mahsulot oldin qo'shilgan.")
    
    await call.answer("✅ Mahsulot savatga qo'shildi. ")  
    await call.message.delete()
    await call.message.answer("Menyu tanlang:", reply_markup=menu)
    
    
@dp.message_handler(Text(equals="🛒 Savatcha"))
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    await message.delete()
    
    products = db.select_user_products(user_id=str(user_id))
    
    main_text = "<b>Savatdagi tovarlar:</b>\n\n"
    text = ""
    counter = 1
    total_price = 0
    
    
    for product in products:
        # print(product[2])
        pr = db.select_product(id=str(product[2]))
        text += f"{counter}. Nomi: {pr[1]} so'm\n"
        text += f"    Narxi: {pr[3]} so'm\n\n"
        counter += 1
        total_price += pr[3]
        
    
    text += "Jami: \n"
    text += f"Mahsulotlar soni: {counter-1}\n"
    text += f"Jami: {total_price} so'm"
    
    button = await buy_product(total_price, "Sotilgan mahsulotlar qaytarib olinmaydi!!")
    
    await message.answer(main_text + text, reply_markup=button)
    
    
@dp.callback_query_handler(buy_product_callback.filter())
async def send_invoice(call: types.CallbackQuery, callback_data:dict):
    await call.answer()
    # print(callback_data)
    
    product = Product(
        title="Savatchadagi mahsulotlarni xarid qilish.:",
        description=callback_data['description'],
        currency="UZS",
        prices=[
            LabeledPrice(
                label='Mahsulotlar',
                amount=int(callback_data["total_price"]+"00")
            ),
            LabeledPrice(
                label='Yetkazib berish (7 kun)',
                amount=1000000, # 10.000 so'm
            ),  
        ],
        start_parameter="products_cart_invoice",
        # photo_url='image_url',
        # photo_width=851,
        # photo_height=1280,
        # photo_size=800,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True, # foydalanuvchi manzilini kiritishi shart
        is_flexible=True,
    )

    await bot.send_invoice(chat_id=call.from_user.id, **product.generate_invoice(), payload="cart_shop")
    
    
@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
        
    elif query.shipping_address.city.lower() == "fergana":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)



@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat!")
    
    
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"                                
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}\n"
                                f"Address: {pre_checkout_query.order_info.shipping_address}")
    
    
    db.clear_user_cart(pre_checkout_query.from_user.id)
 
 

@dp.message_handler(Text(equals="⏳ Mahsulotlar tarixi"))
async def show_history(message:types.Message):
    await message.delete()
    
    histories = db.select_user_histories(user_id=message.from_user.id)
    
    text = "<b>Sizning buyurtmalar tarixingiz</b>\n\n"
    
    for i in histories:
        text += f"Buyurtma vaqti:{i[1]}\nStatus:{i[2]}\n\n"
        
    
    await message.answer(text, reply_markup=back_button)
    


@dp.callback_query_handler(back_callback.filter())
async def handle_back_buttons(call: types.CallbackQuery, callback_data:dict):
    # await call.answer()
    category_id = int(callback_data['category_id'])
    subcategory_id = int(callback_data['subcategory_id'])
    
    print(callback_data)
    
    if category_id == 0 and subcategory_id == 0:
        #home
        await call.message.delete()
        
    elif category_id != 0:
        #subcategoriyalar chiqadi
        # await call.answer("subcategoriyalar chiqadi")
        print(callback_data)
        subcategories = db.select_subcategories(category_id=str(category_id))
        
        button = await subcategories_keyboard(subcategories)
        
        await call.message.edit_text("Kategoriya tanlang 🔽",  reply_markup=button)
       
    
    elif subcategory_id != 0:
        #mahsulotlar ro'yxati
        products  = db.select_products(sub_category_id=str(subcategory_id))
    
        subcat = db.select_subcategory(id=subcategory_id)
        
        button =  await products_keyboard(products, category_id=subcat[2])
        

        await call.message.delete()
        await call.message.answer("Mahsulot tanlang 🔽", reply_markup=button)
