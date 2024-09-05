from rest_framework.authtoken.admin import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)  # Название категории

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'first_app_category'  # Имя таблицы в базе данных
        verbose_name = 'Категория'  # Человекочитаемое имя модели
        verbose_name_plural = 'Категории'
        unique_together = [('name',)]


class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In_progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]
    objects = models.Manager
    title = models.CharField(max_length=200)  # Название задачи
    description = models.TextField()  # Описание задачи
    categories = models.ManyToManyField(Category, related_name='tasks')  # Категории задачи
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # Статус задачи
    deadline = models.DateTimeField()  # Дата и время дедлайна
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    class Meta:
        db_table = 'first_app_task'  # Имя таблицы в базе данных
        verbose_name = 'Задача'  # Человекочитаемое имя модели
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']  # Сортировка по убыванию даты создания
        unique_together = ('title', 'created_at')  # Уникальное сочетание названия задачи и даты

    def __str__(self):
        return self.title


class SubTask(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)  # Название подзадачи
    description = models.TextField()  # Описание подзадачи
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)  # Основная задача
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # Статус подзадачи
    deadline = models.DateTimeField()  # Дата и время дедлайна
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subtasks', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'first_app_subtask'  # Имя таблицы в базе данных
        verbose_name = 'Подзадача'  # Человекочитаемое имя модели
        verbose_name_plural = 'Подзадачи'
        ordering = ['-created_at']  # Сортировка по убыванию даты создания
        unique_together = ('title', 'task')
