from django.db import models
from django.urls import reverse


class MainMenu(models.Model):
    title = models.CharField(max_length=50, verbose_name="Пункт меню", default='Название отсутствует')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Родительский пункт меню")
    route_name = models.CharField(max_length=200, verbose_name="Имя маршрута для ссылки", blank=True, null=True)
    url = models.URLField(verbose_name="Ссылка на страницу", max_length=200, blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Пункты меню"
        verbose_name = "Пункт меню"

    @property
    def is_active(self, current_path=None):
        if not current_path:
            return False
        try:
            if self.route_name:
                resolved_name = reverse(self.route_name)
                if resolved_name == current_path:
                    return True
        except Exception as e:
            return False

        if self.url:
            if self.url == current_path:
                return True


        for child in self.children.all():
            if child.is_active(current_path):
                return True

        return False

