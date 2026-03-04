#!/usr/bin/env python
"""
Скрипт для заполнения базы данных тестовыми данными
"""
import os
import django
from datetime import date, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voda_spa.settings')
django.setup()

from main.models import (
    Service, BathType, PoolType, GalleryImage,
    SliderImage, Contact, SocialNetwork, Action
)


def create_contact():
    """Создание контактной информации"""
    contact, created = Contact.objects.get_or_create(
        defaults={
            'phone': '+7 (351) 220-77-66',
            'email': 'upr@termyvoda.ru',
            'address': 'г. Челябинск, мкр. «Вишнёвая горка», ул. Олимпийская, 29',
            'work_hours': 'Ежедневно с 9:00 до 23:00',
            'map_coordinates': '55.164440, 61.436844'
        }
    )
    if created:
        print("✅ Контактная информация создана")
    else:
        print("ℹ️  Контактная информация уже существует")


def create_social_networks():
    """Создание социальных сетей"""
    socials = [
        {'name': 'ВКонтакте', 'url': 'https://vk.com/termyvoda', 'icon_class': 'vk', 'order': 1},
        {'name': 'Telegram', 'url': 'https://t.me/+79919077667', 'icon_class': 'telegram', 'order': 2},
        {'name': 'WhatsApp', 'url': 'https://wa.me/79919077667', 'icon_class': 'whatsapp', 'order': 3},
    ]

    for social_data in socials:
        social, created = SocialNetwork.objects.get_or_create(
            name=social_data['name'],
            defaults=social_data
        )
        if created:
            print(f"✅ Социальная сеть {social.name} создана")


def create_services():
    """Создание услуг"""
    services = [
        {
            'title': 'Отель VODA',
            'category': 'hotel',
            'short_description': 'Стильные номера с видом на лес',
            'description': 'Комфортабельные номера с современным дизайном, панорамными окнами и всеми необходимыми удобствами для отдыха.',
            'price': 3500.00,
            'order': 1
        },
        {
            'title': 'Термальный бассейн открытый',
            'category': 'pools',
            'short_description': 'Работает круглый год под открытым небом',
            'description': 'Открытый термальный бассейн с температурой воды +38°C. Работает зимой и летом.',
            'price': 1200.00,
            'order': 1
        },
        {
            'title': 'Термальный бассейн закрытый',
            'category': 'pools',
            'short_description': 'Крытый бассейн с комфортной температурой',
            'description': 'Закрытый термальный бассейн с контролируемой температурой воды и воздуха.',
            'price': 1000.00,
            'order': 2
        },
        {
            'title': 'Русская баня',
            'category': 'baths',
            'short_description': 'Традиционная русская баня с березовыми вениками',
            'description': 'Настоящая русская баня на дровах с парилкой, моечной и комнатой отдыха.',
            'price': 2500.00,
            'order': 1
        },
        {
            'title': 'Сауна Булочка с эспрессо',
            'category': 'baths',
            'short_description': 'Уютная финская сауна',
            'description': 'Финская сауна с сухим паром, ароматерапией и возможностью заказа эспрессо.',
            'price': 2000.00,
            'order': 2
        },
        {
            'title': 'Кафе VODA',
            'category': 'cafe',
            'short_description': 'Большой выбор блюд европейской и русской кухни',
            'description': 'Уютное кафе с разнообразным меню, включающим горячие блюда, закуски, десерты и напитки.',
            'order': 1
        },
        {
            'title': 'Pool Bar',
            'category': 'cafe',
            'short_description': 'Прохладительные напитки у бассейна',
            'description': 'Бар у бассейна с освежающими напитками, коктейлями и легкими закусками.',
            'order': 2
        },
        {
            'title': 'СПА-процедуры',
            'category': 'spa',
            'short_description': 'Релаксация и оздоровление',
            'description': 'Широкий спектр СПА-процедур: массаж, обертывания, косметические процедуры.',
            'price': 3000.00,
            'order': 1
        },
        {
            'title': 'Детская зона',
            'category': 'children',
            'short_description': 'Безопасный отдых для детей',
            'description': 'Специально оборудованная детская зона с мелким бассейном и игровой площадкой.',
            'price': 500.00,
            'order': 1
        },
    ]

    for service_data in services:
        service, created = Service.objects.get_or_create(
            title=service_data['title'],
            defaults=service_data
        )
        if created:
            print(f"✅ Услуга {service.title} создана")


def create_bath_types():
    """Создание типов бань"""
    baths = [
        {
            'name': 'Русская баня',
            'description': 'Традиционная русская баня на дровах',
            'capacity': 8,
            'price_per_hour': 2500.00,
            'features': 'Парилка, моечная, комната отдыха, веники'
        },
        {
            'name': 'Сауна Булочка с эспрессо',
            'description': 'Финская сауна с ароматерапией',
            'capacity': 6,
            'price_per_hour': 2000.00,
            'features': 'Сухой пар, ароматерапия, эспрессо-машина'
        },
        {
            'name': 'Пивная сауна',
            'description': 'Уникальная сауна с пивными ароматами',
            'capacity': 8,
            'price_per_hour': 2800.00,
            'features': 'Пивная ароматерапия, комната отдыха, холодные напитки'
        },
        {
            'name': 'Альпийская сауна',
            'description': 'Сауна в альпийском стиле',
            'capacity': 6,
            'price_per_hour': 2200.00,
            'features': 'Альпийские травы, горный воздух, релаксация'
        },
    ]

    for bath_data in baths:
        bath, created = BathType.objects.get_or_create(
            name=bath_data['name'],
            defaults=bath_data
        )
        if created:
            print(f"✅ Тип бани {bath.name} создан")


def create_pool_types():
    """Создание типов бассейнов"""
    pools = [
        {
            'name': 'Открытый термальный бассейн',
            'description': 'Открытый бассейн с горячей термальной водой',
            'temperature': '+38°C',
            'depth': '0.8 - 1.4 м',
            'is_outdoor': True
        },
        {
            'name': 'Закрытый термальный бассейн',
            'description': 'Крытый бассейн с подогревом',
            'temperature': '+36°C',
            'depth': '1.0 - 1.6 м',
            'is_outdoor': False
        },
        {
            'name': 'Детский бассейн',
            'description': 'Мелкий бассейн для детей',
            'temperature': '+32°C',
            'depth': '0.4 - 0.6 м',
            'is_outdoor': False
        },
    ]

    for pool_data in pools:
        pool, created = PoolType.objects.get_or_create(
            name=pool_data['name'],
            defaults=pool_data
        )
        if created:
            print(f"✅ Тип бассейна {pool.name} создан")


def create_actions():
    """Создание акций"""
    today = date.today()
    actions = [
        {
            'title': 'Новогодняя акция',
            'description': 'Скидка 20% на все услуги в новогодние праздники!',
            'discount_percent': 20,
            'start_date': today,
            'end_date': today + timedelta(days=30)
        },
        {
            'title': 'Семейный отдых',
            'description': 'При посещении семьей от 4 человек - скидка 15%',
            'discount_percent': 15,
            'start_date': today,
            'end_date': today + timedelta(days=60)
        },
        {
            'title': 'День рождения',
            'description': 'В день рождения - бесплатное посещение именинника!',
            'start_date': today,
            'end_date': today + timedelta(days=365)
        },
    ]

    for action_data in actions:
        action, created = Action.objects.get_or_create(
            title=action_data['title'],
            defaults=action_data
        )
        if created:
            print(f"✅ Акция {action.title} создана")


def main():
    """Основная функция для создания всех тестовых данных"""
    print("🚀 Начинаем заполнение базы данных тестовыми данными...")
    print()

    create_contact()
    create_social_networks()
    create_services()
    create_bath_types()
    create_pool_types()
    create_actions()

    print()
    print("✅ Заполнение базы данных завершено!")
    print("🔗 Админ-панель доступна по адресу: http://localhost:8000/admin/")
    print("👤 Логин: admin")
    print("🔒 Пароль: admin123")


if __name__ == '__main__':
    main()
