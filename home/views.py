from django.db.models import Q
from django.shortcuts import render, redirect
import re


from .forms import PublicationForm, RateIt, CommentForm

from .models import Group, Publication, Rate, Comment, Tag


def home(request):
    publications = Publication.objects.all()
    groups = Group.objects.all()
    tags = Tag.objects.all()
    return render(request, 'home/home.html', {'publications': publications,
                                              'groups': groups,
                                              'tags': tags})


def single_publication(request, pid):
    rating = 0
    data = dict()
    publication = Publication.objects.get(id=pid)
    ratings = Rate.objects.filter(publication=publication)
    comments = Comment.objects.filter(publication=publication)
    data['publication'] = publication
    data['comments'] = comments
    for i in ratings:
        rating += i.rate
    rating = rating / (len(ratings) or 1)
    data['rating'] = rating
    if request.method == "POST":
        rate_form = RateIt(request.POST)
        if rate_form.is_valid():
            try:
                Rate.objects.get(publication=publication, user=request.user).delete()
            except Rate.DoesNotExist:
                pass
            rate_form = rate_form.save(commit=False)
            rate_form.user = request.user
            rate_form.publication = publication
            rate_form.save()
            data['rate_form'] = rate_form
            return redirect(f"/publication/{pid}")
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.publication = publication
            comment_form.user = request.user
            comment_form.save()
            data['comment_form'] = comment_form
            return redirect(f"/publication/{pid}")
    else:
        data['rate_form'] = RateIt()
        data['comment_form'] = CommentForm()
    return render(request, 'home/publication.html', context=data)


def create_publication(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('/')
    else:
        form = PublicationForm()
    return render(request, 'home/create_publication.html', context={'form': form})


def tag_search(request, tid):
    tag = Tag.objects.get(id=tid)
    publications = Publication.objects.all()
    tag_publications = []
    for publication in publications:
        if tag in publication.tags.all():
            tag_publications.append(publication)
    return render(request, 'home/tag_search.html', context={'tag': tag, 'publications': tag_publications})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        comments = Comment.objects.filter(comment__contains=searched)
        publication_list = [i.publication.id for i in comments]

        publications = Publication.objects.filter(Q(title__contains=searched)
                                                  | Q(content__contains=searched)
                                                  | Q(id__in=publication_list))
    return render(request, 'home/search_results.html', context={'publications': publications,
                                                                'searched': searched})


def tag_cloud(request):
    tags = Tag.objects.all()
    return render(request, 'home/tag_cloud.html', context={'tags': tags})


