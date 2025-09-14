from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView

from .forms import CustomUserCreationForm, ApplicationForm
from .models import Application


# --- Аккаунты ---
def home(request):
    # Контекст: последние 4 выполненные и счётчик "в работе"
    completed_applications = Application.objects.filter(status='completed').order_by('-timestamp')[:4]
    in_progress_count = Application.objects.filter(status='in_progress').count()
    return render(request, 'accounts/home.html', {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Войдите в систему.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


class RulesView(TemplateView):
    template_name = 'accounts/rules.html'


# --- Заявки ---
@login_required
def create_application(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, "Заявка успешно создана.")
            return redirect('view_applications')
        else:
            messages.error(request, "Ошибка при создании заявки. Проверьте поля.")
    else:
        form = ApplicationForm()
    return render(request, 'applications/create_application.html', {'form': form})


@login_required
def view_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-timestamp')

    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'applications/view_applications.html', {'applications': applications})


@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)

    if request.method == "POST":
        if application.status not in ['in_progress', 'completed']:
            application.delete()
            messages.success(request, "Заявка успешно удалена.")
            return redirect('view_applications')
        else:
            messages.error(request, "Невозможно удалить заявку с изменённым статусом.")
            return redirect('view_applications')

    return render(request, 'applications/confirm_delete.html', {'application': application})
