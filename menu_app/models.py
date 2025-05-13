from django.db import models

class MainMenu(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Главное меню"
        verbose_name = "Главное меню"

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(MainMenu, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Пункты меню"
        verbose_name = "Пункт меню"

