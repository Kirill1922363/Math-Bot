from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import math
from .math_logic import MathForm,calculate_expression

from .keyboards import math_menu_keyboard,geometric_calculator_keyboard,BUTTON_CALCULATE,GEOMETRIC_CALCULATOR

router = Router()

class GeometryStates(StatesGroup):
    waiting_radius = State()
    waiting_rectangle_sides = State()
    waiting_triangle_params = State()



@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "Доступні операції:\n"
        "+ додавання\n- віднімання\n* множення\n/ ділення\n^ степінь\n\n"
        "Геометричні функції:\n"
        "Площа кола: S = π * r²\n"
        "Довжина кола: P = 2 * π * r\n"
        "Площа прямокутника: S = a * b\n"
        "Периметр прямокутника: P = 2 * (a + b)\n"
        "Площа трикутника: S = (a * h) / 2\n"
        "Функції: sin(), cos(), tan()\n"
    )
    await message.answer(help_text)

@router.message(F.text == BUTTON_CALCULATE)
async def start_calculation(message: Message, state: FSMContext):
    await state.set_state(MathForm.expression)
    await message.answer(
        "Введіть математичний вираз або виберіть команду /help",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text == GEOMETRIC_CALCULATOR)
@router.message(Command("geometric_calculator"))
async def cmd_geometric_calculator(message: Message):
    await message.answer(
        "📐 <b>Геометричний калькулятор</b>",
        reply_markup=geometric_calculator_keyboard()
    )

@router.message(F.text == "Площа кола ⭕")
async def cmd_circle_area(message: Message, state: FSMContext):
    await state.set_state(GeometryStates.waiting_radius)
    await message.answer("Введіть радіус кола:", reply_markup=ReplyKeyboardRemove())

@router.message(GeometryStates.waiting_radius)
async def process_circle_area(message: Message, state: FSMContext):
    try:
        radius = float(message.text)
        area = math.pi * radius ** 2
        await message.answer(
            f"🔷 Площа кола з радіусом {radius}: <b>{area:.2f}</b>cm^2",
            reply_markup=geometric_calculator_keyboard()
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Будь ласка, введіть коректне число!")

@router.message(F.text == "Довжина кола ⭕")
async def cmd_circle_perimeter(message: Message, state: FSMContext):
    await state.set_state(GeometryStates.waiting_radius)
    await message.answer("Введіть радіус кола:", reply_markup=ReplyKeyboardRemove())

@router.message(GeometryStates.waiting_radius)
async def process_circle_perimeter(message: Message, state: FSMContext):
    try:
        radius = float(message.text)
        perimeter = 2 * math.pi * radius
        await message.answer(
            f"🔵 Довжина кола з радіусом {radius}: <b>{perimeter:.2f}</b>cm",
            reply_markup=geometric_calculator_keyboard()
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Будь ласка, введіть коректне число!")

@router.message(F.text == "Площа прямокутника 🟦")
async def cmd_rectangle_area(message: Message, state: FSMContext):
    await state.set_state(GeometryStates.waiting_rectangle_sides)
    await message.answer("Введіть довжину та ширину через пробіл:", reply_markup=ReplyKeyboardRemove())

@router.message(GeometryStates.waiting_rectangle_sides)
async def process_rectangle_area(message: Message, state: FSMContext):
    try:
        a, b = map(float, message.text.split())
        area = a * b
        await message.answer(
            f"🟦 Площа прямокутника {a}×{b}: <b>{area:.2f}</b>cm^2",
            reply_markup=geometric_calculator_keyboard()
        )
        await state.clear()
    except:
        await message.answer("❌ Введіть два числа через пробіл!")

@router.message(F.text == "Периметр прямокутника 🟦")
async def cmd_rectangle_perimeter(message: Message, state: FSMContext):
    await state.set_state(GeometryStates.waiting_rectangle_sides)
    await message.answer("Введіть довжину та ширину через пробіл:", reply_markup=ReplyKeyboardRemove())

@router.message(GeometryStates.waiting_rectangle_sides)
async def process_rectangle_perimeter(message: Message, state: FSMContext):
    try:
        a, b = map(float, message.text.split())
        perimeter = 2 * (a + b)
        await message.answer(
            f"🟧 Периметр прямокутника {a}×{b}: <b>{perimeter:.2f}</b>cm",
            reply_markup=geometric_calculator_keyboard()
        )
        await state.clear()
    except:
        await message.answer("❌ Введіть два числа через пробіл!")

@router.message(F.text == "Площа трикутника 🔺")
async def cmd_triangle_area(message: Message, state: FSMContext):
    await state.set_state(GeometryStates.waiting_triangle_params)
    await message.answer("Введіть основу та висоту через пробіл:", reply_markup=ReplyKeyboardRemove())

@router.message(GeometryStates.waiting_triangle_params)
async def process_triangle_area(message: Message, state: FSMContext):
    try:
        a, h = map(float, message.text.split())
        area = (a * h) / 2
        await message.answer(
            f"🔺 Площа трикутника (основа {a}, висота {h}): <b>{area:.2f}</b>cm^2",
            reply_markup=geometric_calculator_keyboard()
        )
        await state.clear()
    except:
        await message.answer("❌ Введіть два числа через пробіл!")

@router.message(F.text == "Назад ◀️")
async def cmd_back(message: Message):
    await message.answer(
        "Повернення до головного меню",
        reply_markup=math_menu_keyboard()
    )


@router.message(F.text & ~F.text.startswith("/"))
async def handle_all_text_messages(message: Message):
    if any(char in message.text for char in "+-*/^()"):
        result = calculate_expression(message.text)
        await message.answer(result, reply_markup=math_menu_keyboard())
    else:
        await message.answer("Введіть вираз або виберіть команду /help")
