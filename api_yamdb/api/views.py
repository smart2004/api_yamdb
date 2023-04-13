# from django.shortcuts import render
# from reviews.models import Category
# from api.serializers import CategorySerializer
import string
import random
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail  # отправка сообщений
from rest_framework import status  # статусы
from rest_framework.decorators import api_view, permission_classes  # декоратор
from rest_framework.permissions import AllowAny, IsAuthenticated  # разрешения
from rest_framework.response import Response
from users.models import User
from .serializers import SignUpSerializer, TokenSerializer
# from rest_framework import viewsets(ListCreateDestroyViewSet)


# class CategoryViewSet(ListCreateDestroyViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     search_fields = ('name',)
#     lookup_field = 'slug'


# class GenreViewSet(ListCreateDestroyViewSet):
#     pass


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        User.objects.all().delete()
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
            if User.objects.filter(
                username=request.data['username'],
                confirmation_code=request.data['confirmation_code']
            ).exists():
                access = AccessToken.for_user(request.user)
                return Response(
                    {'token': str(access)},
                    status=status.HTTP_200_OK
                )
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test(request):
    if request.method == 'GET':
        return Response({'message': 'Only token, good work'})
