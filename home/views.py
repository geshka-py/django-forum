from django.shortcuts import render, redirect
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .forms import PublicationForm, RateIt, CommentForm

from .models import Group, Publication, Rate, Comment


def home(request):
    publications = Publication.objects.all()
    groups = Group.objects.all()
    return render(request, 'home/home.html', {'publications': publications, 'groups': groups})


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
    rating = rating / len(ratings)
    data['rating'] = rating
    if request.method == "POST":
        exists = Rate.objects.get(publication=publication, user=request.user)
        rate_form = RateIt(request.POST)
        if rate_form.is_valid():
            if exists:
                exists.delete()
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


# class UserPublicationRelationView(UpdateModelMixin, GenericViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = UserPublicationRelation.objects.all()
#     serializer_class = UserPublicationSerializer
#     lookup_field = 'publication'
#
#     def get_object(self):
#         obj = UserPublicationRelation.objects.get_or_create(user=self.request.user,
#                                                             publication_id=self.kwargs['publication'])
#
#         return obj
