import uuid
import requests
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from django.db import transaction
import razorpay
from .models import Purchase, PurchaseSession
from .serializers import PurchaseSerializer, PurchaseSessionSerializer
from course.models import Levels, Plans, Schedule, Course
from course.serializers import PlansSerializer
from user.models import User, Kid   
# Create your views here.

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def CreatePurchase(request):
    payment_method_chosen = request.data.get('payment_method_chosen')
    course_level_id = request.data.get('course_level_id')
    schedule_id = request.data.get('schedule_id')
    plan_selected_id = request.data.get('plan_selected_id')
    kids_selected_ids = request.data.get('kids_selected_ids')
    purchase_price = request.data.get('purchase_price')
    purchase_session_identifier = request.data.get('purchase_session')

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

    try:
        purchase_session = PurchaseSession.objects.get(identifier=purchase_session_identifier)
    except Exception as e:
        purchase_session = None

    kids_selected = user.my_kids.filter(id__in=kids_selected_ids)

    new_booking_id = course_level.to_course.slug[:3] + str(uuid.uuid4().hex[:7])
    purchase = Purchase.objects.create(
        user=user,
        course_level=course_level,
        schedule=schedule,
        plan_selected=plan_selected,
        purchase_price=purchase_price,
        booking_id= new_booking_id.upper()
    )
    purchase.kids_selected.set(kids_selected)
    purchase.purchase_session = purchase_session

    """DEMO PLAN SELECTED"""
    if purchase_price == 0 or purchase_price < 1:
        purchase.payment_status = 'PAID'
        purchase.payment_platform = 'Free Purchase'
        schedule.seats_occupied = int(schedule.seats_occupied) + kids_selected.count()
        purchase.order_id = "free_purchase_" + str(user.username) + str(uuid.uuid4().hex[:8])
        purchase.payment_id = "Free Purchase"
        purchase.order_signature = "Free Purchase"
        schedule.save()
        """Update the demo_course table for Kids"""
        with transaction.atomic():
            for kid in kids_selected:
                kid.demo_courses.add(course_level.to_course)
        purchase.save()

        data = {}
        data['method'] = 'Free Purchase'
        data['purchase_data'] = PurchaseSerializer(purchase).data
        return Response(data=data, status=status.HTTP_201_CREATED)


    """RAZORPAY ORDER"""
    if payment_method_chosen == 'Razorpay' and purchase_price > 0:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        DATA = {
            "amount": float(purchase.purchase_price) * 100,
            "currency": "INR",
            "receipt": f"receipt@Razorpay{purchase.id}",
            "notes": {
                "purchase_id": purchase.id,
            }
        }
        try:
            razorpay_order = client.order.create(data=DATA)
            purchase.order_id = razorpay_order['id']
            purchase.payment_platform = 'Razorpay'
            purchase.save()
            response_data = {
                'message': 'Purchase created successfully',
                'order_created': True, 
                'order': razorpay_order,
                'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID ,
                'method': 'Razorpay',

            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Some error ocurred.'}, status=status.HTTP_400_BAD_REQUEST)
    
    """CASHFREE"""
    if payment_method_chosen == 'Cashfree' and purchase_price > 0:
        url = f"{settings.CASHFREE_ENDPOINT}/orders"
        payload = {
            "customer_details": {
                "customer_id": user.username,
                "customer_name": user.get_full_name(),
                "customer_email": user.email,
                "customer_phone": str(user.phone_number.national_number)
            },
            "order_amount": float(purchase.purchase_price),
            "order_currency": "INR",
            "order_id": new_booking_id.upper()
        }
        headers = {
            "accept": "application/json",
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY,
            "content-type": "application/json",
            "x-api-version": "2023-08-01",
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            res_data = json.loads(response.text)
            purchase.payment_platform = 'Cashfree'
            purchase.order_id = res_data['cf_order_id']
            purchase.payment_id = 'TBD'
            purchase.order_signature = '---'
            schedule.save()
            purchase.save()
            response_data = {
                    'message': 'Purchase created successfully',
                    'order_created': True, 
                    'order': res_data,
                    'method': 'Cashfree',
                }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': 'Some error ocurred.'}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def successPurchaseRazorpay(request):
    razorpay_payment_id = request.data.get('razorpay_payment_id')
    razorpay_order_id = request.data.get('razorpay_order_id')
    razorpay_signature = request.data.get('razorpay_signature')
    purchase_id = request.data.get('purchase_id')

    try:
        purchase = Purchase.objects.get(id=purchase_id, user=request.user)
        purchase.payment_id = razorpay_payment_id
        purchase.order_signature = razorpay_signature
        if purchase.order_id == razorpay_order_id:
            purchase.payment_status = 'PAID'
            purchase.schedule.seats_occupied = int(purchase.schedule.seats_occupied) + purchase.kids_selected.count()
            purchase.schedule.save()
            try:
                purchase.purchase_session.session_status = 'COMPLETED'
                purchase.purchase_session.save()
            except Exception as e:
                pass
            purchase.save()
            purchase_data = PurchaseSerializer(purchase)
            return Response({"updated": True, 'purchase_data': purchase_data.data},  status=status.HTTP_200_OK)
        else :
            return Response({"updated": False, "message": "Order ID didn't matched"}, status=status.HTTP_400_BAD_REQUEST)

    except Purchase.DoesNotExist:
        return Response({'error': 'Purchase Does Not Exists'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def failedPurchaseRazorpay(request):
    razorpay_payment_id = request.data.get('razorpay_payment_id')
    razorpay_order_id = request.data.get('razorpay_order_id')
    razorpay_signature = request.data.get('razorpay_signature')
    purchase_id = request.data.get('purchase_id')

    try:
        purchase = Purchase.objects.get(id=purchase_id, user=request.user)
        purchase.payment_id = razorpay_payment_id
        purchase.order_signature = razorpay_signature
        if purchase.order_id == razorpay_order_id:
            purchase.payment_status = 'FAILED'
            purchase.payment_platform = 'Razorpay'
            purchase.save()
            return Response({"updated": True}, status=status.HTTP_200_OK)
        else :
            return Response({"updated": False, "message": "Order ID didn't matched"}, status=status.HTTP_400_BAD_REQUEST)

    except Purchase.DoesNotExist:
        return Response({'error': 'Purchase Does Not Exists'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def getOrderCashfree(request):
    cf_order_id = request.data.get('cf_order_id')

    try:
        purchase = Purchase.objects.get(booking_id=cf_order_id, user=request.user,  payment_platform='Cashfree')
        url = f"{settings.CASHFREE_ENDPOINT}/orders/{cf_order_id}/payments"
        headers = {
            "accept": "application/json",
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY,
            "x-api-version": "2023-08-01",
        }
        response = requests.get(url=url, headers=headers)
        res_data = json.loads(response.text)[0]
        if(res_data['payment_status'] == "SUCCESS"):
            purchase.payment_status = 'PAID'
            purchase.payment_method = json.dumps(res_data['payment_method'])
            purchase.payment_id = res_data['cf_payment_id']
            purchase.schedule.seats_occupied = int(purchase.schedule.seats_occupied) + purchase.kids_selected.count()
            purchase.schedule.save()
            try:
                purchase.purchase_session.session_status = 'COMPLETED'
                purchase.purchase_session.save()
            except Exception as e:
                pass
            purchase.save()
            response_data = {
                'payment_status': "SUCCESS",
                'purchase_data': PurchaseSerializer(purchase).data,
                'plan_selected': PlansSerializer(purchase.plan_selected).data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            purchase.payment_status = 'FAILED'
            purchase.payment_id = res_data['cf_payment_id']
            purchase.save()
            response_data = {
                'payment_status': "FAILED",
                'order_status': res_data,
                'order_detail': {
                    'payment_method' : purchase.payment_platform,
                    'payment_id': res_data['cf_payment_id'],
                    'order_id': purchase.booking_id,
                    'error_description': res_data['error_details']['error_description'],
                }
                
            }
            return Response(response_data, status=status.HTTP_200_OK)


    except Purchase.DoesNotExist:
        return Response({'error': 'Purchase Does Not Exists'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def CreatePurchaseSession(request):
    plan_selected = request.data.get('plan_selected')
    level_selected = request.data.get('level_selected')
    course_selected = request.data.get('course_selected')

    try:
        user = request.user
    except User.DoesNotExist:
        return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        level = Levels.objects.get(id=level_selected)
    except Levels.DoesNotExist:
        return Response({'error': 'Invalid course level ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        course = Course.objects.get(slug=course_selected)
    except Schedule.DoesNotExist:
        return Response({'error': 'Invalid schedule ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        plan = Plans.objects.get(id=plan_selected)
    except Plans.DoesNotExist:
        return Response({'error': 'Invalid plan selected ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        query_purchase_session = PurchaseSession.objects.filter(
            user=user,
            course_selected=course,
            plan_selected=plan,
            level_selected=level,
            session_status='INCOMPLETE'
        )
        if query_purchase_session.exists():
            query_purchase_session_serializer = PurchaseSessionSerializer(query_purchase_session.last())
            return Response({'purchase_session': query_purchase_session_serializer.data}, status=status.HTTP_200_OK)
        else:
            identifier = str(uuid.uuid4().hex[:16])  
            purchase_session = PurchaseSession.objects.create(
                user=user,
                course_selected=course,
                plan_selected=plan,
                level_selected=level,
                identifier=identifier.upper()
            )   
            purchase_session_serializer = PurchaseSessionSerializer(purchase_session)
            return Response({'purchase_session': purchase_session_serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': 'Some error ocurred.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def getPurchaseSession(request, identifier):
    try:
        purchase_session = PurchaseSession.objects.get(
            user=request.user,
            identifier=identifier,
            session_status='INCOMPLETE'
        )   
        purchase_session_serializer = PurchaseSessionSerializer(purchase_session)
        return Response({'purchase_session': purchase_session_serializer.data}, status=status.HTTP_200_OK)
    except PurchaseSession.DoesNotExist:
        return Response({'error': 'Some error ocurred.'}, status=status.HTTP_400_BAD_REQUEST)



