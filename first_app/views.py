from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from .serializers import TaskSerializer, TaskListSerializer
from rest_framework import status
from .models import Task

class TaskPagination(PageNumberPagination):
    page_size = 3  # Количество задач на странице
    page_size_query_param = 'page_size'
    max_page_size = 100



@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()

    # Фильтрация по статусу
    status_filter = request.query_params.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Фильтрация по дедлайну
    deadline_filter = request.query_params.get('deadline')
    if deadline_filter:
        tasks = tasks.filter(deadline__lte=deadline_filter)

    # Пагинация
    paginator = TaskPagination()
    paginated_tasks = paginator.paginate_queryset(tasks, request)
    serializer = TaskListSerializer(paginated_tasks, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def task_create(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def task_statistics(request):
#     total_tasks = Task.objects.count()
#     status_counts = Task.objects.values('status').annotate(count=Count('status'))
#     overdue_tasks = Task.objects.filter(deadline__lt=timezone.now(), status__in=['New', 'In progress', 'Pending']).count()
#     data = {
#         'total_tasks': total_tasks,
#         'status_counts': {status['status']: status['count'] for stat in status_counts},
#         'overdue_tasks': overdue_tasks
#     }
#     return Response(data, status=status.HTTP_200_OK)

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

        # 'status_counts': {status['status']: status['count'] for status in status_counts},
        'overdue_tasks': overdue_tasks
    }

    return Response(data, status=status.HTTP_200_OK)
