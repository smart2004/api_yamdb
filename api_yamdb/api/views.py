
from django.shortcuts import get_object_or_404, render
import string
import random
from django.db.models import Avg
from reviews.models import Category, Genre, Title, Review
from api.serializers import CategorySerializer, GenreSerializer
from api.mixins import ListCreateDestroyViewSet
from api.serializers import(CategorySerializer, GenreSerializer,
                            TitleSerializer, ReadOnlyTitleSerializer,
                            ReviewSerializer, CommentSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from api.filters import TitlesFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly)
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status  # статусы
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, action  # декоратор
from rest_framework.permissions import AllowAny, IsAuthenticated  # разрешения
from rest_framework.response import Response
from django.core.mail import send_mail  # отправка сообщений
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer
# from .serializers import AboutUserSerializer, UserMeSerializer
from .serializers import UserSerializer, UserEditSerializer
from reviews.validators import validate_username, validate_confirmation_code

class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
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
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        letters = string.ascii_letters  # upper and lower
        confirmation_code = ''.join(
            random.sample(
                letters,
                User._meta.get_field('confirmation_code').max_length
            )
        )
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            user = User.objects.get(
                username=request.data.get('username')
            )
            send_mail(
                'Your API code',          # topic
                confirmation_code,        # text
                'YamDB_API@yandex.ru',    # from
                [request.data['email']],  # to
                fail_silently=True,       # log error
            )
            user.confirmation_code = confirmation_code
            user.save()
            return Response(request.data, status=status.HTTP_200_OK)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        send_mail(
                'Your API code',          # topic
                confirmation_code,        # text
                'YamDB_API@yandex.ru',    # from
                [request.data['email']],  # to
                fail_silently=True,       # log error
            )
        serializer.save(confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    if request.method == 'POST':
        serializer = TokenSerializer(data=request.data)
        # get_object_or_404(User, username=request.data.get('username'))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(User, username=request.data.get('username'))
        if not validate_confirmation_code(request.data['confirmation_code']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(
            User,
            username=request.data['username'],
            confirmation_code=request.data['confirmation_code']
        )
        access = AccessToken.for_user(user)
        return Response(
            {'token': str(access)},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
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
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
