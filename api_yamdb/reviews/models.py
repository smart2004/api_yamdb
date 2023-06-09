from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_year
from users.models import User


class Category(models.Model):
    """Категория произведения"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    """Жанр произведения"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Title(models.Model):
    """Описание произведения"""
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=(validate_year,))
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class GenreTitle(models.Model):
    """Связь произведения с жанром"""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, genre: {self.genre}'


class Review(models.Model):
    """Отзывы к произведениям"""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Publication date', auto_now=True)

    class Meta:
        default_related_name = 'reviews'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]


class Comment(models.Model):
    """Комменатрии к отзывам"""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField('Publication date', auto_now_add=True)

    class Meta:
        default_related_name = 'comments'
        ordering = ['pub_date']
