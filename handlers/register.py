from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from config import *
from create_bot import dp, cur, db

#@dp.callback_query_handler(text="reg")
async def reg(call: types.CallbackQuery, state: FSMContext):
    data = cur.execute("SELECT TGID FROM Специалисты").fetchall()
    if tuple([call.from_user.id]) in data:
        await call.message.answer("Вы уже зарегистрированы!", reply_markup=mainKB )
        return
    await call.message.answer("Регистрация началась. Введите свою специальность: ")
    await state.set_state(RegSpec.prof)

#@dp.message_handler(state=RegSpec.prof)
async def reg_prof(mes: types.Message, state: FSMContext):
    # cur.execute("INSERT INTO Специалисты (Специальность) VALUES (?)", [mes.text])
    # db.commit()
    await state.update_data({"prof":mes.text})
    await mes.answer(f"Специальность '{mes.text}' установлена! \nТеперь введите свою Фамилию: ")
    await state.set_state(RegSpec.surname)


#@dp.message_handler(state=RegSpec.surname)
async def reg_surname(mes: types.Message, state: FSMContext):
    await state.update_data({"surname": mes.text})
    await mes.answer(f"Фамилия '{mes.text}' установлена!\nВведите свое Имя: ")
    await state.set_state(RegSpec.name)


#@dp.message_handler(state=RegSpec.name)
async def reg_name(mes: types.Message, state: FSMContext):
    await state.update_data({"name": mes.text})
    await mes.answer(f"Имя '{mes.text}' установлено!\nВведите свой номер телефона: ")
    await state.set_state(RegSpec.tNumber)


#@dp.message_handler(state=RegSpec.tNumber)
async def reg_tNumb(mes: types.Message, state: FSMContext):
    await state.update_data({"tNumber": mes.text})
    await mes.answer(f"номер телефона '{mes.text}' установлен!\nВведите свой номер email: ")
    await state.set_state(RegSpec.email)


#@dp.message_handler(state=RegSpec.email)
async def reg_email(mes: types.Message, state: FSMContext):
    await state.update_data({"email": mes.text})
    await mes.answer(f"email '{mes.text}' зарегистирован!\nВведите адрес предоставления услуг: ")
    await state.set_state(RegSpec.adress)


#@dp.message_handler(state=RegSpec.adress)
async def reg_adress(mes: types.Message, state: FSMContext):
    await state.update_data({"adress": mes.text})
    await mes.answer(f"адрес '{mes.text}' зарегистирован!\nВведите свое время работы: ")
    await state.set_state(RegSpec.tWork)


#@dp.message_handler(state=RegSpec.tWork)
async def reg_tW(mes: types.Message, state: FSMContext):
    await state.update_data({"twork": mes.text})
    data = await state.get_data()
    data_list = []
    for i in data.values():
        data_list.append(i)
    cur.execute("INSERT INTO Специалисты (TGID,Специальность, Фамилия, Имя, Телефон, Email, Адрес, РабочееВремя ) VALUES (?,?,?,?,?,?,?,?)", [mes.from_user.id] + data_list)
    db.commit()
    await mes.answer(f"время работы'{mes.text}' зарегистировано!\nРегистрация завершена ", reply_markup=mainKB)

    await state.finish()

def register_handlers_reg(dp:Dispatcher):
    dp.register_callback_query_handler(reg, text="reg")
    dp.register_message_handler(reg_prof, state=RegSpec.prof)
    dp.register_message_handler(reg_surname, state=RegSpec.surname)
    dp.register_message_handler(reg_name, state=RegSpec.name)
    dp.register_message_handler(reg_tNumb, state=RegSpec.tNumber)
    dp.register_message_handler(reg_email, state=RegSpec.email)
    dp.register_message_handler(reg_adress, state=RegSpec.adress)
    dp.register_message_handler(reg_tW, state=RegSpec.tWork)
