from rest_framework import serializers
from student_registry.models import Students


class StdSerializers(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'