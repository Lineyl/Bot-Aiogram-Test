from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from config import *
from create_bot import dp, cur, db


# @dp.message_handler(text="Добавить", state="*")
async def nameU(mes: types.Message, state: FSMContext):
    await mes.answer("Добавление услуги. Введите название: ", reply_markup=cancelKB)
    await state.set_state(addUslug.name)


# @dp.message_handler(state=addUslug.name)
async def opis(mes: types.Message, state: FSMContext):
    await mes.answer(f"Название {mes.text} успешно добавлено! Теперь введите описание",
                     reply_markup=cancelKB)
    await state.update_data({"name": mes.text})
    await state.set_state(addUslug.opis)


# @dp.message_handler(state=addUslug.opis)
async def final(mes: types.Message, state: FSMContext):
    await mes.answer(f"Описание успешно добавлено: {mes.text} ")
    await mes.answer("Услуга упешно добавлена!", reply_markup=mainU)
    await state.update_data({"opis": mes.text})
    data = await state.get_data()
    data_list = []
    for i in data.values():
        data_list.append(i)
    cur.execute(
        "INSERT INTO Услуги (Название,Описание, ID_Специалиста) VALUES (?,?,?)",
        data_list + [mes.from_user.id])
    db.commit()
    await state.finish()


# @dp.message_handler(text="Услуги")
async def U(mes: types.Message):
    data = cur.execute(f"SELECT ID, Название FROM Услуги WHERE ID_Специалиста={mes.from_user.id}").fetchall()
    if not data:
        await mes.answer("У вас нет ни одной услуги! Создайте ее с помощью команды", reply_markup=mainU)
        return
    mess = ""
    for i in data:
        mess += f"ID-{i[0]}\n - {i[1]}\n\n"
    await mes.answer(f"Список ваших услуг: \n{mess}", reply_markup=mainU)


# @dp.message_handler(text="Удалить")
async def delU(mes: types.Message, state: FSMContext):
    data = cur.execute(f"SELECT ID, Название FROM Услуги WHERE ID_Специалиста={mes.from_user.id}").fetchall()
    if not data:
        await mes.answer("У вас нет ни одной услуги! Создайте ее с помощью команды")
        return
    mess = ""
    for i in data:
        mess += f"ID-{i[0]}\n - {i[1]}\n\n"
    await mes.answer(f"Введите ID услуги, которую хотите удалить: \n{mess}", reply_markup=cancelKB)
    await state.set_state(delUslug.waitID)


# @dp.message_handler(state=delUslug.waitID)
async def delById(mes: types.Message, state: FSMContext):
    data = cur.execute(
        f"SELECT ID, Название FROM Услуги WHERE ID={int(mes.text)} AND ID_Специалиста={mes.from_user.id}").fetchall()
    if not data:
        await mes.answer("Неверный ID! Повторите ввод!")
        return
    cur.execute(f"DELETE FROM Услуги WHERE ID={int(mes.text)} AND ID_Специалиста = {mes.from_user.id}")
    await mes.answer(f"Услуга '{data[0][1]}' успешно удалена!", reply_markup=mainU)
    db.commit()
    await state.finish()


# @dp.message_handler(text="Редактировать")
async def redU(mes: types.Message, state: FSMContext):
    data = cur.execute(f"SELECT ID, Название FROM Услуги WHERE ID_Специалиста={mes.from_user.id}").fetchall()
    mess = ""
    for i in data:
        mess += f"ID-{i[0]}\n - {i[1]}\n\n"
    await mes.answer(f"Введите ID услуги, которую хотите редактировать: \n{mess}", reply_markup=cancelKB)
    await state.set_state(redUslug.waitID)


# @dp.message_handler(state=redUslug.waitID)
async def redWhat(mes: types.Message, state: FSMContext):
    try:
        data = cur.execute(
            f"SELECT ID, Название, Описание FROM Услуги WHERE ID={mes.text} AND ID_Специалиста = {mes.from_user.id}").fetchone()
        mess = f"ID: {data[0]}\nНазвание: {data[1]}\nОписание: {data[2]}\nВыберите, что хотите редактировать: "
    except:
        await mes.answer("Такого ID не найдено!\nПовторите ввод:", reply_markup=cancelKB)
        return
    await state.update_data({"ID": data[0]})
    await mes.answer(mess, reply_markup=choiceRedKB)
    await state.set_state(redUslug.waitWhat)


# @dp.message_handler(state=redUslug.waitWhat)
async def choiseRed(mes: types.Message, state: FSMContext):
    if mes.text == "Название":
        await mes.answer("Введите новое название: ", reply_markup=cancelKB)
        await state.set_state(redUslug.waitName)
    elif mes.text == "Описание":
        await mes.answer("Введите новое описание: ", reply_markup=cancelKB)
        await state.set_state(redUslug.waitOpis)
    else:
        await mes.answer("Не помнимаю, что вы хотите!\nНажмите, пожалуйста, на кнопку!",
                         reply_markup=choiceRedKB)


# @dp.message_handler(state=redUslug.waitName)
async def redNameU(mes: types.Message, state: FSMContext):
    data = await state.get_data()
    cur.execute(f"UPDATE Услуги SET Название='{mes.text}' WHERE ID={data['ID']}")
    db.commit()
    await mes.answer("Название успешно обновлено!", reply_markup=mainU)
    await state.finish()


# @dp.message_handler(state=redUslug.waitOpis)
async def redOpisU(mes: types.Message, state: FSMContext):
    data = await state.get_data()
    cur.execute(f"UPDATE Услуги SET Описание='{mes.text}' WHERE ID={data['ID']}")
    db.commit()
    await mes.answer("Описание успешно обновлено!", reply_markup=mainU)
    await state.finish()


def register_handlers_uslug(dp: Dispatcher):
    dp.register_message_handler(nameU, text="Добавить", state="*")
    dp.register_message_handler(opis, state=addUslug.name)
    dp.register_message_handler(final, state=addUslug.opis)
    dp.register_message_handler(U, text="Услуги")
    dp.register_message_handler(delU, text="Удалить")
    dp.register_message_handler(delById, state=delUslug.waitID)
    dp.register_message_handler(redU, text="Редактировать")
    dp.register_message_handler(redWhat, state=redUslug.waitID)
    dp.register_message_handler(choiseRed, state=redUslug.waitWhat)
    dp.register_message_handler(redNameU, state=redUslug.waitName)
    dp.register_message_handler(redOpisU, state=redUslug.waitOpis)
