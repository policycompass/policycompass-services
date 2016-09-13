from django.contrib import admin
from .models import Story, Chapter, Content, ChapterInContent, StoryInChapter

admin.site.register(Story)
admin.site.register(Chapter)
admin.site.register(Content)
admin.site.register(ChapterInContent)
admin.site.register(StoryInChapter)
