from django.db import models

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    """Модель для Категорий продукта"""

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", **NULLABLE)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель для продукта"""

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(
        verbose_name="Описание", **NULLABLE
    )  # blank=True. null=True
    preview = models.ImageField(
        upload_to="products_foto", verbose_name="Изображение", **NULLABLE
    )
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.SET_NULL, null=True
    )
    price = models.IntegerField(verbose_name="Цена")
    date_of_creation = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    last_modified_date = models.DateField(auto_now=True, verbose_name="Дата изменения")

    view_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Version(models.Model):
    """Модель для версии продукта"""

    product = models.ForeignKey(
        Product,
        related_name="versions",
        verbose_name="Продукт",
        on_delete=models.CASCADE,
    )
    number = models.PositiveIntegerField(
        verbose_name=" Номер версии", blank=True, null=True
    )
    name = models.CharField(max_length=150, verbose_name="Название версии")
    is_current = models.BooleanField(default=True, verbose_name="Признак актуальности")

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ("name",)

    def __str__(self):
        return self.name
