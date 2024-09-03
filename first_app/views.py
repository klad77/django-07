from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
# from .models import *
from .serializers import *
from rest_framework import status


class TaskPagination(PageNumberPagination):
    page_size = 3  # Количество задач на странице
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@api_view(['GET'])
def task_statistics(request):
    total_tasks = Task.objects.count()
    status_counts = Task.objects.values('status').annotate(count=Count('status'))
    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now(),
        status__in=['New', 'In progress', 'Pending']
    ).count()

    data = {
        'total_tasks': total_tasks,
        'status_counts': {item['status']: item['count'] for item in status_counts},
        'overdue_tasks': overdue_tasks
    }

    return Response(data, status=status.HTTP_200_OK)


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        task_id = self.request.data.get('task_id')
        if not task_id:
            raise serializers.ValidationError({"task_id": "This field is required."})
        task = Task.objects.get(id=task_id)
        serializer.save(task=task)


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
