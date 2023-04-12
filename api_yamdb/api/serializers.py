from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('reviews', )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        source='author.username', read_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    text = serializers.CharField(allow_null=True)
    id = serializers.ReadOnlyField()
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueValidator(
                queryset=Review.objects.all(),
                message='Вы уже написали отзыв к данному произведению'
            )
        ]

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj.title)
        if reviews:
            total_score = sum([review.score for review in reviews])
            rating = total_score / len(reviews)
            return round(rating, 2)
        return None
