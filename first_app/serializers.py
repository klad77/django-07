from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['title', 'status', 'deadline']


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), source='task')

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'task_id']


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise ValidationError({"name": "A category with this name already exists."})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name != instance.name and Category.objects.filter(name=name).exists():
            raise ValidationError({"name": "A category with this name already exists."})
        return super().update(instance, validated_data)


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['title', 'description', 'status', 'deadline', 'task_id']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

    def validate_deadline(self, value):
        if value.date() < timezone.now().date():
            raise serializers.ValidationError("The deadline cannot be in the past.")
        return value
