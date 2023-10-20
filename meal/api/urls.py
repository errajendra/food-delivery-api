from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
    CategoryView, SubCategoryView,
    MealView,
)

router = DefaultRouter()

router.register('category', CategoryView, basename='category-api')
router.register('sub-category', SubCategoryView, basename='sub-category-api')
router.register('meals', MealView, basename='meal-api')


urlpatterns = [
    path('', include(router.urls)),
]
