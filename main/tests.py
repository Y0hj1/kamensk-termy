from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from .models import (
    Service, BathType, PoolType, GalleryImage,
    SliderImage, Contact, SocialNetwork, Action
)


class ModelsTestCase(TestCase):
    """Тесты для моделей"""

    def setUp(self):
        """Создание тестовых данных"""
        # Создаем изображение для тестов
        self.test_image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

    def test_service_creation(self):
        """Тест создания услуги"""
        service = Service.objects.create(
            title="Тестовая услуга",
            description="Описание тестовой услуги",
            category="pools",
            price=1000.00
        )

        self.assertEqual(service.title, "Тестовая услуга")
        self.assertEqual(service.category, "pools")
        self.assertEqual(service.price, 1000.00)
        self.assertTrue(service.is_active)
        self.assertEqual(str(service), "Тестовая услуга")

    def test_bath_type_creation(self):
        """Тест создания типа бани"""
        bath = BathType.objects.create(
            name="Тестовая сауна",
            description="Описание тестовой сауны",
            capacity=8,
            price_per_hour=1500.00
        )

        self.assertEqual(bath.name, "Тестовая сауна")
        self.assertEqual(bath.capacity, 8)
        self.assertTrue(bath.is_available)
        self.assertEqual(str(bath), "Тестовая сауна")

    def test_action_is_current_property(self):
        """Тест свойства is_current для акций"""
        # Текущая акция
        current_action = Action.objects.create(
            title="Текущая акция",
            description="Описание текущей акции",
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=30),
            is_active=True
        )

        # Завершившаяся акция
        expired_action = Action.objects.create(
            title="Завершившаяся акция",
            description="Описание завершившейся акции",
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() - timedelta(days=1),
            is_active=True
        )

        self.assertTrue(current_action.is_current)
        self.assertFalse(expired_action.is_current)


class ViewsTestCase(TestCase):
    """Тесты для представлений"""

    def setUp(self):
        """Настройка тестового клиента"""
        self.client = Client()

        # Создаем тестовые данные
        self.service = Service.objects.create(
            title="Тестовая услуга",
            description="Описание",
            category="pools",
            price=1000.00,
            is_active=True
        )

        self.contact = Contact.objects.create(
            phone="+7 (351) 220-77-66",
            email="test@test.ru",
            address="Тестовый адрес",
            work_hours="9:00 - 23:00"
        )

    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('main:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VODA")
        self.assertContains(response, "Наши услуги")

    def test_thermal_pools_page(self):
        """Тест страницы бассейнов"""
        response = self.client.get(reverse('main:thermal_pools'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Термальные бассейны")

    def test_baths_page(self):
        """Тест страницы бань"""
        response = self.client.get(reverse('main:baths'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Бани и сауны")

    def test_price_page(self):
        """Тест страницы прайса"""
        response = self.client.get(reverse('main:price'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Прайс-лист")

    def test_gallery_page(self):
        """Тест страницы галереи"""
        response = self.client.get(reverse('main:gallery'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Фотогалерея")

    def test_contacts_page(self):
        """Тест страницы контактов"""
        response = self.client.get(reverse('main:contacts'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Контакты")
        self.assertContains(response, self.contact.phone)

    def test_actions_page(self):
        """Тест страницы акций"""
        response = self.client.get(reverse('main:actions'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Акции")

    def test_certificates_page(self):
        """Тест страницы сертификатов"""
        response = self.client.get(reverse('main:certificates'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Подарочные сертификаты")

    def test_service_detail_page(self):
        """Тест детальной страницы услуги"""
        response = self.client.get(
            reverse('main:service_detail', args=[self.service.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service.title)

    def test_service_detail_404(self):
        """Тест 404 для несуществующей услуги"""
        response = self.client.get(
            reverse('main:service_detail', args=[999])
        )

        self.assertEqual(response.status_code, 404)


class URLsTestCase(TestCase):
    """Тесты для URL маршрутов"""

    def test_url_resolves_to_correct_view(self):
        """Тест корректности URL маршрутов"""
        urls_and_names = [
            ('/', 'main:home'),
            ('/services/termalnye-basseyny/', 'main:thermal_pools'),
            ('/services/bani/', 'main:baths'),
            ('/services/zona-spa/spa/', 'main:spa'),
            ('/services/eda/', 'main:cafe'),
            ('/services/detyam/', 'main:children'),
            ('/services/otel/', 'main:hotel'),
            ('/price/', 'main:price'),
            ('/actions/', 'main:actions'),
            ('/projects/', 'main:gallery'),
            ('/contacts/', 'main:contacts'),
            ('/gift-certificates/', 'main:certificates'),
        ]

        for url, name in urls_and_names:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn(response.status_code, [200, 301, 302])


class AdminTestCase(TestCase):
    """Тесты для административной панели"""

    def setUp(self):
        """Создание суперпользователя"""
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.ru',
            password='admin123'
        )
        self.client.login(username='admin', password='admin123')

    def test_admin_access(self):
        """Тест доступа к админке"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_service_admin(self):
        """Тест админки услуг"""
        response = self.client.get('/admin/main/service/')
        self.assertEqual(response.status_code, 200)

    def test_service_add(self):
        """Тест добавления услуги через админку"""
        response = self.client.post('/admin/main/service/add/', {
            'title': 'Новая услуга',
            'description': 'Описание новой услуги',
            'category': 'pools',
            'price': '1500.00',
            'is_active': True,
            'order': 0
        })

        self.assertIn(response.status_code, [200, 302])

        # Проверяем, что услуга создалась
        service_exists = Service.objects.filter(title='Новая услуга').exists()
        self.assertTrue(service_exists)


class FormValidationTestCase(TestCase):
    """Тесты валидации форм"""

    def test_contact_form_validation(self):
        """Тест валидации контактной формы"""
        # Тест будет добавлен при создании форм
        pass

    def test_booking_form_validation(self):
        """Тест валидации формы бронирования"""
        # Тест будет добавлен при создании форм
        pass


class IntegrationTestCase(TestCase):
    """Интеграционные тесты"""

    def setUp(self):
        """Создание полного набора тестовых данных"""
        # Услуги
        self.pool_service = Service.objects.create(
            title="Термальные бассейны",
            description="Открытый и закрытый бассейны",
            category="pools",
            price=800.00,
            is_active=True
        )

        # Бани
        self.bath = BathType.objects.create(
            name="Финская сауна",
            description="Классическая финская сауна",
            capacity=8,
            price_per_hour=1500.00,
            is_available=True
        )

        # Акции
        self.action = Action.objects.create(
            title="Скидка 30%",
            description="Скидка для новых клиентов",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            discount_percent=30,
            is_active=True
        )

        # Контакты
        self.contact = Contact.objects.create(
            phone="+7 (351) 220-77-66",
            email="info@termyvoda.ru",
            address="г. Челябинск, ул. Олимпийская, 29",
            work_hours="9:00 - 23:00"
        )

    def test_full_user_journey(self):
        """Тест полного пути пользователя по сайту"""
        # Главная страница
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Переход к услугам
        response = self.client.get('/services/termalnye-basseyny/')
        self.assertEqual(response.status_code, 200)

        # Просмотр прайса
        response = self.client.get('/price/')
        self.assertEqual(response.status_code, 200)

        # Просмотр акций
        response = self.client.get('/actions/')
        self.assertEqual(response.status_code, 200)

        # Контакты
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_data_consistency(self):
        """Тест целостности данных"""
        # Проверяем, что все созданные объекты существуют
        self.assertTrue(Service.objects.filter(title="Термальные бассейны").exists())
        self.assertTrue(BathType.objects.filter(name="Финская сауна").exists())
        self.assertTrue(Action.objects.filter(title="Скидка 30%").exists())
        self.assertTrue(Contact.objects.exists())

        # Проверяем связи и методы
        self.assertTrue(self.action.is_current)
        self.assertEqual(str(self.pool_service), "Термальные бассейны")


class PerformanceTestCase(TestCase):
    """Тесты производительности"""

    def setUp(self):
        """Создание большого количества тестовых данных"""
        # Создаем много услуг
        for i in range(50):
            Service.objects.create(
                title=f"Услуга {i}",
                description=f"Описание услуги {i}",
                category="pools",
                price=1000.00 + i * 100,
                is_active=True,
                order=i
            )

    def test_home_page_performance(self):
        """Тест производительности главной страницы"""
        import time

        start_time = time.time()
        response = self.client.get('/')
        end_time = time.time()

        self.assertEqual(response.status_code, 200)
        # Проверяем, что страница загружается быстро (менее 1 секунды)
        self.assertLess(end_time - start_time, 1.0)

    def test_gallery_pagination(self):
        """Тест пагинации галереи"""
        # Создаем много изображений галереи
        for i in range(25):
            GalleryImage.objects.create(
                title=f"Изображение {i}",
                category="pools"
            )

        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)

        # Проверяем пагинацию
        response = self.client.get('/projects/?page=2')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    import unittest
    unittest.main()
