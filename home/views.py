from django.db.models import Q
from django.shortcuts import render, redirect


from .forms import PublicationForm, RateIt, CommentForm

from .models import Group, Publication, Rate, Comment, Tag, Like


def home(request, ordering='-published'):
    groups = Group.objects.all()
    tags = Tag.objects.all()
    publications = Publication.objects.order_by(ordering)
    return render(request, 'home/home.html', context={
        'publications': publications,
        'groups': groups,
        'tags': tags,
        'ordering': ordering
    })


def like_it(request, pid):
    publication = Publication.objects.get(id=pid)
    try:
        like = Like.objects.get(publication=publication, user=request.user)
        like.delete()
        publication.liked -= 1
        publication.save()
    except Like.DoesNotExist:
        like = Like.objects.create(publication=publication, user=request.user, value=True)
        publication.liked += 1
        publication.save()
    return redirect(f'/home/publication/{pid}')


def single_publication(request, pid):
    publication = Publication.objects.get(id=pid)
    comments = Comment.objects.filter(publication=publication)
    rate_form = rate(request, pid)
    comment_form = comment(request, pid)
    if rate_form == 'success' or comment_form == 'success':
        return redirect(f"/publication/{pid}")
    return render(request, 'home/publication.html',
                  context={
                            'publication': publication,
                            'comments': comments,
                            'rate_form': rate_form,
                            'comment_form': comment_form
                          })


def rate(request, pid):
    publication = Publication.objects.get(id=pid)
    if request.method == 'POST':
        form = RateIt(request.POST)
        if form.is_valid():
            try:

                publication.rating -= Rate.objects.get(publication=publication, user=request.user).rate / ((len(Rate.objects.filter(publication=publication)) - 1) or 1)
                publication.save()
                Rate.objects.get(publication=publication, user=request.user).delete()
            except Rate.DoesNotExist:
                pass
            form = form.save(commit=False)
            form.user = request.user
            form.publication = publication
            form.save()
            publication.rating += ((form.rate + 1) / len(Rate.objects.filter(publication=publication)))
            publication.save()
            return 'success'
    form = RateIt()
    return form


def comment(request, pid):
    publication = Publication.objects.get(id=pid)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.publication = publication
            form.save()
            return 'success'
    form = CommentForm()
    return form


def create_publication(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST)
        if form.is_valid():
            new_publication = form.save(commit=False)
            new_publication.author = request.user
            new_publication.save()
            new_publication.tags.set(request.POST.get('tags'))
            return redirect('/')
    else:
        form = PublicationForm()
    return render(request, 'home/create_publication.html', context={'form': form})


def tag_search(request, slug):
    tag = Tag.objects.get(slug=slug)
    publications = Publication.objects.filter(tags=tag)
    return render(request, 'home/tag_search.html', context={'tag': tag,
                                                            'publications': publications,
                                                            'searched': tag.tag_name})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        if searched:
            comments = Comment.objects.filter(comment__contains=searched)
            publication_list = [i.publication.id for i in comments]

            publications = Publication.objects.filter(Q(title__contains=searched)
                                                      | Q(content__contains=searched)
                                                      | Q(id__in=publication_list)
                                                      | Q(tags=tags(searched))).distinct()
        else:
            return redirect('/home/')
    return render(request, 'home/search_results.html', context={'publications': publications,
                                                                'searched': searched})


def tags(searched):
    try:
        return Tag.objects.get(tag_name=searched)
    except Tag.DoesNotExist:
        return None


def tags_list(request):
    return render(request, 'home/tag_cloud.html')


def tag_detail(request, slug):
    tag = Tag.objects.get(slug=slug)
    return render(request, 'home/tag_detail.html', context={'tag': tag})


def group_view(request, slug):
    groups = Group.objects.all()
    group = groups.get(slug=slug)
    publications = Publication.objects.filter(group=group)
    return render(request, 'home/home.html', context={
        'group': group,
        'publications': publications,
        'groups': groups
    })


def file_upload_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        Publication.objects.create(upload=file)
        return
