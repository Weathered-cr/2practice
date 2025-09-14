from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, Category


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Размер фото не должен превышать 2 МБ.")
        return photo


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'admin_comment', 'design']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        comment = cleaned_data.get("admin_comment")
        design = cleaned_data.get("design")

        if status == "in_progress" and not comment:
            raise forms.ValidationError("Для статуса 'Принято в работу' нужно добавить комментарий.")
        if status == "completed" and not design:
            raise forms.ValidationError("Для статуса 'Выполнено' нужно прикрепить дизайн.")
        return cleaned_data
