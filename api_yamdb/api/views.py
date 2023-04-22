import uuid

from api.filters import TitlesFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReadOnlyTitleSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleSerializer, TokenSerializer, UserSerializer)
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User


class CategoryViewSet(ListCreateDestroyViewSet):
    """Обрабатывает операции чтения, создания и удаления категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    """Обрабатывает операции чтения, создания и удаления жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатывает операции чтения, создания,
    изменения и удаления произведений"""
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает операции чтения, создания,
    изменения и удаления отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает операции чтения, создания,
    изменения и удаления комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Обрабатывавает регистраницию новых пользователей"""
    serializer = SignUpSerializer(data=request.data)
    confirmation_code = uuid.uuid4().hex
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        **serializer.validated_data
    )
    send_mail(
        'Your API code',
        confirmation_code,
        'YamDB_API@yandex.ru',
        [request.data.get('email')],
        fail_silently=True,
    )
    user.confirmation_code = confirmation_code
    user.save()
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Получение токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.get(
        **serializer.validated_data
    )
    access = AccessToken.for_user(user)
    return Response(
        {'token': str(access)},
        status=status.HTTP_200_OK
    )


class UserViewSet(viewsets.ModelViewSet):
    """Обрабатывает операции чтения, создания,
    изменения и удаления пользователей"""
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    permission_classes = (IsAdmin,)

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
