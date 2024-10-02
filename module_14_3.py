from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button1)
kb.add(button2)
kb.add(button3)

in_kb = InlineKeyboardMarkup(resize_keyboard=True)
key1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
key2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_kb.add(key1)
in_kb.add(key2)

in_kb2 = InlineKeyboardMarkup(resize_keyboard=True)
but1 = InlineKeyboardButton(text='Вишня', callback_data='product_buying')
but2 = InlineKeyboardButton(text='Клубника', callback_data='product_buying')
but3 = InlineKeyboardButton(text='Персик-Маракуйя', callback_data='product_buying')
but4 = InlineKeyboardButton(text='Шоколад', callback_data='product_buying')
in_kb2.add(but1)
in_kb2.add(but2)
in_kb2.add(but3)
in_kb2.add(but4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=in_kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    await message.answer('Название: Вишня | Описание: Гейнер со вкусом вишни | Цена: 100')
    with open('files/gCh1.PNG', 'rb') as img1:
        await message.answer_photo(img1)
    await message.answer('Название: Клубника | Описание: Гейнер со вкусом клубники | Цена: 200')
    with open('files/gkl2.PNG', 'rb') as img2:
        await message.answer_photo(img2)
    await message.answer('Название: Персик-Маракуйя | Описание: Гейнер со вкусом персик-маракуйя | Цена: 300')
    with open('files/gPM3.PNG', 'rb') as img3:
        await message.answer_photo(img3)
    await message.answer('Название: Шоколад | Описание: Гейнер со вкусом шоколада | Цена: 400')
    with open('files/gSh4.PNG', 'rb') as img4:
        await message.answer_photo(img4)
    await message.answer('Выберите продукт для покупки: ', reply_markup=in_kb2)



@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора: '
                              '\n\n для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              '\n\n для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(gro=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(wei=message.text)
    data = await state.get_data()
    await message.answer(
        f'Ваша норма калорий: {10 * int(data["wei"])+ 6.25 * int(data["gro"]) - 5 * int(data["age"]) + 5} '
        f'калорий.')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Теперь я умею не только считать норму калорий, '
                         'но и могу показать тебе формулу расчета, ведь я развиваюсь!'
                         ' А еще теперь я могу продавать полезные товары;)')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду "/start", чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
