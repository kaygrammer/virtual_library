from django.contrib import admin
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'language', 'isbn', 'total_copies', 'available_copies']
    list_filter = ['title', 'author']
    list_editable = ['total_copies', 'available_copies']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'stud_id', 'school', 'faculty', 'department', 'contact_no', 'email', 'total_book_due']
    list_filter = ['name', 'stud_id']

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ['student']

admin.site.register(Genre)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Reviews)