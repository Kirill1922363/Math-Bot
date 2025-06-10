from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove,BotCommand
from aiogram.fsm.context import FSMContext

from .keyboards import BUTTON_CALCULATE, GEOMETRIC_CALCULATOR,STOP, math_menu_keyboard
from .math_logic import MathForm, calculate_expression

router = Router()

@router.message(F.text == STOP)
async def start_calculation(message: Message, state: FSMContext):
    await state.set_state(MathForm.expression)
    await message.answer(
        "Бот зупинено!",
        reply_markup=ReplyKeyboardRemove()
        )
    
@router.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "Доступні операції:\n"
        "+ додавання\n- віднімання\n* множення\n/ ділення\n^ степінь\n\n"
        "Геометричні функції:\n"
        "/circle_area(Площа кола): `S = π * r^2`\n"
        "/circle_perimeter(Периметр кола): `P = 2 * π * r`\n"
        "/rectangle_area(Площа прямокутника): `S = a * b`\n"
        "/rectangle_perimeter(Периметр прямокутника): `P = 2 * (a + b)`\n"
        "/triangle_area(Площа трикутника): `S = (a * h) / 2`\n"
        "Функції: sin(), cos(), tan()\n"
    )
    await message.answer(help_text, reply_markup=math_menu_keyboard())

@router.message(F.text == BUTTON_CALCULATE)
async def start_calculation(message: Message, state: FSMContext):
    await state.set_state(MathForm.expression)
    await message.answer(
        "Введіть математичний вираз або виберіть команду /help",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text == GEOMETRIC_CALCULATOR)
async def handle_geometry(message: Message):
    await message.answer(
        "Використовуйте /help для довідки.",
        reply_markup=math_menu_keyboard()
    )

@router.message(Command("calculator"))
async def command_calculator_handler(message: Message):
    await message.answer(
        "Введіть математичний вираз або виберіть команду /help",
        reply_markup=math_menu_keyboard()
    )

@router.message(MathForm.expression)
async def evaluate(message: Message, state: FSMContext):
    result = calculate_expression(message.text)
    await state.clear()
    await message.answer(result, reply_markup=math_menu_keyboard())

@router.message(Command("circle_area"))
async def circle_area_handler(message: Message):
    try:
        radius = float(message.text.split()[1])
        area = 3.14159 * radius ** 2
        await message.answer(f"Площа кола з радіусом {radius} дорівнює {area:.2f}")
    except (IndexError, ValueError):
        await message.answer("Будь ласка, введіть радіус кола у форматі: /circle_area радіус")

@router.message(Command("circle_perimeter"))
async def circle_perimeter_handler(message: Message):
    try:
        radius = float(message.text.split()[1])
        perimeter = 2 * 3.14159 * radius
        await message.answer(f"Периметр кола з радіусом {radius} дорівнює {perimeter:.2f}")
    except (IndexError, ValueError):
        await message.answer("Будь ласка, введіть радіус кола у форматі: /circle_perimeter радіус")

@router.message(Command("rectangle_area"))
async def rectangle_area_handler(message: Message):
    try:
        dimensions = message.text.split()[1:]
        if len(dimensions) != 2:
            raise ValueError("Потрібно ввести дві сторони прямокутника")
        a, b = map(float, dimensions)
        area = a * b
        await message.answer(f"Площа прямокутника зі сторонами {a} і {b} дорівнює {area:.2f}")
    except (IndexError, ValueError) as e:
        await message.answer(f"Помилка: {str(e)}. Використовуйте формат: /rectangle_area a b")

@router.message(Command("rectangle_perimeter"))
async def rectangle_perimeter_handler(message: Message):
    try:
        dimensions = message.text.split()[1:]
        if len(dimensions) != 2:
            raise ValueError("Потрібно ввести дві сторони прямокутника")
        a, b = map(float, dimensions)
        perimeter = 2 * (a + b)
        await message.answer(f"Периметр прямокутника зі сторонами {a} і {b} дорівнює {perimeter:.2f}")
    except (IndexError, ValueError) as e:
        await message.answer(f"Помилка: {str(e)}. Використовуйте формат: /rectangle_perimeter a b")

@router.message(Command("triangle_area"))
async def triangle_area_handler(message: Message):
    try:
        dimensions = message.text.split()[1:]
        if len(dimensions) != 2:
            raise ValueError("Потрібно ввести основу і висоту трикутника")
        a, h = map(float, dimensions)
        area = (a * h) / 2
        await message.answer(f"Площа трикутника з основою {a} і висотою {h} дорівнює {area:.2f}")
    except (IndexError, ValueError) as e:
        await message.answer(f"Помилка: {str(e)}. Використовуйте формат: /triangle_area a h")

@router.message(F.text & ~F.text.startswith('/'))  
async def handle_all_text_messages(message: Message):
    if any(char in message.text for char in '+-*/^()'):  
        result = calculate_expression(message.text)
        await message.answer(result, reply_markup=math_menu_keyboard())
    else:
        await message.answer("Введіть вираз або виберіть команду /help")
