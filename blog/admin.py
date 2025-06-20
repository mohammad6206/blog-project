# admin.py
from django.contrib import admin
from blog.models import Post,Category,pakages

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_date', 'counted_view')
    list_filter = ('status', 'published_date', 'category')
    search_fields = ('title', 'author__username', 'content')
    readonly_fields = ('counted_view', 'created_date', 'updated_date')
    filter_horizontal = ('category',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    

@admin.register(pakages)
class pakagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'hotel', 'hotel_stars', 'max_count', 'price', 'Number_of_nights', 'location')
    search_fields = ('name', 'description', 'hotel', 'location')
    list_filter = ('hotel_stars', 'max_count', 'price', 'Number_of_nights', 'location')
    ordering = ('name',)


