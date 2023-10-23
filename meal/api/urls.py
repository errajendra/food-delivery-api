from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
    CategoryView, SubCategoryView,
    MealView,
    PlanListingView,
)

router = DefaultRouter()

router.register('category', CategoryView, basename='category-api')
router.register('sub-category', SubCategoryView, basename='sub-category-api')
router.register('meals', MealView, basename='meal-api')
router.register('plans', PlanListingView, basename='plan-api')


urlpatterns = [
    path('', include(router.urls)),
]
