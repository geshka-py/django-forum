from django.shortcuts import render, redirect
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .forms import UserPublicationRelationForm
from .models import UserPublicationRelation

from .models import Group, Publication
from .serializers import UserPublicationSerializer


def home(request):
    publications = Publication.objects.all()
    groups = Group.objects.all()
    for i in publications:
        i.content = i.content[:256] + '....'
    return render(request, 'home/home.html', {'publications': publications, 'groups': groups})


def single_publication(request, pid):
    publication = Publication.objects.get(id=pid)
    if request.method == "POST":
        form = UserPublicationRelationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.publication = publication
            form.save()
            return redirect("/", context={'form': form})
    else:
        form = UserPublicationRelationForm()
    reviews = UserPublicationRelation.objects.filter(publication=publication)
    return render(request, 'home/publication.html', context={'publication': publication,
                                                             'form': form,
                                                             'reviews': reviews})


class UserPublicationRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPublicationRelation.objects.all()
    serializer_class = UserPublicationSerializer
    lookup_field = 'publication'

    def get_object(self):
        obj = UserPublicationRelation.objects.get_or_create(user=self.request.user,
                                                            publication_id=self.kwargs['publication'])

        return obj
