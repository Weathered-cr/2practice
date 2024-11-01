from django.db import models
from django import forms
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User


# Модель заявки
class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')


# Форма заявки
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo.size > 2 * 1024 * 1024:  # 2MB
            raise forms.ValidationError("Размер фото не должен превышать 2 МБ.")
        return photo


# Создание заявки
def create_application(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, "Заявка успешно создана.")
            return redirect(reverse('view_applications'))
        else:
            messages.error(request, "Ошибка при создании заявки. Проверьте все поля.")
    else:
        form = ApplicationForm()
    return render(request, 'create_application.html', {'form': form})


# Удаление заявки
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)

    if request.method == "POST":
        if application.status not in ['in_progress', 'completed']:
            application.delete()
            messages.success(request, "Заявка успешно удалена.")
            return redirect(reverse('view_applications'))
        else:
            messages.error(request, "Невозможно удалить заявку с измененным статусом.")
    return render(request, 'confirm_delete.html', {'application': application})


# Просмотр своих заявок
def view_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-timestamp')

    # Фильтрация по статусу
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'view_applications.html', {'applications': applications})


# Главная страница
def home(request):
    completed_applications = Application.objects.filter(status='completed').order_by('-timestamp')[:4]
    in_progress_count = Application.objects.filter(status='in_progress').count()

    return render(request, 'home.html', {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    })