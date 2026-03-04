from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Service, BathType, PoolType, GalleryImage,
    SliderImage, Contact, SocialNetwork, Action,
    Booking, ContactRequest, Newsletter
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['category', 'order']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'category', 'short_description', 'description')
        }),
        ('Изображение и цена', {
            'fields': ('image', 'price')
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(BathType)
class BathTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'price_per_hour', 'is_available']
    list_filter = ['is_available', 'capacity']
    search_fields = ['name', 'description']
    list_editable = ['is_available']


@admin.register(PoolType)
class PoolTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'temperature', 'depth', 'is_outdoor']
    list_filter = ['is_outdoor']
    search_fields = ['name', 'description']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_preview', 'order', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order']
    ordering = ['order', '-created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = "Превью"


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'image_preview', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']
    list_editable = ['is_active', 'order']
    ordering = ['order']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="40" style="object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = "Превью"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'work_hours']

    def has_add_permission(self, request):
        # Ограничиваем создание только одной записи контактов
        if Contact.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление контактов
        return False


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'icon_class', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    ordering = ['order']


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percent', 'start_date', 'end_date', 'is_active', 'is_current_display']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    ordering = ['-start_date']

    def is_current_display(self, obj):
        return obj.is_current
    is_current_display.short_description = "Актуальна"
    is_current_display.boolean = True


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service_type', 'date', 'time', 'guests_count', 'status', 'total_price_display', 'created_at']
    list_filter = ['service_type', 'status', 'date', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_editable = ['status']
    ordering = ['-created_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Детали бронирования', {
            'fields': ('service_type', 'service', 'bath_type', 'date', 'time', 'guests_count', 'duration_hours')
        }),
        ('Дополнительно', {
            'fields': ('comment', 'status')
        }),
    )

    def total_price_display(self, obj):
        total = obj.total_price
        if total > 0:
            return f"{total:,.0f} ₽"
        return "Не указана"
    total_price_display.short_description = "Стоимость"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('service', 'bath_type')


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'request_type', 'status', 'created_at', 'is_responded']
    list_filter = ['request_type', 'status', 'created_at']
    search_fields = ['name', 'phone', 'email', 'subject']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Запрос', {
            'fields': ('request_type', 'subject', 'message', 'preferred_time')
        }),
        ('Обработка', {
            'fields': ('status', 'response')
        }),
        ('Служебная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def is_responded(self, obj):
        return bool(obj.response)
    is_responded.short_description = "Отвечено"
    is_responded.boolean = True

    actions = ['mark_as_completed', 'mark_as_in_progress']

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'Обновлено {updated} заявок на статус "Выполнена"')
    mark_as_completed.short_description = "Отметить как выполненные"

    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'Обновлено {updated} заявок на статус "В обработке"')
    mark_as_in_progress.short_description = "Отметить как в обработке"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    ordering = ['-created_at']

    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано {updated} подписок')
    activate_subscriptions.short_description = "Активировать подписки"

    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано {updated} подписок')
    deactivate_subscriptions.short_description = "Деактивировать подписки"


# Настройка административной панели
admin.site.site_header = "Админ-панель VODA Термы"
admin.site.site_title = "VODA Термы"
admin.site.index_title = "Управление сайтом термального комплекса"
