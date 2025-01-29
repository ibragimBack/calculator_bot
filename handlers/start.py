from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import datetime, timedelta

from keyboards.start_keyboard import choose_start_kb


class Calculator(StatesGroup):
    sum = State()
    months = State()
    mode = State()

start_router = Router()


@start_router.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('Выберите рассрочку, а если хотите завершить процесс используйте команду /stop', reply_markup=choose_start_kb())


@start_router.message(Command('stop'))
async def stop_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Процесс завершен')


@start_router.message(F.text.lower() == 'mbank mplus')
async def calculation_with_bank(message: types.Message, state: FSMContext):
    await state.update_data(mode='with_bank')
    await state.set_state(Calculator.sum)
    await message.answer('Введите сумму: ' )


@start_router.message(F.text.lower() == 'рассрочка без банка')
async def calculation_without_bank(message: types.Message, state: FSMContext):
    await state.update_data(mode='without_bank')
    await state.set_state(Calculator.sum)
    await message.answer(f'Введите сумму: ')


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
        result = ((sum / 100) * 10) + sum 
        await message.answer(f'Результаты расчета: {result} сом')
        await state.clear()
    else:
        sum = int(sum)
        await state.set_state(Calculator.months)
        await message.answer('Введите срок в количестве месяцев: ')


@start_router.message(Calculator.months)
async def results_without_bank(message: types.Message, state: FSMContext):
    months = message.text

    if not months.isdigit():
        await message.answer('Срок должен быть числом!!!')
        return 
    
    months = int(months)

    if months < 1 or months > 3:
        await message.answer('Срок может быть от 1 до 3 месяцев!!!')
        return
    
    await state.update_data(months=message.text)
    data = await state.get_data()
    sum = int(data['sum'])

    prepayment = round((sum / 100) * 30, 2)
    monthly_payment = round(int(sum - prepayment) / int(months), 2)

    async def generate_payment_schedule(start_date, months, monthly_payment, prepayment):
        schedule = []
        current_date = datetime.strptime(start_date, "%d.%m.%Y")
        schedule.append((current_date.strftime("%d.%m.%Y"), prepayment))
        for i in range(1, months + 1):
            payment_date = current_date + timedelta(days=30 * i)
            schedule.append((payment_date.strftime("%d.%m.%Y"), monthly_payment))
        return schedule
    
    start_date = datetime.now().strftime("%d.%m.%Y")
    payment_schedule = await generate_payment_schedule(start_date, months, monthly_payment, prepayment)

    result_message = (
        f'Результаты расчета \n'
        f'Сумма: {sum} сом \n'
        f'Предоплата 30%: {prepayment} сом \n\n'
        f'График оплаты: \n'
    )
    for i, (date, amount) in enumerate(payment_schedule, 1):
        result_message += f"{i}. {date} - {amount} сом \n"

    await message.answer(result_message)
    await state.clear()
