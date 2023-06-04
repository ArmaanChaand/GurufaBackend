from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQs
from .serializers import FAQsSerializer
# Create your views here.
@api_view(http_method_names=['GET'])
def getAllFaqs(request):
    faqs = FAQs.objects.all()
    faqs_data = FAQsSerializer(faqs, many=True).data
    return Response(faqs_data)