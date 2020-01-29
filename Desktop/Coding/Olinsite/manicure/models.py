from django.db import models
from django.core import validators
from django.core.validators import RegexValidator


# Создавай свои модели здесь

# Модель раздела прайса
class PricePart(models.Model):
    part_price = models.CharField(max_length=20, db_index=True, verbose_name='Раздел прайса')

    class Meta:
        verbose_name_plural = 'Разделы'
        verbose_name = 'Раздел'
        # ordering = ['-part_price']

    def __str__(self):
        return self.part_price

    def get_items(self):
        items = PriceItem.objects.filter(pricepart__part_price=self)
        return items


# Модель услуги в прайсе
class PriceItem(models.Model):
    title = models.CharField(max_length=50, verbose_name='Услуга')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')

    pricepart = models.ForeignKey('PricePart', null=True, on_delete=models.PROTECT, verbose_name='Раздел')


    class Meta:
        verbose_name_plural = 'Прайс'
        verbose_name = 'Услуга'
        # ordering = ['-price'] сортировка по цене


# Модель добавление изображения
class AboutMaster(models.Model):
    image = models.ImageField(
        upload_to='static', height_field=None,
        width_field=None, max_length=100, verbose_name='Ссылка на изображение')

    text = models.TextField(max_length=1500, blank=True, null=True, verbose_name='Текст')

    def last(self):
        last_about = AboutMaster.objects.filter(aboutmaster__image=self)
        return last_about

    class Meta:
        verbose_name_plural = 'О мастере'
        verbose_name = 'Фото и текст'
        # ordering = ['-price'] сортировка по цене

    def image_img(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Фото'
    image_img.allow_tags = True


# Модель добавления отзывов
class FeedbackItem(models.Model):
    photo = models.ImageField(
        upload_to='static/feedphotos', height_field=None,
        width_field=None, max_length=100, verbose_name='Ссылка на фото'
    )
    name = models.CharField(max_length=50, verbose_name='Имя')
    text = models.TextField(max_length=1500, null=True, blank=True, verbose_name='Текст отзыва')

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    def feedback_photo(self):
        if self.photo:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.photo.url))
        else:
            return '(Нет изображения)'
    feedback_photo.short_description = 'Фото'
    feedback_photo.allow_tags = True


# Модель добавления фотографий галереи
class GalleryPhoto(models.Model):
    photo = models.ImageField(
        upload_to='static/galleryphotos', height_field=None,
        width_field=None, max_length=100, verbose_name='Ссылка на фото', db_index=True,
    )

    class Meta:
        verbose_name_plural = 'Фотографии галереи'
        verbose_name = 'Фото'

    def gallery_photo(self):
        if self.photo:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.photo.url))
        else:
            return '(Нет изображения)'
    gallery_photo.short_description = 'Фото'
    gallery_photo.allow_tags = True


# Модель сохранения данных контактной формы
class Contact(models.Model):
    name = models.CharField(max_length=15, blank=False, verbose_name='Имя',
                            validators=[validators.RegexValidator( regex=r'[A-Za-z]' )],
                            error_messages={'invalid': 'Некорректно введено имя'}
                            )

    last_name = models.CharField(max_length=25, blank=False, verbose_name='Фамилия',
                                 validators=[validators.RegexValidator( regex=r'[A-Za-z]' )],
                                 error_messages={'invalid': 'Некорректно введена фамилия'} )

    phone_number = models.CharField(max_length=17, blank=False, verbose_name='Моб. телефон',
                                    validators=[validators.RegexValidator(regex=r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')],error_messages={'invalid': 'Некорректно введен номер'})
    message = models.TextField(max_length=250, blank=False, verbose_name='Сообщение')

    class Meta:
        verbose_name_plural = 'Записи'
        verbose_name = 'Клиент'