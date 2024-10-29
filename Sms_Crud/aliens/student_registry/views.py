import base64
import json
import pdb
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from .forms import *
from django.contrib.auth import authenticate,login,logout
from .models import Students

# Create your views here.

def student_create(request):
    if request.method == 'POST':
        form_data_json= request.POST.get('form')
        if form_data_json:
            form_data = json.loads(form_data_json)
            
        for data in form_data:
            student = Students.objects.create(
                fullname=data['fullname'],
                role_no=data['role_no'],
                email=data['email'],
                mobile=data['mobile'],
                degree=data['degree'],
                dept=data['dept']
            )
            student.save()
        messages.success(request,"Information Added Successfully")
        return redirect('student_details')
    return render(request,'create.html')

    #     return JsonResponse({'message': 'Data saved successfully.'})

    # return JsonResponse({'error': 'Invalid request method.'})
    # # if request.method == 'POST':
    #     print(request.POST)
    #     form = StudentForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         print("hi")
    #         messages.success(request,"Information Added Successfully")
    #         return redirect('student_details')
    #     return render(request,'create.html',{'form':form})
    # else:
    #     form=StudentForm()
    # return render(request,'create.html',{'form':form})

def bundlesave(request):
    my_dict = request.POST
    token = {}
    updateddict = {}
    for i in my_dict:
        key = i[8:][:-1]
        val = list[i]
        
        updateddict[key] = [val]
        
    print(updateddict) 
    form = StudentForm(updateddict)
    print(form)
    data = {"message": "Hello"}
    if form.is_valid():
        print("shhdfsfdst------------------------------------------------")
        form.save()
        
        return JsonResponse(data)
    return JsonResponse(data)

def student_update(request,id):
    student = Students.objects.get(id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request,"Information Updated Successfully")
            return redirect('student_details')
    else:
        form=StudentForm(instance=student)
    return render(request,'edit.html',{'form':form})


@never_cache
def student_list(request):
    if request.user.is_authenticated:
        data = Students.objects.all()
        return render(request,'list.html',{'data':data})
    else:
        return redirect('sign_in')
    
def student_delete(request,id):
    student=Students.objects.get(id=id)
    student.delete()
    #messages.success(request,"Information deleted Successfully.")
    return redirect('student_details')
    

def register_page(request):
    if request.user.is_authenticated:
        return redirect('student_details')
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,"Username already Taken!")
            return redirect('register')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username= username
        )
        user.set_password(password)
        user.save()

        messages.info(request, "Account Create Successfully!")
        return redirect('sign_in')
    return render(request,'register.html')

@never_cache
def login_page(request):
    if request.user.is_authenticated:
        return redirect('student_details')
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('student_details')
        else:
            messages.add_message(request, messages.ERROR, "Username and password do not match.")
    else:
        form = AuthenticationForm()  # Create an instance of the form for GET requests
    return render(request,'login.html', {'form': form})

def logout_page(request):
    logout(request)
    return redirect('sign_in')


from openpyxl import Workbook
from .models import Students

def export_to_xl(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition']='attachment; filename = "stddata.xlsx"'
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Student Data"
    
    header = ['Full Name','Roll Number','Email ID','Mobile Number','Degree','Department']
    worksheet.append(header)
    
    students = Students.objects.all()
    for student in students:
        worksheet.append([student.fullname,student.role_no,student.email,student.mobile,student.degree,student.dept])
        
    workbook.save(response)
    return response

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.http import FileResponse


def export_to_pdf(request):
    student = Students.objects.all() 
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    row_height = 30
    dataumn_width = 150
    
    data = [
        ['Full Name','Roll Number','Email ID','Mobile Number','Degree','Department']
    ]
    for student in Students.objects.all():
        data.append([student.fullname,
                      student.role_no,
                      student.email,
                      student.mobile,
                      student.degree,
                      student.dept])
    x = 50
    y = 750
    for row in data:
        for item in row:
            p.drawString(x,y,str(item))
            x += dataumn_width
        x = 50
        y -= row_height
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=True,filename="stddata.pdf")


from django.core.mail import EmailMessage


def export_and_email_pdf(request,id):
    student = get_object_or_404(Students, id=id)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    row_height = 30
    column_width = 150

    data = [
        ['Full Name', 'Roll Number', 'Email ID', 'Mobile Number', 'Degree', 'Department'],
        [student.fullname, student.role_no, student.email, student.mobile, student.degree, student.dept]
    ]

    x = 50
    y = 750
    for row in data:
        for item in row:
            p.drawString(x, y, str(item))
            x += column_width
        x = 50
        y -= row_height

    p.save()
    buffer.seek(0)

    subject = 'Student Details'
    message = 'Please find attached the details of the student.'
    from_email = 'pavithranpavithran608@gmail.com'

    email = EmailMessage(
        subject,
        message,
        from_email,
        [student.email],  # Assuming email field exists in your Students model
    )
    email.attach('student_details.pdf', buffer.getvalue(), 'application/pdf')
    email.send(fail_silently=False)

    return FileResponse(buffer, as_attachment=True, filename="student_details.pdf")


from django.db.models import Q

def search_info(request):
    if request.method == "GET":
        search_term = request.GET.get('search')
        if search_term:
            query = Q(fullname__icontains=search_term) | Q(role_no__icontains=search_term) | Q(email__icontains=search_term) | Q(mobile__icontains=search_term) | Q(degree__icontains=search_term) | Q(dept__icontains=search_term)
            data = Students.objects.filter(query)
        else:
            data = Students.objects.all()
            
        return render(request, 'list.html', {'data': data})

from .forms import FileUploadForm
from .models import Document

def upload_file(request):
    file_data = b''
    if request.method == "POST":
        form = FileUploadForm(request.POST , request.FILES)
        if form.is_valid():
            new_file = Document(myfile = request.FILES['myfile'])
            new_file.save()
            messages.success(request,"File Uploaded Successfully")
            return redirect("list_file")
    else:
        form = FileUploadForm()    
    return render(request,'upload.html',{'form':form, 'file_data':file_data})

import os

def filelist(request):
    documents = Document.objects.all()
    data = []

    for document in documents:
        file_path = document.myfile.path
        file_exists = os.path.exists(file_path)

        # Only include documents whose files exist
        if file_exists:
            data.append(document)

    return render(request, 'filelist.html', {'data': data})


from django.shortcuts import get_object_or_404

def viewfile(request, id):
    document = get_object_or_404(Document, id=id)
    temp_name = None
    
    if document.myfile:
        with document.myfile.open(mode='rb') as file:
            file_data = base64.b64encode(file.read()).decode('utf-8')
            file_ext = document.myfile.name.split('.')[-1].lower()
            print(file_ext)
            supported_ext = 'pdf', 'jpg', 'jpeg', 'png', 'gif'
            if file_ext in supported_ext:
                print(file_ext)
                # Render the appropriate template based on the file type
                temp_name = 'viewfile.html' if file_ext == 'pdf' else 'viewimage.html'
            else:
                file_data = None  # Unsupported file type
                print(file_data)
    else:
        file_data = None

    return render(request, temp_name, {'file_data': file_data})