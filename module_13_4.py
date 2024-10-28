from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    
@dp.message_handler(text = 'Calories')
async def set_age(message):
    await message.answer('Напишите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите совй рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_growth(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = float(data.get('age'))
    growth = float(data.get('growth'))
    weight = float(data.get('weight'))
    bmr = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f"Ваша норма калорий: {bmr:.2f} ккал")
    await state.finish()
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)