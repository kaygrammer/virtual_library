from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save


# relation to the genre of books
class Genre(models.Model):
    name = models.CharField(max_length=20, help_text='Enter a book(e.g science fiction, French poetry)')

    def __str__(self):
        return self.name


# related to language of books
class Language(models.Model):
    name = models.CharField(max_length=200, help_text='Enter the boo natural language e.g English, French')

    def __str__(self):
        return self.name


# book relation that has 2 foreign key author language
# book relation can contain multiple
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description on the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character &lt;a href="https://www.isbn-international.org/content/what-isbn">ISBN number&lt;/a>')
    genre = models.ManyToManyField(Genre, help_text='select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    pic = models.ImageField(blank=True, null=True, upload_to='book_image')

# return conical url for an object
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

# __str__ method used to override default string return by object
    def __str__(self):
        return self.title


def create_user(sender, *args, **kwargs):
    if kwargs:
        user = User.objects.create_user(username=kwargs)


# relation containing info about student
# stud_id is used to determine student uniqueness
class Student(models.Model):
    stud_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, help_text='Enter full name')
    school = models.CharField(max_length=10, help_text='please input school name abbreviation')
    faculty = models.CharField(max_length=100, default=None)
    department = models.CharField(max_length=100, default=None)
    contact_no = models.CharField(max_length=11, default=None)
    total_book_due = models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    pic = models.ImageField(blank=True, upload_to='profile_image')

    def __str__(self):
        return str(self.stud_id)


# a class in relation to borrowed books
# it has a foreign key in book and student for referencing book and student
# stud_id is used to recognise student
# if book is returned corresponding tuple is deleted from database
class Borrower(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.student.name+ 'borrowed' + self.book.title


class Reviews(models.Model):
    reviews = models.CharField(max_length=100,default='none')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    CHOICES = (
        ('0', '0'),
        ('.5', '.5'),
        ('1', '1'),
        ('1.5', '1.5'),
        ('2', '2'),
        ('2.5', '2.5'),
        ('3', '3'),
        ('3.5', '3.5'),
        ('4', '4'),
        ('4.5', '4.5'),
        ('5', '5')
    )
    rating = models.CharField(max_length=3, choices=CHOICES, default='2')

