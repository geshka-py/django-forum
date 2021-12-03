from home.models import Tag


def tag(request):
    return {
        'tags': Tag.objects.all()
    }
