from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from .serializers import BecomeAGuruSerializer
from .models import BecomeAGuru
# Create your views here.

@api_view(http_method_names=['POST'])
def becomeAGuruView(request):
    become_a_guru_serializer = BecomeAGuruSerializer(data=request.data)
    if become_a_guru_serializer.is_valid():
        return Response(data=become_a_guru_serializer.data, status=status.HTTP_201_CREATED)
    else :
        return Response(data=become_a_guru_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveBecomeAGuru(GenericAPIView):
    serializer_class = BecomeAGuruSerializer
    queryset = BecomeAGuru.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
