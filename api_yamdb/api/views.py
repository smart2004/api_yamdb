# from django.shortcuts import render
# from reviews.models import Category
# from api.serializers import CategorySerializer
import string
import random
from django.core.mail import send_mail  # отправка сообщений
from rest_framework import status  # статусы
from rest_framework.decorators import api_view, permission_classes  # декоратор
from rest_framework.permissions import AllowAny  # разрешения
from rest_framework.response import Response
from users.models import User
from .serializers import SignUpSerializer
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
        # User.objects.all().delete()
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
            return Response(
                {'message': 'confirmation_code отправлен вам на почту'},
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
