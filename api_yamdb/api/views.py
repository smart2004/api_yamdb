from django.shortcuts import render
from reviews.models import Category
from api.serializers import CategorySerializer
from rest_framework import viewsets(ListCreateDestroyViewSet)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)
    lookup_field = 'slug'

class GenreViewSet(ListCreateDestroyViewSet):
    pass
