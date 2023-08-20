from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Kid
from .serializers import registerUserSerializer, userInfoSerializer, kidInfoSerializer
from purchase.models import Purchase
from purchase.serializers import PurchaseSerializer
from course.models import Course
from course.serializers import CourseSerializer
from .verifyViews import send_verification_email, sendOTP, send_password_reset_email

@api_view(http_method_names=['GET'])
def userAPIView(request):
    users = User.objects.all()
    data = userInfoSerializer(users, many=True).data
    data = {
        'users': data,
        'num_of_users': len(users),
    }
    return Response(data=data)

@api_view(http_method_names=['POST'])
def authenticateUser(request):
    response_data = {}
    if request.method == 'POST':
        data = request.data
        user = authenticate(request, email=data['email'], password=data['password'])
        if user is not None: 
            user.last_login = timezone.now()
            user.save()
            refresh = RefreshToken.for_user(user)
            response_data['success'] = True
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            response_data['token'] = token
            user_data = userInfoSerializer(user, many=False).data
            response_data['user_data'] = user_data
            if not user.is_phone_verified:
                response_data['otp'] = True
                sendOTP(user)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data['success']= False
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    if request.method == 'POST':
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=200)
        except Exception:
            return Response({'error': 'Invalid refresh token.'}, status=400)



@api_view(http_method_names=['POST'])
def registerUser(request):
    if request.method == 'POST':
        new_user_serializer = registerUserSerializer(data=request.data, many=False)
        response_data = {} 
        if new_user_serializer.is_valid():
            user = new_user_serializer.save()
            user.save()
            response_data['user'] = new_user_serializer.data
            """Issue Tokens"""
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            response_data['token'] = token
            user_data = userInfoSerializer(user, many=False).data
            response_data['user_data'] = user_data
            try:
                send_verification_email(request=request, user=user)
                if user.phone_number:
                    sendOTP(user=user)
            except:
                pass
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data['errors'] = new_user_serializer.errors
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def getUserInfo(request):
    user = request.user
    response_data = {} # Append With Informations
    data = userInfoSerializer(user, many=False).data
    response_data['user'] = data
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUserName(request):
    user = request.user
    if request.method == 'POST':
        serializer = userInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUserKey(request):
    email = request.user.email
    password = request.data['password']
    if request.method == 'POST':
        user = authenticate(request, email=email, password=password)
        print(email, password)
        response_data = {}
        if user is not None:
            send_password_reset_email(request=request, user=request.user)
            response_data['authenticated'] = True
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data['authenticated'] = False
            response_data['detail'] = 'Incorrect Password'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error' : 'Some error ocurred'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def getMyKids(request):
    try:
        user = request.user 
        kids = Kid.objects.filter(kid_parent=user, is_active=True)
        serializer = kidInfoSerializer(kids, many=True)
        return Response(serializer.data)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def saveMyKid(request, kid_id=None):
    if kid_id is not None:
            try:
                kid = Kid.objects.get(id=kid_id)
            except Kid.DoesNotExist:
                return Response({"error": "Kid not found."}, status=status.HTTP_404_NOT_FOUND)
            updated_data = request.data.copy()  # Create a copy of the request data
            if(updated_data['kid_profile'] == ""):
                updated_data['kid_profile'] = kid.kid_profile  # Update the kid_profile field with the desired new value
            serializer = kidInfoSerializer(instance=kid, data=updated_data, partial=True)
    else:
        serializer = kidInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(kid_parent=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteAKid(request, kid_id):
    try:
        the_kid = Kid.objects.get(id=kid_id)
    except Kid.DoesNotExist:
        return Response({"error": "Kid not found."}, status=status.HTTP_404_NOT_FOUND)

    the_kid.is_active = False
    the_kid.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPurchasedCourses(request):
    try:
        purchases = Purchase.objects.filter(user=request.user, payment_status='PAID')
        
        purchase_serializer = PurchaseSerializer(purchases, many=True)
        return Response(data=purchase_serializer.data, status=status.HTTP_200_OK)
    except Purchase.DoesNotExist:
        return Response({'error': 'No purchased courses found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def updatePhoneNuber(request):
    user = request.user  # Retrieve the authenticated user
    
    if request.method == 'POST':
        serializer = userInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            sendOTP(user=user)
            data = {
                'user_data': serializer.data,
                'otp': True
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgotKeyEmail(request):
    if request.method == 'POST':
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(request=request, user=user)
            return Response({'email_sent': True}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': "User with this email address does not exists."}, status=status.HTTP_400_BAD_REQUEST)

