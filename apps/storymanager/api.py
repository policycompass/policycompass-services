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
        if len(request._request.GET) is 0 or ('page' in request._request.GET) is True:
            stories = Story.objects.all()
            storyList = []
            for s in range(0, len(stories)):
                storyTitle = stories[s].title
                storyChapters = stories[s].chapters
                chapters = []
                for c in range(0, len(storyChapters)):
                    chapterId = int(str(storyChapters[c]))
                    chapter = Chapter.objects.get(pk=chapterId)
                    chapterContents = chapter.contents
                    contents = []
                    for con in range(0, len(chapterContents)):
                        contentId = int(str(chapterContents[con]))
                        content = Content.objects.get(pk=contentId)
                        contents.append({"type": content.type, "index": content.index, "contentId": content.id})
                    chapters.append({"title": chapter.title, "text": chapter.text, "number": chapter.number, "contents": contents})
                story = {"title": storyTitle, "chapters": chapters, "issued": stories[s].date_created, "modified": stories[s].date_modified,
                         "creator_path": stories[s].creator_path, "id": stories[s].id, "is_draft": stories[s].is_draft}
                storyList.append(story)
            response = {"count": len(storyList), "results": storyList, "next": None}

            return Response(response)

        self.serializer_class = StorySerializer
        id = request._request.GET['id']
        try:
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
                    contents.append({"type": content.type, "index": content.index, "contentId": content.id})
                chapters.append({"title": chapter.title, "text": chapter.text, "number": chapter.number, "contents": contents})

            storyResult = {"title": story.title, "chapters": chapters, "id": story.id, "creator_path": story.creator_path, "is_draft": story.is_draft, "issued": story.date_created, "modified": story.date_modified}

            return Response(storyResult)
        except:
            errorDict = {"result": 500}
            errorString = str(errorDict).replace("'", '"')
            errorJson = json.loads(errorString)
            return Response(errorJson)

    def post(self, request, *args, **kwargs):
        self.serializer_class = UpdateStorySerializer
        json_request = json.loads(request.body.decode('utf-8'))
        title = json_request['title']

        storyList = Story.objects.all()
        for s in range(0, len(storyList)):
            if(title == storyList[s].title):
                result = {"result": 500}
                return Response(result)
        is_draft = json_request['is_draft']
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
        newStory = Story(title=title, chapters=chapterIndices, is_draft=is_draft)
        newStory.creator_path = self.request.user.resource_path
        newStory.save()

        newStoryJson = {"title": title, "chapters": chapterIndices, "id": newStory.id, "is_draft": is_draft}

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
        is_draft = json_request['is_draft']

        user = request.user.resource_path

        if oldStory.creator_path == user or request.user.is_god is True:
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

            newStory = Story(title=title, chapters=chapterIndices, is_draft=is_draft)
            newStory.creator_path = self.request.user.resource_path
            oldStory.title = title
            oldStory.chapters = chapterIndices
            oldStory.is_draft = is_draft
            oldStory.save()
            oldStoryJson = {"title": title, "chapters": chapterIndices, "id": oldStory.id, "is_draft": is_draft}

            result = {"result": oldStoryJson}

            return Response(result)
        else:
            return Response({'error': "User does not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)

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
                    content = Content.objects.get(pk=contentId)
                    content.delete()
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
