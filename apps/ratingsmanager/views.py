from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import *


class RatingsListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    serializer_class = RatingSerializer


class RatingDetailView(generics.GenericAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_rating(self, identifier):
        try:
            return Rating.objects.get(identifier=identifier)
        except Rating.DoesNotExist:
            raise Http404

    def get(self, request, identifier, format=None):
        rating = self.get_rating(identifier)
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    def post(self, request, identifier, format=None):
        vote = VoteSerializer(data=request.DATA)
        if vote.is_valid():
            try:
                rating = self.get_rating(identifier)
            except:
                rating = Rating(identifier=identifier)
                rating.save()
            user_identifier = self.request.user.resource_path
            try:
                ratingVote = RatingVote.objects.get(rating=rating,
                                                    user_identifier=user_identifier)
            except:
                ratingVote = RatingVote(rating=rating,
                                        user_identifier=user_identifier)
            ratingVote.score = vote.data.get('score')
            ratingVote.save()
            rating.calculate()
            return Response(RatingSerializer(rating).data)
        return Response(vote.errors, status=400)


class Base(APIView):
    def get(self, request, format=None):
        result = {
            "Ratings": reverse('ratings-list', request=request)
        }

        return Response(result)
