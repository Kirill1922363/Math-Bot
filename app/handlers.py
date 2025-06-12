from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .keyboards import BUTTON_CALCULATE, GEOMETRIC_CALCULATOR, math_menu_keyboard
from .math_logic import MathForm, calculate_expression

router = Router()


class GeometryForm(StatesGroup):
    waiting_for_radius = State()
    waiting_for_rectangle_sides = State()
    waiting_for_triangle_params = State()


@router.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "Доступні операції:\n"
        "+ додавання\n- віднімання\n* множення\n/ ділення\n^ степінь\n\n"
        "Геометричні функції:\n"
        "/circle_area - Площа кола: S = π * r²\n"
        "/circle_perimeter - Довжина кола: P = 2 * π * r\n"
        "/rectangle_area - Площа прямокутника: S = a * b\n"
        "/rectangle_perimeter - Периметр прямокутника: P = 2 * (a + b)\n"
        "/triangle_area - Площа трикутника: S = (a * h) / 2\n"
        "Функції: sin(), cos(), tan()\n"
    )
    await message.answer(help_text, reply_markup=math_menu_keyboard())


@router.message(F.text == BUTTON_CALCULATE)
async def start_calculation(message: Message, state: FSMContext):
    await state.set_state(MathForm.expression)
    await message.answer(
        "Введіть математичний вираз або виберіть команду /help",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text == GEOMETRIC_CALCULATOR)
async def handle_geometry(message: Message):
    await message.answer(
        "Оберіть геометричну операцію:\n"
        "/circle_area - площа кола\n"
        "/circle_perimeter - довжина кола\n"
        "/rectangle_area - площа прямокутника\n"
        "/rectangle_perimeter - периметр прямокутника\n"
        "/triangle_area - площа трикутника",
        reply_markup=math_menu_keyboard(),
    )


@router.message(MathForm.expression)
async def evaluate(message: Message, state: FSMContext):
    result = calculate_expression(message.text)
    await state.clear()
    await message.answer(result, reply_markup=math_menu_keyboard())


@router.message(Command("circle_area"))
async def circle_area_handler(message: Message, state: FSMContext):
    await state.set_state(GeometryForm.waiting_for_radius)
    await message.answer("Введіть радіус кола:")


@router.message(GeometryForm.waiting_for_radius)
async def process_circle_area(message: Message, state: FSMContext):
    try:
        radius = float(message.text)
        area = 3.14159 * radius**2
        await state.clear()
        await message.answer(
            f"Площа кола з радіусом {radius} дорівнює {area:.2f}",
            reply_markup=math_menu_keyboard(),
        )
    except ValueError:
        await message.answer("Будь ласка, введіть коректне число для радіусу")


@router.message(Command("circle_perimeter"))
async def circle_perimeter_handler(message: Message, state: FSMContext):
    await state.set_state(GeometryForm.waiting_for_radius)
    await message.answer("Введіть радіус кола для обчислення довжини:")


@router.message(Command("rectangle_area"))
async def rectangle_area_handler(message: Message, state: FSMContext):
    await state.set_state(GeometryForm.waiting_for_rectangle_sides)
    await message.answer("Введіть довжини двох сторін прямокутника через пробіл:")


@router.message(GeometryForm.waiting_for_rectangle_sides)
async def process_rectangle_sides(message: Message, state: FSMContext):
    try:
        a, b = map(float, message.text.split())
        area = a * b
        await state.clear()
        await message.answer(
            f"Площа прямокутника зі сторонами {a} і {b} дорівнює {area:.2f}",
            reply_markup=math_menu_keyboard(),
        )
    except ValueError:
        await message.answer("Будь ласка, введіть два числа, розділені пробілом")


@router.message(Command("rectangle_perimeter"))
async def rectangle_perimeter_handler(message: Message, state: FSMContext):
    await state.set_state(GeometryForm.waiting_for_rectangle_sides)
    await message.answer(
        "Введіть довжини двох сторін прямокутника для обчислення периметра:"
    )


@router.message(Command("triangle_area"))
async def triangle_area_handler(message: Message, state: FSMContext):
    await state.set_state(GeometryForm.waiting_for_triangle_params)
    await message.answer("Введіть основу та висоту трикутника через пробіл:")


@router.message(GeometryForm.waiting_for_triangle_params)
async def process_triangle_params(message: Message, state: FSMContext):
    try:
        a, h = map(float, message.text.split())
        area = (a * h) / 2
        await state.clear()
        await message.answer(
            f"Площа трикутника з основою {a} і висотою {h} дорівнює {area:.2f}",
            reply_markup=math_menu_keyboard(),
        )
    except ValueError:
        await message.answer(
            "Будь ласка, введіть два числа (основу та висоту), розділені пробілом"
        )


@router.message(F.text & ~F.text.startswith("/"))
async def handle_all_text_messages(message: Message):
    if any(char in message.text for char in "+-*/^()"):
        result = calculate_expression(message.text)
        await message.answer(result, reply_markup=math_menu_keyboard())
    else:
        await message.answer("Введіть вираз або виберіть команду /help")
