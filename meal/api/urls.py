from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
    CategoryView, SubCategoryView,
    MealView,
    PlanListingView, PlanPurcheseView,
    MenuListOfPlan, PlanMeal
)

router = DefaultRouter()

router.register('category', CategoryView, basename='category-api')
router.register('sub-category', SubCategoryView, basename='sub-category-api')
router.register('meals', MealView, basename='meal-api')
router.register('plans', PlanListingView, basename='plan-listing-api')
router.register('plan-purchese', PlanPurcheseView, basename='plan-purchese-api')
router.register('plan-menu-meal', MenuListOfPlan, basename='plan-menu-meal-api')
router.register('plan-your-meal', PlanMeal, basename='plan-your-meal-api')


urlpatterns = [
    path('', include(router.urls)),
]
