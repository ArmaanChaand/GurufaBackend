from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import FAQs, Review
from .serializers import FAQsSerializer,ReviewSerializer
# Create your views here.

@api_view(http_method_names=['GET'])
def getAllFaqs(request):
    faqs = FAQs.objects.all()
    faqs_data = FAQsSerializer(faqs, many=True).data
    return Response(faqs_data)

@api_view(http_method_names=['GET'])
def getAllReviews(request):
    reviews = Review.objects.all()
    reviews = ReviewSerializer(reviews, many=True).data
    return Response(reviews, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCourseReviews(request, course_id):
    try:
        course_reviews = Review.objects.filter(to_course_id=course_id)
    except Review.DoesNotExist:
        return Response(status=404)

    paginator = PageNumberPagination()
    paginator.page_size = 2  # Number of reviews per page
    paginated_reviews = paginator.paginate_queryset(course_reviews, request)

    serializer = ReviewSerializer(paginated_reviews, many=True)
    return paginator.get_paginated_response(serializer.data)
