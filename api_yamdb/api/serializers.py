from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects 
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source = 'reviews__score__avg', red_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class GenreTitleSerializer(serializers.ModelSerializer):
    pass
