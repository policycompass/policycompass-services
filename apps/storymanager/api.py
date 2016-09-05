import requests
from django.http.response import HttpResponse
from policycompass_services import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.reverse import reverse
import json
from .models import Story, Chapter, Content
from apps.visualizationsmanager.models import Visualization
from apps.metricsmanager.models import Metric


class Base(APIView):
    def get(self, request):
        result = {
            "Stories": reverse('story-view', request=request),
            "Chapters": reverse('chapter-view', request=request),
            "Contents": reverse('content-view', request=request)
        }
        return Response(result)


class StoryView(generics.ListCreateAPIView):
    model = Story
    serializer_class = StorySerializer
    paginate_by = 10
    paginate_by_param = 'page_size'
    permission_classes = IsAuthenticatedOrReadOnly,

    def pre_save(self, obj):
        obj.creator_path = self.request.user.resource_path

    def get(self, request, *args, **kwargs):
        if len(request._request.GET) is 0:
            stories = Story.objects.all()
            storyList = []
            for s in range(0, len(stories)):
                storyTitle = stories[s].title
                storyChapters = stories[s].chapters
                chapterList = []
                for ch in range(0, len(storyChapters)):
                    chapterList.append(storyChapters[ch].chapter)

                story = {"title":storyTitle, "chapters":chapterList, "issued": stories[s].issued, "modified":stories[s].modified,
                         "creator_path":stories[s].creator_path, "id":stories[s].id,}
                storyList.append(story)
            return Response({"count":len(storyList),"results": storyList})

        self.serializer_class = StorySerializer
        id = request._request.GET['id']
        story = Story.objects.get(pk=id)
        storyChapters = story.chapters
        chapters = []
        for c in range(0, len(storyChapters)):
            chapterId = int(str(storyChapters[c]))
            chapter = Chapter.objects.get(pk=chapterId)
            chapterContents = chapter.contents
            contents = []
            for con in range(0, len(chapterContents)):
                contentId = int(str(chapterContents[con]))
                content = Content.objects.get(pk=contentId)
                contents.append({"type":content.type, "index":content.index, "contentId":content.id})
            chapters.append({"title":chapter.title, "text":chapter.text, "number":chapter.number, "contents":contents})

        storyResult = {"title":story.title, "chapters":chapters, "id":story.id}
        result = {"result": storyResult}

        return Response(result)


    def post(self, request, *args, **kwargs):
        self.serializer_class = UpdateStorySerializer
        json_request = json.loads(request.body.decode('utf-8'))
        title = json_request['title']

        storyList = Story.objects.all()
        for s in range(0, len(storyList)):
            if(title == storyList[s].title):
                result = {"result": 500}
                return Response(result)

        chapters = json_request['chapters']
        chapterIndices = []
        for i in range(0, len(chapters)):
            contents = chapters[i]['contents']
            contentIndices = []
            for j in range(0, len(contents)):
                newContent = Content(type=contents[j]['type'], index=contents[j]['index'])
                newContent.save()
                contentIndices.append(newContent.id)
            newChapter = Chapter(title=chapters[i]['title'], text=chapters[i]['text'], number=chapters[i]['number'], contents=contentIndices)
            newChapter.save()
            chapterIndices.append(newChapter.id)
        newStory = Story(title=title, chapters=chapterIndices)
        newStory.creator_path = self.request.user.resource_path
        newStory.save()

        newStoryJson = {"title":title, "chapters":chapterIndices, "id":newStory.id}

        result = {"result": newStoryJson}

        return Response(result)


    def get_queryset(self):
        queryset = Story.objects.all()
        return queryset


class StoryDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Story
    serializer_class = ExternalStorySerializer
    permission_classes = permissions.IsCreatorOrReadOnly,

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateStorySerializer
        json_request = json.loads(request.body.decode('utf-8'))
        storyId = kwargs.get('pk')
        oldStory = Story.objects.get(id=storyId)
        title = json_request['title']
        chapters = json_request['chapters']
        oldContents = json_request['oldContents']

        chapterIndices = []
        for i in range(0, len(chapters)):
            contents = chapters[i]['contents']
            contentIndices = []
            for j in range(0, len(contents)):
                newContent = Content(type=contents[j]['type'], index=contents[j]['index'])
                newContent.save()
                contentIndices.append(newContent.id)
            newChapter = Chapter(title=chapters[i]['title'], text=chapters[i]['text'], number=chapters[i]['number'], contents=contentIndices)
            newChapter.save()
            print("newChapter " , newChapter.id)
            chapterIndices.append(newChapter.id)

        if len(oldContents) > 0:
            contentList = oldContents
            for l in range(0, len(oldContents)):
                contentId = contentList[l]['contentId']
                co = Content.objects.get(pk=contentId)
                co.delete()

        for k in range(0, len(oldStory.chapters)):
            chapterId = int(str(oldStory.chapters[k]))
            ch = Chapter.objects.get(pk=chapterId)
            ch.delete()

        newStory = Story(title=title, chapters=chapterIndices)
        newStory.creator_path = self.request.user.resource_path
        oldStory.title = title
        oldStory.chapters = chapterIndices
        oldStory.save()
        oldStoryJson = {"title":title, "chapters":chapterIndices, "id":oldStory.id}

        result = {"result": oldStoryJson}

        return Response(result)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        user = request.user.resource_path
        story = Story.objects.get(id=id)

        if story.creator_path == user or request.user.is_god is True:
            for i in range(0, len(story.chapters)):
                chapterId = int(str(story.chapters[i]))
                chapter = Chapter.objects.get(pk=chapterId)
                for j in range(0, len(chapter.contents)):
                    contentId = int(str(chapter.contents[j]))
                    content = Content.objects.get(pk=contentId).delete()
                chapter.delete()
            story.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': "User does not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)

class ChapterView(generics.ListCreateAPIView):
    model = Chapter
    permission_classes = IsAuthenticatedOrReadOnly,
    queryset = Chapter.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    serializer_class = ChapterSerializer

    def pre_save(self, obj):
        obj.creator_path = self.request.user.resource_path


class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Chapter
    serializer_class = ExternalChapterSerializer
    permission_classes = permissions.IsCreatorOrReadOnly,

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateChapterSerializer
        return super(ChapterDetail, self).put(request, args, kwargs)


class ContentView(generics.ListCreateAPIView):
    model = Content
    permission_classes = IsAuthenticatedOrReadOnly,
    queryset = Content.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    serializer_class = ContentSerializer

    def pre_save(self, obj):
        obj.creator_path = self.request.user.resource_path


class ContentDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Content
    serializer_class = ExternalContentSerializer
    permission_classes = permissions.IsCreatorOrReadOnly,

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateContentSerializer
        return super(ContentDetail, self).put(request, args, kwargs)