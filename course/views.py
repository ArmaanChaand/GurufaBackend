from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Course
from .serializers import CourseSerializer

@api_view(http_method_names=['GET'])
def getAllCourses(request):    
    courses = Course.objects.all()
    all_courses = CourseSerializer(courses, many=True).data
    return Response(all_courses)