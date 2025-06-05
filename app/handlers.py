from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from .keyboards import BUTTON_CALCULATE, math_menu_keyboard
from .math_logic import MathForm, calculate_expression

router = Router()

@router.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "Доступні операції:\n"
        "+ додавання\n- віднімання\n* множення\n/ ділення\n^ степінь\n\n"
        "Функції:sin(), cos(), tan()\n"
    )
    await message.answer(help_text, reply_markup=math_menu_keyboard())

@router.message(F.text == BUTTON_CALCULATE)
async def start_calculation(message: Message, state: FSMContext):
    await state.set_state(MathForm.expression)
    await message.answer(
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command("calculator"))
async def command_calculator_handler(message: Message):
    await message.answer(
        "Режим калькулятора. Введіть вираз:",
        reply_markup=math_menu_keyboard()
    )

@router.message(MathForm.expression)
async def evaluate(message: Message, state: FSMContext):
    result = calculate_expression(message.text)
    await state.clear()
    await message.answer(result, reply_markup=math_menu_keyboard())

@router.message(F.text & ~F.text.startswith('/'))  
async def handle_all_text_messages(message: Message):
    if any(char in message.text for char in '+-*/^()'):  
        result = calculate_expression(message.text)
        await message.answer(result, reply_markup=math_menu_keyboard())
    else:
        await message.answer("Введіть математичний вираз або виберіть команду /help")