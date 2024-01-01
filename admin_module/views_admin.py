from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User


def add_user(request):
    if request.method == 'POST':
        # Process the form data for POST requests
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_created_by_add_user = True  # Set the flag
            profile.save()
            return redirect('admin_module:user_list')
    else:
        # Render the form for GET requests (and other methods besides POST)
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request, 'admin_module/add_user.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
@staff_member_required
def edit_user(request, user_id):
    # Извлечение пользователя и связанного с ним профиля из базы данных
    try:
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        # Обработка случая, когда пользователь с предоставленным user_id не существует
        return HttpResponse("Пользователь не найден", status=404)

    if request.method == 'POST':
        # Обработка отправки формы для обновления данных пользователя и профиля
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('admin_module:user_list')
    else:
        # Отображение данных пользователя и профиля для редактирования
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'admin_module/edit_user.html', {'user_form': user_form, 'profile_form': profile_form, 'user': user})


@login_required
@staff_member_required
def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_home') 


def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'admin_module/user_list.html', {'users': users})
