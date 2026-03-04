from django.db import models
from django.urls import reverse


class Service(models.Model):
    """Модель для услуг комплекса"""
    CATEGORY_CHOICES = [
        ('hotel', 'Отель'),
        ('pools', 'Термальные бассейны'),
        ('baths', 'Бани'),
        ('cafe', 'Кафе'),
        ('spa', 'СПА'),
        ('children', 'Детям'),
    ]

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    short_description = models.CharField('Краткое описание', max_length=300, blank=True)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField('Изображение', upload_to='services/')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField('Активно', default=True)
    order = models.IntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class BathType(models.Model):
    """Модель для видов бань"""
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='baths/')
    capacity = models.IntegerField('Вместимость')
    price_per_hour = models.DecimalField('Цена за час', max_digits=8, decimal_places=2)
    features = models.TextField('Особенности', blank=True)
    is_available = models.BooleanField('Доступна', default=True)

    class Meta:
        verbose_name = 'Вид бани'
        verbose_name_plural = 'Виды бань'

    def __str__(self):
        return self.name


class PoolType(models.Model):
    """Модель для видов бассейнов"""
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='pools/')
    temperature = models.CharField('Температура', max_length=50)
    depth = models.CharField('Глубина', max_length=50)
    is_outdoor = models.BooleanField('Открытый', default=False)

    class Meta:
        verbose_name = 'Вид бассейна'
        verbose_name_plural = 'Виды бассейнов'

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Модель для фотогалереи"""
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='gallery/')
    category = models.CharField('Категория', max_length=50, choices=[
        ('pools', 'Бассейны'),
        ('baths', 'Бани'),
        ('hotel', 'Отель'),
        ('cafe', 'Кафе'),
        ('spa', 'СПА'),
        ('exterior', 'Экстерьер'),
    ])
    description = models.TextField('Описание', blank=True)
    order = models.IntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Фото галереи'
        verbose_name_plural = 'Фотогалерея'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class SliderImage(models.Model):
    """Модель для слайдера на главной странице"""
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    image = models.ImageField('Изображение', upload_to='slider/')
    link_url = models.URLField('Ссылка', blank=True)
    link_text = models.CharField('Текст ссылки', max_length=100, blank=True)
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайдер'
        ordering = ['order']

    def __str__(self):
        return self.title


class Contact(models.Model):
    """Модель для контактной информации"""
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    address = models.TextField('Адрес')
    work_hours = models.CharField('Часы работы', max_length=100)
    map_coordinates = models.CharField('Координаты карты', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"Контакты {self.phone}"


class SocialNetwork(models.Model):
    """Модель для социальных сетей"""
    name = models.CharField('Название', max_length=50)
    url = models.URLField('Ссылка')
    icon_class = models.CharField('CSS класс иконки', max_length=50)
    order = models.IntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'
        ordering = ['order']

    def __str__(self):
        return self.name


class Action(models.Model):
    """Модель для акций"""
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actions/')
    discount_percent = models.IntegerField('Скидка %', null=True, blank=True)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def is_current(self):
        from datetime import date
        return self.start_date <= date.today() <= self.end_date


class Booking(models.Model):
    """Модель для бронирования услуг"""
    SERVICE_TYPES = [
        ('cafe', 'Столик в кафе'),
        ('pool', 'Термальные бассейны'),
        ('bath', 'Баня/сауна'),
        ('spa', 'СПА-процедуры'),
        ('hotel', 'Номер в отеле'),
    ]

    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('confirmed', 'Подтверждена'),
        ('cancelled', 'Отменена'),
        ('completed', 'Выполнена'),
    ]

    # Основная информация
    service_type = models.CharField('Тип услуги', max_length=20, choices=SERVICE_TYPES)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Услуга')
    bath_type = models.ForeignKey(BathType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип бани')

    # Клиентские данные
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True)

    # Детали бронирования
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    guests_count = models.IntegerField('Количество гостей', default=1)
    duration_hours = models.IntegerField('Продолжительность (часы)', default=2)

    # Дополнительная информация
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')

    # Служебные поля
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.name} ({self.date})"

    @property
    def total_price(self):
        """Расчет общей стоимости"""
        if self.service and self.service.price:
            return self.service.price * self.guests_count
        elif self.bath_type:
            return self.bath_type.price_per_hour * self.duration_hours
        return 0


class ContactRequest(models.Model):
    """Модель для заявок обратной связи"""
    REQUEST_TYPES = [
        ('callback', 'Заказ звонка'),
        ('question', 'Вопрос'),
        ('complaint', 'Жалоба'),
        ('suggestion', 'Предложение'),
    ]

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]

    # Основная информация
    request_type = models.CharField('Тип запроса', max_length=20, choices=REQUEST_TYPES, default='callback')
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True)

    # Содержание запроса
    subject = models.CharField('Тема', max_length=200, blank=True)
    message = models.TextField('Сообщение', blank=True)

    # Предпочтительное время звонка (для заказа звонка)
    preferred_time = models.CharField('Предпочтительное время звонка', max_length=100, blank=True)

    # Служебные поля
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    response = models.TextField('Ответ', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Запрос обратной связи'
        verbose_name_plural = 'Запросы обратной связи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.name}"


class Newsletter(models.Model):
    """Модель для подписки на новости"""
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Имя', max_length=100, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка на новости'
        verbose_name_plural = 'Подписки на новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
