from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Course, Plans, Levels, Batch
from .serializers import CourseSerializer, LevelsSerializer, PlansSerializer, BatchSerializer

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

@api_view(http_method_names=['GET'])
def getAllBatches(request   ):
    batches = Batch.objects.all()
    return Response(BatchSerializer(batches, many=True).data)