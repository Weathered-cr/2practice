from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Application, Category
from .forms import ApplicationForm, CategoryForm, UpdateStatusForm, CustomUserCreationForm


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
    applications = Application.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'accounts/profile.html', {"applications": applications})


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

# Смена статуса заявки
@login_required
def update_status(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)

    # Проверяем, что можно менять только новые заявки
    if application.status != "new":
        messages.error(request, "Изменять можно только заявки в статусе 'Новая'.")
        return redirect("view_applications")  # можно redirect на профиль или список заявок

    if request.method == "POST":
        # Обрабатываем POST вручную для надёжного сохранения
        new_status = request.POST.get("status")
        comment = request.POST.get("comment")
        design_image = request.FILES.get("design_image")

        if new_status:
            application.status = new_status
        if comment:
            application.comment = comment
        if design_image:
            application.design_image = design_image

        application.save()
        messages.success(request, "Статус заявки обновлён.")
        return redirect("view_applications")

    else:
        # GET-запрос — подгружаем форму для отображения
        form = UpdateStatusForm(instance=application)

    return render(
        request,
        "applications/update_status.html",
        {"form": form, "application": application}
    )


# Проверка на администратора
def is_admin(user):
    return user.is_superuser


# Управление категориями
@user_passes_test(is_admin)
def manage_categories(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Категория добавлена.")
            return redirect("manage_categories")
    else:
        form = CategoryForm()
    return render(request, "applications/manage_categories.html", {"categories": categories, "form": form})


@user_passes_test(is_admin)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()  # автоматически удалит все заявки этой категории
        messages.success(request, "Категория и её заявки удалены.")
        return redirect("manage_categories")
    return render(request, "applications/delete_category.html", {"category": category})


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
