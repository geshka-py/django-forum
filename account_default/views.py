from django.shortcuts import render, redirect
from .forms import NewUserForm, UserEditForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.models import Publication


def registration(request):
    message = None
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("signup_res")
        else:
            message = "Form is not valid. Try again."
    form = NewUserForm()
    return render(request, "registration/sign_up.html", context={"registration_form": form, "message": message})


def signup_res(request):
    return render(request, "registration/sign_up_res.html")


@login_required
def profile(request):
    publications = Publication.objects.filter(author=request.user)
    message = ''
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            message = 'Your profile has been changed'
    form = UserEditForm()
    form['username'].initial = request.user.username
    form['email'].initial = request.user.email
    return render(request, 'registration/profile.html', context={'form': form,
                                                                 'message': message,
                                                                 'publications': publications
                                                                 })


def delete_publication(request, pid):
    publication = Publication.objects.get(id=pid)
    publication.delete()
    return render(request, 'home/home.html')