from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.start_keyboard import choose_start_kb


class Calculator(StatesGroup):
    sum = State()
    months = State()
    mode = State()

start_router = Router()


@start_router.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, выберите рассрочку, а если хотите завершить процесс используйте команду /stop', reply_markup=choose_start_kb())


@start_router.message(Command('stop'))
async def stop_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Процесс завершен')


@start_router.message(F.text.lower() == 'mbank mplus')
async def calculation_with_bank(message: types.Message, state: FSMContext):
    await state.update_data(mode='with_bank')
    await state.set_state(Calculator.sum)
    await message.answer(f'{message.from_user.first_name} введите сумму: ' )


@start_router.message(F.text.lower() == 'рассрочка без банка')
async def calculation_without_bank(message: types.Message, state: FSMContext):
    await state.update_data(mode='without_bank')
    await state.set_state(Calculator.sum)
    await message.answer(f'{message.from_user.first_name} введите сумму: ')


@start_router.message(Calculator.sum)
async def sum_calculation(message: types.Message, state:FSMContext):
    sum = message.text
    if not sum.isdigit():
        await message.answer('Сумма должна быть числом!!!')
        return
    await state.update_data(sum=sum)
    user_data = await state.get_data()
    if user_data['mode'] == 'with_bank':
        sum = int(sum)
        result = ((sum / 100) * 20) + sum 
        await message.answer(f'Результаты расчета: {result} сом')
        await state.clear()
    else:
        await state.set_state(Calculator.months)
        await message.answer(f'{message.from_user.first_name} введите срок в количестве месяцев: ')


@start_router.message(Calculator.months)
async def results_without_bank(message: types.Message, state: FSMContext):
    months = message.text
    if not months.isdigit():
        await message.answer('Срок должен быть числом!!!')
        return 
    await state.update_data(months=message.text)
    data = await state.get_data()
    sum = int(data['sum'])
    sum_with_percent = ((sum / 100) * 20) + sum
    prepayment = (sum_with_percent / 100) * 30
    monthly_payment = int(sum_with_percent - prepayment) / int(months)
    await message.answer(f'Результаты расчета \n'
                        f'Сумма: {sum_with_percent} сом \n'
                        f'Предоплата 30%: {prepayment} сом \n'
                        f'Ежемесяная оплата: {monthly_payment} сом')
    await state.clear()

