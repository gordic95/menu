from django import template
from menu_app.models import MainMenu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, parent_slug=None):
    """ Кастомный тег для отображения меню """
    def build_menu_items(menus):
        """ Функция построения HTML-кода меню рекурсивно """
        items = []

        for menu in menus:
            if menu.is_active:
                item_html = f"<li><a href='{menu.url}'>{menu.title}</a>"

                children = MainMenu.objects.filter(parent=menu.id)
                if children.exists():
                    item_html += '<ul>'
                    item_html += build_menu_items(children)
                    item_html += '</ul>'

                item_html += "</li>"
                items.append(item_html)

        return ''.join(items)


    root_menus = MainMenu.objects.filter(parent__isnull=True)
    return f"<ul>{build_menu_items(root_menus)}</ul>"