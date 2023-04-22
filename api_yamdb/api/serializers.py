from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Genre, Title, Review, Comment, User
from users.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений"""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений только для чтения"""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'It is not applicable to add more than one review'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователей"""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            validate_username,
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    def validate(self, attrs):
        # Других идей по реализации нет
        if User.objects.filter(
            username=attrs['username'],
            email=attrs['email']
        ).exists():
            return attrs
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username exists")
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email exists")
        return attrs

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор токенов"""
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    def validate(self, attrs):
        get_object_or_404(User, username=attrs['username'])
        if len(attrs['confirmation_code']) != 32:
            raise serializers.ValidationError("Confiramtion code length error")
        if not User.objects.filter(
            username=attrs['username'],
            confirmation_code=attrs['confirmation_code']
        ).exists():
            raise serializers.ValidationError(
                "This confirmation_code not found"
            )
        return attrs

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
