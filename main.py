from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from config import *
from handlers import uslug, register
from create_bot import dp, cur, db


@dp.message_handler(commands="start")
async def start(mes: types.Message):
    await mes.answer("Приветствую!", reply_markup=regKB)
    try:
        cur.execute("INSERT INTO Клиенты (TelegramID) VALUES (?)", [mes.from_user.id])
        db.commit()
    except Exception:
        pass

@dp.message_handler(text="Назад")
async def mainM(mes:types.Message):
    await mes.answer("Главное меню", reply_markup=mainKB)

@dp.message_handler(text="Отмена", state="*")
async def cancel(mes:types.Message, state: FSMContext):
    await mes.answer("Действи отменено!\nГлавное меню", reply_markup=mainKB)
    await state.finish()


register.register_handlers_reg(dp)
uslug.register_handlers_uslug(dp)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)