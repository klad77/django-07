from django.db import models

# Модель Category


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название категории

    class Meta:
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.name

# Модель Task

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)  # Название задачи
    description = models.TextField()  # Описание задачи
    categories = models.ManyToManyField(Category, related_name='tasks')  # Категории задачи
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # Статус задачи
    deadline = models.DateTimeField()  # Дата и время дедлайна
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания

    class Meta:
        unique_together = ('title', 'created_at')  # Уникальное сочетание названия задачи и даты

    def __str__(self):
        return self.title

# Модель SubTask

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

    def __str__(self):
        return self.title
