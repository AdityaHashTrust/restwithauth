from django.urls import path,include
from rest_framework import routers
# from .views import ArticleDetailView,ArticleListView
# from .views import ArticleAPIView,AuthorAPIView
from .views import ArticleViewSet,AuthorViewSet, CustomAuthToken,RegisterUser,LogoutUser

from rest_framework.authtoken import views

router=routers.DefaultRouter()
router.register(r'authors',AuthorViewSet)
router.register(r'articles',ArticleViewSet)
urlpatterns = [
    path('',include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('register/',RegisterUser.as_view()),
    path('custom/',CustomAuthToken.as_view()),
    path('logout/',LogoutUser.as_view())
]
