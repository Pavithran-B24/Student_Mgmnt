from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from student_registry.models import Students
from token_auth.serializers import StdSerializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your views here.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=True, **kwargs):
    if created:
        token=Token.objects.create(user=instance)
        print(token.key)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listview(request):
    students = Students.objects.all()
    serializer = StdSerializers(students,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_std(request):
    student = StdSerializers(data=request.data)
    if student.is_valid():
        student.save()
        return Response(student.data,status=status.HTTP_201_CREATED)
    
    else:
        return Response(student.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_std(request,id):
    student = Students.objects.get(id=id)
    serializer = StdSerializers(instance=student,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def del_std(request,id):
    student = Students.objects.get(id=id)
    student.delete()
    return Response({"message": "Student info deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
