from datetime import date, timedelta
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from meal.models import MealRequestDaily
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect, get_object_or_404


class MealRequestSerilizer(serializers.ModelSerializer):
    class Meta:
        model = MealRequestDaily
        fields = "__all__"

class OrderDeliverView(viewsets.ModelViewSet):
    serializer_class = MealRequestSerilizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MealRequestDaily.objects.filter(delivery_person=self.request.user)

    def list(self, request, *args, **kwargs):
        # Check if the user is a delivery person
        if not self.request.user.is_delivery_person:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "You are not a delivery person. Please log in as a delivery person.",
                }
            )
           

        queryset = self.get_queryset()

        # Fetching data for today, tomorrow, and history
        today_data = queryset.filter(date__date=date.today())
        tomorrow_data = queryset.filter(date__date=date.today() + timedelta(days=1))
        history_data = queryset.exclude(date__date__in=[date.today(), date.today() + timedelta(days=1)])

        serializer = MealRequestSerilizer

        response_data = {
            'today': serializer(today_data, many=True).data,
            'tomorrow': serializer(tomorrow_data, many=True).data,
            'history': serializer(history_data, many=True).data
        }
        return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "data":response_data
                }
            )


# delivery boy will update delivery status
@api_view(['POST'])
def change_order_status(request):
    if not request.user.is_delivery_person:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "You are not a delivery person. Please log in as a delivery person.",
            }
        )

    
    meal_id = request.POST.get('meal')
    ord_status = request.data.get('change_status')

    if not meal_id:
        return Response(data={ "status": status.HTTP_400_BAD_REQUEST,  "message": "Meal ID is missing" }, status=status.HTTP_400_BAD_REQUEST)

    if not ord_status:
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Change status is missing. Please provide a change status."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        meal_id = int(meal_id)  # Convert order_id to an integer
        order = get_object_or_404(MealRequestDaily, id=meal_id)

        auth_status_list = ['Success', 'Requested', 'Cancelled']
        if ord_status in auth_status_list:
            if order.status in ['Success', 'Requested', 'Cancelled']:
                order.status = ord_status
                order.save()
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "message": f'Order is now {order.status}'
                    },
                    status=status.HTTP_200_OK
                )
           
            else:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid choice."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
               
        else:
            return Response(
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid input for order status"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except ValueError:
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid Meal ID"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except MealRequestDaily.DoesNotExist:
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": 'Invalid Meal ID. MealRequest ID does not exist.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as ex:
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Error"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
