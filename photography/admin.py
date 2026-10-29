from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'place', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'place')
    search_fields = ('customer_name', 'place', 'comment')