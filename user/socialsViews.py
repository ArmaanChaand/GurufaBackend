from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from google.auth import jwt
from datetime import datetime

from .models import User
from .serializers import userInfoSerializer, registerUserSerializer

from .validators import generate_strong_password
from .verifyViews import sendHtmlEmail
@api_view(['POST'])
def googleOAuth2(request):
    id_token = request.data.get('credential')
    response_data = {}

    if id_token:
        try:
            decoded_token = jwt.decode(id_token, verify=False)
            email = decoded_token.get('email', '')
            # Check if the token is expired
            now = datetime.utcnow()
            if 'exp' in decoded_token and now < datetime.fromtimestamp(decoded_token['exp']):
                if User.objects.filter(email=email, auth_providers='Email').exists():
                    return Response({'error': 'This email already being used. Use regular sign in.'}, status=status.HTTP_400_BAD_REQUEST)
                if User.objects.filter(email=email, auth_providers='Google').exists():
                    user = User.objects.filter(email=email, auth_providers='Google')[0]
                    picture_url = decoded_token.get('picture', '')
                    if picture_url and picture_url != '':
                        user.auth_provider_img = picture_url
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
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    new_user_data = {
                        'first_name': decoded_token.get('given_name', ''),
                        'last_name': decoded_token.get('family_name', ''),
                        'email': email,
                        'password': generate_strong_password(15),
                        'whatsapp_update': False,
                        'phone_number': decoded_token.get('phone_number', ''),
                    }
                    new_user_serializer = registerUserSerializer(data=new_user_data, many=False)
                    if new_user_serializer.is_valid():
                        user = new_user_serializer.save()
                        user.auth_providers = 'Google'    
                        user.is_email_verified = decoded_token.get('email_verified', False)
                        picture_url = decoded_token.get('picture', '')
                        user.auth_provider_img = picture_url
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

                        """Send Welcome Email"""
                        sendHtmlEmail(
                            subject='Welcome to Gurufa Kids',
                            recipient_list=[user_data['email']],
                            email_template_name='welcome_email.html',
                            email_template_context={
                                'first_name': user_data['first_name']
                            }
                        )
                        return Response(response_data, status=status.HTTP_201_CREATED)
                    else:
                        response_data['errors'] = "Some error ocurred! Try again."
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Token expired.'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.InvalidTokenError:
            # Handle invalid token error
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Missing id_token parameter.'}, status=status.HTTP_400_BAD_REQUEST)
