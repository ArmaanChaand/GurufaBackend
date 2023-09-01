from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Course, Plans, Levels, Schedule
from .serializers import CourseSerializer, LevelsSerializer, PlansSerializer, ScheduleSerializer
from datetime import date

@api_view(http_method_names=['GET'])
def getAllCourses(request):    
    plans = Plans.objects.filter(is_active=True)
    plans_serializer = PlansSerializer(plans, many=True)
    courses = Course.objects.filter(is_active=True)
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
        plan = Plans.objects.get(slug=request.GET.get('plan_slug'))
        schedules = Schedule.objects.filter(to_course=course, plan=plan, is_active=True)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    except Course.DoesNotExist or Plans.DoesNotExist:
        return Response({'error': 'Course or Plan not found.'}, status=status.HTTP_404_NOT_FOUND)