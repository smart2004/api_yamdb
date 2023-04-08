from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import UserViewSet
# from .views import CategoryViewSet
# from .views import GenreViewSet
# from .views import TitleViewSet
# from .views import ReviewViewSet
# from .views import CommentViewSet
# from .views import register
# from .views import get_jwt_token


router = DefaultRouter()

# router.register(r'users', UserViewSet, basename='users')
# router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'genres', GenreViewSet, basename='genres')
# router.register(r'titles', TitleViewSet, basename='titles')
# router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
# router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
#    path('v1/', include('djoser.urls')),
#    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
#    path('v1/auth/signup/', register, name='register'),
#    path('v1/auth/token/', get_jwt_token, name='token')
]