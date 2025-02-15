from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
    MealView,
    MealTypeView,
    PlanListingView, PlanPurcheseView,
    MenuListOfPlan, PlanMeal, BannerView,
    RequestedPlanMealHistory,
    CancelMealRequest,
    DailyMealMenuView,
    CustomerSupportView,
    SalesConnectViews,
    CheckCouponCode,
    KitchenOffDateView,
    get_distance, get_service_area_by_zipcode,
)

router = DefaultRouter()

router.register('meals', MealView, basename='meal-api')
router.register('meal-plans', MealTypeView, basename='meal-plan-listing-api')
router.register('plans', PlanListingView, basename='plan-listing-api')
router.register('plan-purchese', PlanPurcheseView, basename='plan-purchese-api')
router.register('plan-menu-meal', MenuListOfPlan, basename='plan-menu-meal-api')
router.register('plan-your-meal', PlanMeal, basename='plan-your-meal-api')
router.register('requested-meal-history', RequestedPlanMealHistory, 
                basename='requested-meal-history-api')
router.register('cancel-meal-request', CancelMealRequest,
                basename='cancel-meal-request-api')
router.register('daily-meal-menu', DailyMealMenuView,
                basename='daily-meal-menu-api')
router.register('customer-support', CustomerSupportView,
                basename='customer-support-api')
router.register('sales-connect', SalesConnectViews,
                basename='sales-connect-api')
router.register('kitchen-off-dates', KitchenOffDateView, basename='kitchen-off-dates-api')

urlpatterns = [
    path('', include(router.urls)),
    path('banners/', BannerView.as_view(), name='banner-api'),
    path('check-coupon/', CheckCouponCode.as_view(), name='check-coupon-api'),
    path('check-distance/', get_distance, name='check-distance-api'),
    path('check-service-area-by-zipcode/', get_service_area_by_zipcode, name='check-service-area-by-zipcode-api'),

]
