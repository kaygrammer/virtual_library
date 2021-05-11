from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
import datetime


# Homepage
def index(request):
    return render(request, 'index.html',)


# Return List of books
def book_list_view(request):
    book_list = Book.objects.all()
    return render(request, 'catalog/book_list.html', locals())

# return list of student
@login_required
def student_book_list_view(request):
    student = Student.objects.get(stud_id=request.user)
    bor = Borrower.objects.filter(student=student)
    book_list =[]
    for b in bor:
        book_list.append(b.book)
    return render(request, 'catalog/book_list.html', locals())


# view to return detail of a particular book
# it accept an id. i.e primary key of book to identify it
# get_object_404 if object is not found then return to the 404 server
# locals return a dictionary local variable

def book_detail_view(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews = Reviews.objects.filter(book=book).exclude(review='none')
    try:
        stu = Student.objects.get(stu_id=request.user)
        rr = Reviews.object.get(review='none')
    except:
        pass
    return render(request, 'catalog/book_detail.html', locals())


@login_required
def book_create(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'catalog/form.html', locals())


@login_required
def book_update(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Book.objects.get(id=pk)
    form = BookForm(instance=id)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            obj.save()
            return redirect(request, 'catalog/form.html', locals())


@login_required
def book_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return redirect('index')


@login_required
def student_request_issue(request, pk):
    obj = Book.objects.get(id=pk)
    stu = Student.objects.get(stu_id=request.user)
    s = get_object_or_404(Student, stu_id=str(request.user))
    if s.total_books_due:
        message = "book has been issued, you can collect book from library"
        a = Borrower()
        a.student = s
        a.book = obj
        a.issue_date = datetime.datetime.now()
        obj.available_copies = obj.available_copies - 1
        obj.save()
        a.save()
    else:
        message = "you have exceeded limit."
    return render(request, 'catalog/result.html', locals())


@login_required
def student_create(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            s = form.cleaned_data
            form.save()
            u = User.objects.get(username=s)
            s = Student.objects.get(stud_id=s)
            u.email = s.email
            u.save()
            return redirect('index')
    return render(request, 'catalog/form.html', locals())


@login_required
def student_update(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Student.objects.get(id=pk)
    form = StudentForm(instance=obj)
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('index')
    return render(request, 'catalog/form.html', locals())


@login_required
def student_delete(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    obj.delete()
    return redirect('index')


@login_required
def student_list(request):
    students = Student.objects.get()
    return render(request, 'catalog/student_list.html', locals())


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, id=pk)
    books = Borrower.objects.filter(student=student)
    return render(request, 'catalog/student_detail.html', locals())


@login_required
def ret(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Borrower.objects.get(id=pk)
    book_pk = obj.book.id






