import codecs
import csv
import os.path

from django.conf import settings
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from users.models import User

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    help = 'load data from csv'

    def handle(self, *args, **options):

        load_dir = os.path.join(f'{settings.BASE_DIR}', 'static', 'data')

        with codecs.open(os.path.join(load_dir, 'category.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('category.csv uploading...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                category = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                category.save()
            print('category.csv complete.')

        with codecs.open(os.path.join(load_dir, 'genre.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('genre.csv uploading...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                genre.save()
            print('genre.csv complete.')

        with codecs.open(os.path.join(load_dir, 'titles.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('titles.csv uploading...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                category = Category.objects.get(pk=row['category'])
                titles = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category
                )
                titles.save()
            print('titles.csv complete.')

        with codecs.open(os.path.join(load_dir, 'genre_title.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('genre_title.csv uploading...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                genre_title = GenreTitle(
                    id=row['id'],
                    genre=genre,
                    title=title
                )
                genre_title.save()
            print('genre_title.csv complete.')

        with codecs.open(os.path.join(load_dir, 'users.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('users.csv uploading...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                user = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                user.save()
            print('users.csv complete.')

        with codecs.open(os.path.join(load_dir, 'review.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('review.csv uploading...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                title = Title.objects.get(pk=row['title_id'])
                author = User.objects.get(pk=row['author'])
                review = Review(
                    id=row['id'],
                    text=row['text'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                    title=title,
                    author=author
                )
                review.save()
            print('review.csv complete.')

        with codecs.open(os.path.join(load_dir, 'comments.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('comments.csv uploading...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                review = Review.objects.get(pk=row['review_id'])
                author = User.objects.get(pk=row['author'])
                comments = Comment(
                    id=row['id'],
                    text=row['text'],
                    pub_date=row['pub_date'],
                    review=review,
                    author=author
                )
                comments.save()
            print('comments.csv complete.')
