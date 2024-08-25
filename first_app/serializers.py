from rest_framework import serializers
from .models import *


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title', 'status', 'deadline']
