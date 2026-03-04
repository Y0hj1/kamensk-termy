from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Case, When
from django.db.models.functions import Lower
from django.templatetags.static import static
from .models import (
    Service, BathType, PoolType, GalleryImage,
    SliderImage, Contact, SocialNetwork, Action
)


def home(request):
    """Главная страница"""
    # Получаем данные для главной страницы
    slider_images = SliderImage.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)
    gallery_images = GalleryImage.objects.all()[:12]  # Первые 12 фото для главной
    current_actions = Action.objects.filter(is_active=True)[:3]

    # Группируем услуги по категориям для секции "Наши услуги"
    service_categories = {
        'hotel': services.filter(category='hotel').first(),
        'pools': services.filter(category='pools').first(),
        'baths': services.filter(category='baths').first(),
        'cafe': services.filter(category='cafe').first(),
    }

    context = {
        'slider_images': slider_images,
        'service_categories': service_categories,
        'gallery_images': gallery_images,
        'current_actions': current_actions,
    }

    return render(request, 'main/home.html', context)


def services_thermal_pools(request):
    """Страница термальных бассейнов"""
    pools = PoolType.objects.all()
    pool_services = Service.objects.filter(category='pools', is_active=True)

    context = {
        'pools': pools,
        'services': pool_services,
        'page_title': 'Термальные бассейны',
    }

    return render(request, 'main/thermal_pools.html', context)


def services_baths(request):
    """Страница бань"""
    baths = BathType.objects.filter(is_available=True)
    bath_services = Service.objects.filter(category='baths', is_active=True)

    context = {
        'baths': baths,
        'services': bath_services,
        'page_title': 'Бани',
    }

    return render(request, 'main/baths.html', context)


def services_spa(request):
    """Страница СПА"""
    spa_services = Service.objects.filter(category='spa', is_active=True)

    context = {
        'services': spa_services,
        'page_title': 'СПА',
    }

    return render(request, 'main/spa.html', context)


def services_cafe(request):
    """Страница кафе"""
    cafe_services = Service.objects.filter(category='cafe', is_active=True)

    context = {
        'services': cafe_services,
        'page_title': 'Кафе',
    }

    return render(request, 'main/cafe.html', context)


def services_children(request):
    """Страница детских услуг"""
    children_services = Service.objects.filter(category='children', is_active=True)

    context = {
        'services': children_services,
        'page_title': 'Детям',
    }

    return render(request, 'main/children.html', context)


def services_hotel(request):
    """Страница отеля"""
    hotel_services = Service.objects.filter(category='hotel', is_active=True)

    context = {
        'services': hotel_services,
        'page_title': 'Отель',
    }

    return render(request, 'main/hotel.html', context)


def price_list(request):
    """Страница прайс-листа"""
    services_by_category = {}
    categories = Service.CATEGORY_CHOICES

    for category_key, category_name in categories:
        services = Service.objects.filter(
            category=category_key,
            is_active=True,
            price__isnull=False
        )
        if services.exists():
            services_by_category[category_name] = services

    baths = BathType.objects.filter(is_available=True)

    context = {
        'services_by_category': services_by_category,
        'baths': baths,
        'page_title': 'Прайс-лист',
    }

    return render(request, 'main/price.html', context)


def actions(request):
    """Страница акций"""
    current_actions = Action.objects.filter(is_active=True)

    # Пагинация
    paginator = Paginator(current_actions, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page_title': 'Акции',
    }

    return render(request, 'main/actions.html', context)


from django.db.models import Case, When
from django.db.models.functions import Lower

def gallery(request):
    """
    Возвращает categories = [
      {"code": "pools", "label": "Термальные бассейны", "cover": <img>, "items": [<img>, ...]},
      ...
    ]
    Без обращения к GalleryImage.CATEGORY_CHOICES.
    """
    # 1) Пробуем достать choices из метаданных поля модели
    choices = {}
    try:
        cat_field = GalleryImage._meta.get_field('category')
        raw_choices = list(getattr(cat_field, 'choices', [])) or []
        choices = dict(raw_choices)  # {'pools': 'Термальные бассейны', ...}
    except Exception:
        pass

    # 2) Если choices пусты — соберём коды из БД и «очеловечим» подписи
    if not choices:
        codes = (
            GalleryImage.objects
            .exclude(category__isnull=True)
            .exclude(category__exact='')
            .values_list('category', flat=True)
            .distinct()
        )

        def prettify(code: str) -> str:
            mapping = {
                'pools': 'Термальные бассейны',
                'baths': 'Бани',
                'hotel': 'Отель',
                'cafe': 'Кафе и Pool Bar',
                'exterior': 'Экстерьер',
                'kids': 'Детям',
                'spa': 'SPA',
            }
            return mapping.get(code, str(code).replace('_', ' ').title())

        choices = {code: prettify(code) for code in codes}

    # 3) Порядок категорий — как в choices (если их нет, будет порядок distinct из БД)
    order = list(choices.keys())

    # 4) Тянем все изображения, сортируем по порядку категорий и внутри по created_at (если есть)
    try:
        images = GalleryImage.objects.all().order_by(
            Case(*[When(category=cat, then=pos) for pos, cat in enumerate(order)], default=len(order)),
            '-created_at'
        )
    except Exception:
        images = GalleryImage.objects.all().order_by(
            Case(*[When(category=cat, then=pos) for pos, cat in enumerate(order)], default=len(order)),
            Lower('title')  # запасной вариант сортировки
        )

    # 5) Группируем
    grouped = {}
    for img in images:
        code = img.category or 'other'
        if code not in grouped:
            grouped[code] = {
                'code': code,
                'label': choices.get(code, getattr(img, 'get_category_display', lambda: code)()),
                'cover': None,
                'items': []
            }
        g = grouped[code]
        g['items'].append(img)
        if g['cover'] is None:
            g['cover'] = img  # первая картинка как обложка

    # 6) Превращаем в список по order; «лишние» категории в конец
    categories = [grouped[c] for c in order if c in grouped]
    for code, data in grouped.items():
        if code not in order:
            categories.append(data)

    return render(request, "main/gallery.html", {"categories": categories})



def contacts(request):
    """Страница контактов"""
    contact_info = Contact.objects.first()
    social_networks = SocialNetwork.objects.filter(is_active=True)

    context = {
        'contact': contact_info,
        'social_networks': social_networks,
        'page_title': 'Контакты',
    }

    return render(request, 'main/contacts.html', context)


def certificates(request):
    """Страница подарочных сертификатов"""
    context = {
        'page_title': 'Подарочные сертификаты',
    }

    return render(request, 'main/certificates.html', context)


def service_detail(request, service_id):
    """Детальная страница услуги"""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    related_services = Service.objects.filter(
        category=service.category,
        is_active=True
    ).exclude(id=service.id)[:3]

    context = {
        'service': service,
        'related_services': related_services,
        'page_title': service.title,
    }

    return render(request, 'main/service_detail.html', context)
