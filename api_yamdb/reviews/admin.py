from django.contrib import admin
# from .models import User
from .models import Category
from .models import Genre
from .models import Title
from .models import GenreTitle
from .models import Review
from .models import Comment


# admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)