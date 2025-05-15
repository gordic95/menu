from django.db import models
from django.urls import reverse


class MainMenu(models.Model):
    title = models.CharField(max_length=50, verbose_name="Пункт меню", default='Название отсутствует')  # Наименование пункта меню
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')   # Ссылка на родительский пункт меню
    route_name = models.CharField(max_length=200, verbose_name="Маршрут", blank=True, null=True)  # Имя маршрута для ссылки
    url = models.URLField(verbose_name="Ссылка", max_length=200, blank=True, null=True)  # Ссылка на страницу


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Пункты меню"
        verbose_name = "Пункт меню"

    @property
    def is_active(self, current_path=None):  # Проверка активности пункта меню
        if not current_path:  # Если нет текущего пути, то вернуть False
            return False
        try:
            if self.route_name:  # Если есть имя маршрута
                resolved_name = reverse(self.route_name)  # Получить имя маршрута
                if resolved_name == current_path:  # Если имя маршрута совпадает с текущим путем
                    return True
        except Exception as e:
            return False

        # Затем проверим прямой URL
        if self.url:
            if self.url == current_path:
                return True


        #Рекурсивно проверим активных детей
        for child in self.children.all():
            if child.is_active(current_path):
                return True

        return False

