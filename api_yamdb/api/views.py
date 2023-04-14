import string
import random
from django.shortcuts import render
from django.db.models import Avg
from reviews.models import Category, Genre, Title
from api.serializers import CategorySerializer, GenreSerializer
from api.mixins import ListCreateDestroyViewSet
from api.serializers import(CategorySerializer, GenreSerializer,
                            TitleSerializer, ReadOnlyTitleSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from api.filters import TitlesFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly)
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status  # статусы
from rest_framework.decorators import api_view, permission_classes  # декоратор
from rest_framework.permissions import AllowAny, IsAuthenticated  # разрешения
from rest_framework.response import Response
from django.core.mail import send_mail  # отправка сообщений
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import SignUpSerializer, TokenSerializer


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
        
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            letters = string.ascii_letters  # upper and lower
            confirmation_code = ''.join(
                random.sample(
                    letters,
                    User._meta.get_field('confirmation_code').max_length
                )
            )
            send_mail(
                'Your API code',          # topic
                confirmation_code,        # text
                'YamDB_API@yandex.ru',    # from
                [request.data['email']],  # to
                fail_silently=True,       # log error
            )
            serializer.save(confirmation_code=confirmation_code)
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    if request.method == 'POST':
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            queryset = User.objects.filter(
                username=request.data['username'],
                confirmation_code=request.data['confirmation_code']
            )
            user = get_object_or_404(queryset)
            access = AccessToken.for_user(user)
            return Response(
                {'token': str(access)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)