from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Course
from .serializers import CourseSerializer

@api_view(http_method_names=['GET'])
def getAllCourses(request):
    response_data = {}        
    courses = Course.objects.all()
    response_data['courses'] = CourseSerializer(courses, many=True).data
    return Response(response_data)