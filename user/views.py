# from django.shortcuts import render

# # Create your views here.
# from google.auth.transport import requests
# from google.oauth2 import id_token
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken

# from .models import User

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def google_login(request):
#     token = request.data.get('token')
#     idinfo = id_token.verify_oauth2_token(token, requests.Request())
#     if idinfo['aud'] not in [YOUR_CLIENT_ID]:
#         return Response('Invalid client ID', status=403)
#     if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#         return Response('Invalid issuer', status=403)

#     email = idinfo['email']
#     name = idinfo['name']
#     user, created = User.objects.get_or_create(email=email, defaults={'password': User.objects.make_random_password()})
#     if created:
#         user.first_name = name
#         user.save()
#         user.groups.add(Group.objects.get(name='User'))  # Optional: Assign user to a specific group
    
#     refresh = RefreshToken.for_user(user)
#     return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
