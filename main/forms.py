from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Booking, ContactRequest, Newsletter, BathType


class BookingForm(forms.ModelForm):
    """Форма для бронирования услуг"""

    class Meta:
        model = Booking
        fields = [
            'service_type', 'name', 'phone', 'email',
            'date', 'time', 'guests_count', 'duration_hours', 'comment'
        ]
        widgets = {
            'service_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67',
                'required': True,
                'pattern': r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'guests_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20,
                'value': 2
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 8,
                'value': 2
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Дополнительные пожелания...',
                'rows': 3
            }),
        }

    def clean_date(self):
        """Валидация даты бронирования"""
        booking_date = self.cleaned_data.get('date')
        if booking_date:
            if booking_date < date.today():
                raise ValidationError('Дата бронирования не может быть в прошлом')
            if booking_date > date.today() + timedelta(days=90):
                raise ValidationError('Бронирование возможно не более чем на 90 дней вперед')
        return booking_date

    def clean_phone(self):
        """Валидация номера телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Удаляем все символы кроме цифр и +
            cleaned_phone = ''.join(char for char in phone if char.isdigit() or char == '+')
            if not cleaned_phone.startswith(('+7', '8')):
                raise ValidationError('Номер телефона должен начинаться с +7 или 8')
            if len(cleaned_phone.replace('+', '')) != 11:
                raise ValidationError('Номер телефона должен содержать 11 цифр')
        return phone


class CafeBookingForm(BookingForm):
    """Специализированная форма для бронирования столика в кафе"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].initial = 'cafe'
        self.fields['service_type'].widget = forms.HiddenInput()
        self.fields['duration_hours'].initial = 2
        self.fields['duration_hours'].widget.attrs.update({'max': 4})


class BathBookingForm(BookingForm):
    """Специализированная форма для бронирования бани"""

    bath_type = forms.ModelChoiceField(
        queryset=BathType.objects.filter(is_available=True),
        empty_label="Выберите тип бани",
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        label='Тип бани'
    )

    class Meta(BookingForm.Meta):
        fields = BookingForm.Meta.fields + ['bath_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].initial = 'bath'
        self.fields['service_type'].widget = forms.HiddenInput()
        self.fields['duration_hours'].initial = 3
        self.fields['duration_hours'].widget.attrs.update({'min': 2, 'max': 8})

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.bath_type = self.cleaned_data.get('bath_type')
        if commit:
            instance.save()
        return instance


class ContactRequestForm(forms.ModelForm):
    """Форма для заявок обратной связи"""

    class Meta:
        model = ContactRequest
        fields = ['request_type', 'name', 'phone', 'email', 'subject', 'message', 'preferred_time']
        widgets = {
            'request_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема обращения'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше сообщение...',
                'rows': 4
            }),
            'preferred_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: с 10:00 до 18:00'
            }),
        }

    def clean_phone(self):
        """Валидация номера телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            cleaned_phone = ''.join(char for char in phone if char.isdigit() or char == '+')
            if not cleaned_phone.startswith(('+7', '8')):
                raise ValidationError('Номер телефона должен начинаться с +7 или 8')
            if len(cleaned_phone.replace('+', '')) != 11:
                raise ValidationError('Номер телефона должен содержать 11 цифр')
        return phone


class CallbackRequestForm(forms.ModelForm):
    """Упрощенная форма для заказа звонка"""

    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'preferred_time']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67',
                'required': True
            }),
            'preferred_time': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Выберите удобное время'),
                ('morning', 'Утром (9:00 - 12:00)'),
                ('afternoon', 'Днем (12:00 - 17:00)'),
                ('evening', 'Вечером (17:00 - 20:00)'),
                ('anytime', 'В любое время'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'] = forms.CharField(
            initial='callback',
            widget=forms.HiddenInput()
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.request_type = 'callback'
        instance.subject = 'Заказ звонка'
        instance.message = f'Просьба перезвонить в удобное время: {self.cleaned_data.get("preferred_time", "В любое время")}'
        if commit:
            instance.save()
        return instance

    def clean_phone(self):
        """Валидация номера телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            cleaned_phone = ''.join(char for char in phone if char.isdigit() or char == '+')
            if not cleaned_phone.startswith(('+7', '8')):
                raise ValidationError('Номер телефона должен начинаться с +7 или 8')
            if len(cleaned_phone.replace('+', '')) != 11:
                raise ValidationError('Номер телефона должен содержать 11 цифр')
        return phone


class NewsletterForm(forms.ModelForm):
    """Форма для подписки на новости"""

    class Meta:
        model = Newsletter
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш email',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя (необязательно)'
            }),
        }

    def clean_email(self):
        """Валидация email на уникальность"""
        email = self.cleaned_data.get('email')
        if email and Newsletter.objects.filter(email=email, is_active=True).exists():
            raise ValidationError('Этот email уже подписан на новости')
        return email


class QuickBookingForm(forms.Form):
    """Быстрая форма бронирования для модальных окон"""

    service_type = forms.ChoiceField(
        choices=Booking.SERVICE_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67'
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    guests_count = forms.IntegerField(
        initial=2,
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    def clean_date(self):
        """Валидация даты"""
        booking_date = self.cleaned_data.get('date')
        if booking_date and booking_date < date.today():
            raise ValidationError('Дата не может быть в прошлом')
        return booking_date

    def clean_phone(self):
        """Валидация телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            cleaned_phone = ''.join(char for char in phone if char.isdigit() or char == '+')
            if not cleaned_phone.startswith(('+7', '8')):
                raise ValidationError('Номер должен начинаться с +7 или 8')
        return phone
