from settings import PAGE_SIZE
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
BUTTON_CALCULATE = " Обчислити вираз"
GEOMETRIC_CALCULATOR = " Геометричний калькулятор"
STOP = "Стоп"
def math_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=GEOMETRIC_CALCULATOR)
    builder.button(text=BUTTON_CALCULATE)
    builder.button(text=STOP)
    builder.adjust(2, 1) 
    return builder.as_markup(resize_keyboard=True)

def menu_keyboards():
    return math_menu_keyboard()

class TaskCallback(CallbackData, prefix="task", sep=";"):
    id: int
    title: str

def tasks_keyboard_markup(tasks_list: list[dict], page: int = 1):
    builder = InlineKeyboardBuilder()
    total_pages = (len(tasks_list) + PAGE_SIZE - 1) // PAGE_SIZE
    start_idx = (page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE

    for index, task in enumerate(tasks_list[start_idx:end_idx], start=start_idx):
        callback_task = TaskCallback(id=index, title=task["title"])
        builder.button(
            text=task["title"],
            callback_data=callback_task.pack()
        )

    builder.adjust(1)  
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text='< назад', callback_data=f"page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text='вперед >', callback_data=f"page_{page+1}"))
    if nav_buttons:
        builder.row(*nav_buttons)
    
    return builder.as_markup()
