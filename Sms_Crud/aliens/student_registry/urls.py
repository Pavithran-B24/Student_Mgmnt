from django.urls import path
from . import views

urlpatterns=[
    path('list/',views.student_list,name="student_details"),
    path('register/',views.register_page,name="register"),
    path('login/',views.login_page,name="sign_in"),
    path('logout/',views.logout_page,name="sign_out"),
    path('create/',views.student_create,name="create"),
    path('edit/<int:id>/',views.student_update,name="edit"),
    path('delete/<int:id>/',views.student_delete,name="delete"),
    path('export/',views.export_to_xl,name="export_xl"),
    path('export-pdf/',views.export_to_pdf,name="export_pdf"),
    path('export-pdfmail/<int:id>/',views.export_and_email_pdf,name="export_pdfmail"),
    path('save/',views.bundlesave,name="save_info"),
    path('search/',views.search_info,name="search_std"),
    path('upload/',views.upload_file,name="upload"),
    path('filelist/',views.filelist,name="list_file"),
    path('viewfile/<int:id>/',views.viewfile,name="file_view"),
         
]