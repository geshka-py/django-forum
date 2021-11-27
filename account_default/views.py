from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .forms import NewUserForm, UserEditForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.models import Publication
from home.forms import PublicationForm


def registration(request):
    message = None
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
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
    try:
        publication = Publication.objects.get(id=pid)
        publication.delete()
        return redirect("/account_default/profile")
    except Publication.DoesNotExist:
        return HttpResponseNotFound("<h2>Publication not found</h2>")


def edit_publication(request, pid):
    try:
        publication = Publication.objects.get(id=pid)
        if request.method == "POST":
            publication.title = request.POST.get('title')
            publication.content = request.POST.get('content')
            publication.tags.set(request.POST.get('tags'))
            publication.save()
            return redirect('/account_default/profile')
        edit_form = PublicationForm(instance=publication)
        return render(request, 'home/create_publication.html', context={'form': edit_form,
                                                                        'publication': publication})
    except Publication.DoesNotExist:
        return HttpResponseNotFound("<h2>Publication not found</h2>")
