from django import template
from menu_app.models import MainMenu

register = template.Library()

def _draw_menu(menuitems, active_item_id=None, level=0):
    """тэг для отрисовки меню"""
    result = [] # список для сохранения строки меню
    for i in menuitems:  # перебор элементов меню
        children = i.children.all() if hasattr(i, 'children') else []  # получение всех дочерних элементов
        active = i.id == active_item_id or any(child.id == active_item_id for child in children)  # проверка активности элемента меню
        result.append(f'<li class="{"active" if active else ""}"><a href="{i.url}">{i.title}</a>')  # добавление строки меню

        if len(children) > 0 and (level <= 1 or active):  # проверка на наличие дочерних элементов и уровень вложенности
            result.append('<ul>' + "".join(_draw_menu(children, active_item_id, level + 1)) + '</ul>')  # рекурсивный вызов для дочерних элементов
            result.append('</li>')  # закрытие тега списка
    return ''.join(result)  # объединение всех строк в одну строку меню

@register.simple_tag(takes_context=True)  # регистрация тэга с параметром context
def draw_menu(context, menu_name):  # функция для отрисовки меню
    request = context['request']  # получение объекта запроса из контекста
    current_path = request.path   # получение текущего пути запроса
    root_items = MainMenu.objects.filter(parent__isnull=True).prefetch_related('children').all()  # получение корневых элементов меню с предварительной выборкой дочерних элементов
    active_root = next((root for root in root_items if root.is_active(current_path)), None)  # получение активного корневого элемента меню
    if active_root:  # если есть активный корневой элемент меню
        first_level_children = active_root.children.all().prefetch_related('children')   # получение дочерних элементов первого уровня с предварительной выборкой дочерних элементов
    else:
        first_level_children = []  # если нет активного корневого элемента меню, то список дочерних элементов первого уровня будет пустым

    html = '<ul>'   # начало строки меню
    html += _draw_menu(root_items, active_root.id if active_root else None)  # вызов функции для отрисовки меню
    html += '</ul>'  # конец строки меню
    return html  # возврат строки меню


