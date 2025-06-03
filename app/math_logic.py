import re
from math import sin, cos, tan, log
from aiogram.fsm.state import StatesGroup, State

class MathForm(StatesGroup):
    expression = State()

def safe_eval(expr: str) -> float:
    allowed_names = {
        'sin': sin,
        'cos': cos,
        'tan': tan,

    }
    
    expr = expr.replace('^', '**')
    

    if not re.match(r'^[\d+\-*/().\s^ sqrtincoglep]+$', expr.lower()):
        raise ValueError("Вираз містить недозволені символи")
    
    try:
        code = compile(expr, '<string>', 'eval')
        for name in code.co_names:
            if name not in allowed_names:
                raise ValueError(f"Заборонена функція: {name}")
        return eval(code, {'__builtins__': {}}, allowed_names)
    except Exception as e:
        raise ValueError(f"Помилка обчислення: {str(e)}")

def calculate_expression(expr: str) -> str:
    try:
        expr = expr.strip()
        if not expr:
            return " Пустий вираз"
            
        result = safe_eval(expr)
        return f" Результат: {expr} = {result}"
    except ValueError as e:
        return f" Помилка: {str(e)}"
    except Exception:
        return " Невідома помилка при обчисленні"