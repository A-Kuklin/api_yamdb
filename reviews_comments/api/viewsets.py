from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from categories_genres_titles.models import Title
from reviews_comments.models import Review

from .permissions import IsAdmin, IsModerator, IsOwnerOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly | IsModerator | IsAdmin]

    pagination_class = PageNumberPagination

    def get_title(self):
        """Getting title object by the title id"""
        return get_object_or_404(
            Title,
            id=self.request.parser_context['kwargs'].get('title_id')
        )

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        if Review.objects.filter(
                author=self.request.user,
                title=self.get_title()
        ).exists():
            raise ValidationError('Вы уже оставили отзыв на это произведение')
        serializer.save(
            title=self.get_title(),
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly | IsModerator | IsAdmin]
    pagination_class = PageNumberPagination

    def get_review(self):
        """Getting review object by the review id"""
        return get_object_or_404(
            Review,
            id=self.request.parser_context['kwargs'].get('review_id')
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=self.get_review(),
            author=self.request.user
        )
