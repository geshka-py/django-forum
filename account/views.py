from django.shortcuts import render, redirect
from .forms import NewUserForm, UserEditForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def registration(request):
    message = None
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
        else:
            message = "Form is not valid. Try again."
    form = NewUserForm()
    return render(request, "registration/sign_up.html", context={"registration_form": form, "message": message})


@login_required
def profile(request):
    message = ''
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            message = 'Your profile has been changed'
    form = UserEditForm()
    form['username'].initial = request.user.username
    form['email'].initial = request.user.email
    return render(request, 'registration/profile.html', context={'form': form, 'message': message})
