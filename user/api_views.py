from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import userSerializer, registerUserSerializer, userInfoSerializer

@api_view(http_method_names=['GET'])
def userAPIView(request):
    users = User.objects.all()
    data = userInfoSerializer(users, many=True).data
    data = {
        'users': data,
        'num_of_users': len(users),
    }
    return Response(data=data)

@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated])
def getUserInfo(request):
    theUser = request.user
    data = userInfoSerializer(theUser, many=False).data
    response_data = {
        'users': data,
    }
    return Response(data=response_data)


@api_view(http_method_names=['POST'])
def registerUser(request):
    if request.method == 'POST':
        new_user_serializer = registerUserSerializer(data=request.data, many=False)
        response_data = {} # Append With Informations
        if new_user_serializer.is_valid():
            user = new_user_serializer.save()
            user.set_password(request.data['password'])
            user.save()
            response_data['success']= True,
            response_data['user'] = new_user_serializer.data
            """Issue Tokens"""
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            response_data['token'] = token
        else:
            response_data['success']= False,
            response_data['errors'] = new_user_serializer.errors
        return Response(response_data)
            