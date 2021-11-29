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


def like_it(request, slug):
    publication = Publication.objects.get(slug=slug)
    try:
        like = Like.objects.get(publication=publication, user=request.user)
        like.delete()
        publication.liked -= 1
        publication.save()
    except Like.DoesNotExist:
        like = Like.objects.create(publication=publication, user=request.user, value=True)
        publication.liked += 1
        publication.save()
    return redirect(f'/home/publication/{slug}')


def single_publication(request, slug):
    publication = Publication.objects.get(slug=slug)
    comments = Comment.objects.filter(publication=publication)
    rate_form = rate(request, slug)
    comment_form = comment(request, slug)
    if rate_form == 'success' or comment_form == 'success':
        return redirect(f"/publication/{slug}")
    return render(request, 'home/publication.html',
                  context={
                            'publication': publication,
                            'comments': comments,
                            'rate_form': rate_form,
                            'comment_form': comment_form
                          })


def rate(request, slug):
    publication = Publication.objects.get(slug=slug)
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


def comment(request, slug):
    publication = Publication.objects.get(slug=slug)
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
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            form.tags.set(request.POST.get('tags'))
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
        comments = Comment.objects.filter(comment__contains=searched)
        publication_list = [i.publication.id for i in comments]

        publications = Publication.objects.filter(Q(title__contains=searched)
                                                  | Q(content__contains=searched)
                                                  | Q(id__in=publication_list))
    return render(request, 'home/search_results.html', context={'publications': publications,
                                                                'searched': searched})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    return render(request, 'blog/tag_detail.html', context={'tag': tag})



