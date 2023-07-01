from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Purchase
from .serializers import PurchaseSerializer
from course.models import Levels, Plans, Schedule
from user.models import User, Kid   
# Create your views here.

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def CreatePurchase(request):
    course_level_id = request.data.get('course_level_id')
    print(course_level_id)
    schedule_id = request.data.get('schedule_id')
    plan_selected_id = request.data.get('plan_selected_id')
    kids_selected_ids = request.data.get('kids_selected_ids')
    purchase_price = request.data.get('purchase_price')

    try:
        user = request.user
    except User.DoesNotExist:
        return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course_level = Levels.objects.get(id=course_level_id)
    except Levels.DoesNotExist:
        return Response({'error': 'Invalid course level ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        return Response({'error': 'Invalid schedule ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        plan_selected = Plans.objects.get(id=plan_selected_id)
    except Plans.DoesNotExist:
        return Response({'error': 'Invalid plan selected ID'}, status=status.HTTP_400_BAD_REQUEST)

    # kids_selected = Kid.objects.filter(id__in=kids_selected_ids)
    kids_selected = user.my_kids.filter(id__in=kids_selected_ids)

    purchase = Purchase.objects.create(
        user=user,
        course_level=course_level,
        schedule=schedule,
        plan_selected=plan_selected,
        purchase_price=purchase_price
    )
    purchase.kids_selected.set(kids_selected)

    return Response({'message': 'Purchase created successfully'}, status=status.HTTP_201_CREATED)




"""
purchase_data = {
            "user": request.user,
            "course_level": Levels.objects.get(id=user_data["course_level"]),
            "plan_selected": Plans.objects.get(id=user_data["plan_selected"]),
            "schedule": Schedule.objects.get(id=user_data["schedule"]),
            "kids_selected": user_data["kids_selected"],
            "purchase_price": user_data["purchase_price"],
        }
"""