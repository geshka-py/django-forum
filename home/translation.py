from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Group)
class GroupTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Publication)
class PublicationTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
