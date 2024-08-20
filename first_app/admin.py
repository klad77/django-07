from django.contrib import admin
from .models import Category, Task, SubTask

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories', 'deadline')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    ordering = ('-created_at',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'task', 'deadline')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
