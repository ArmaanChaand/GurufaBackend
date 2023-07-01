from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Course, Plans, Levels, Schedule
from .serializers import CourseSerializer, LevelsSerializer, PlansSerializer, ScheduleSerializer

@api_view(http_method_names=['GET'])
def getAllCourses(request):    
    plans = Plans.objects.all()
    plans_serializer = PlansSerializer(plans, many=True)
    courses = Course.objects.all()
    course_serializer = CourseSerializer(courses, many=True)

    data = {            
        'plans': plans_serializer.data,
        'courses': course_serializer.data
    }
    return Response(data)           

@api_view(['GET'])
def getAllSchedules(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        batches = Schedule.objects.filter(to_course=course)
        serializer = ScheduleSerializer(batches, many=True)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)