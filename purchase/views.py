from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Purchase
from .serializers import PurchaseSerializer
# Create your views here.

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def CreatePurchase(request):
    purchase_serializer = PurchaseSerializer(data=request.data, many=False)
    if purchase_serializer.is_valid():
        purchase_serializer.save()    
        return Response(data=purchase_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

