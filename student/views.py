from django.shortcuts import render
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from student.models import StuInfo


#show all the student info
def show_all(request):
    student_list = StuInfo.objects.all()
    return render(request, 'show_all.html', {'student_list': student_list})

#direct to insert page
def insert_page(request):
    return render(request, 'insert_page.html')


#receive post form insert_page
#insert in to databas
#redirect to show all page
@csrf_exempt
def insert(request):
    if request.POST:
        stu_id = request.POST.get('stu_id')
        #if post contain stu_id
        if stu_id != '':
            stu_id = int(stu_id)
        stu_name = request.POST.get('stu_name')
        stu_tel = request.POST.get('stu_tel')
        stu_mail = request.POST.get('stu_mail')
        stu_want = request.POST.get('stu_want')
        resume_path = request.POST.get('resume_path')
        my_meet = int(request.POST.get('my_meet'))
        if stu_id == '':
            #if post dostn't contain stu_id
            new_student = StuInfo(stu_name = stu_name,
                                  stu_tel = stu_tel,
                                  stu_mail = stu_mail,
                                  stu_want = stu_want,
                                  resume_path = resume_path,
                                  my_meet = my_meet)
        else:
            #if post contain stu_id
            new_student = StuInfo(stu_id, stu_name, stu_tel, stu_mail,
                                   stu_want, resume_path, my_meet)
        new_student.save()
        return show_all(request)


#direct to delete page
def delete_page(request):
    return render(request, 'delete_page.html')

#receive post from delete page
#delte the student infor in database
#redirect to show all page
@csrf_exempt
def delete(request):
    if request.POST:
        stu_id = int(request.POST.get('stu_id'))
        try:
            delete_student = StuInfo.objects.all().get(stu_id=stu_id)
            delete_student.delete()
        except StuInfo.DoesNotExist:
            raise Http404
    return show_all(request)



#direct to page select
def select_page(request):
    return render(request, 'select_page.html')

#receive post from select page
#select student infor from database
#redirect to page show one  if stu_id is not empty
@csrf_exempt
def select(request):
    if request.POST:
        stu_id = request.POST.get('stu_id')
        if stu_id == '':
            #if stu_id is empty
            return select_page(request)
        else:
            #if stu_id isn't empty
            stu_id = int(stu_id)
            try:
                select_student = StuInfo.objects.all().get(stu_id=stu_id)
                return render(request, 'show_one.html', {'student': select_student})
            except StuInfo.DoesNotExist:
                raise Http404;



#receive post form page show one
#direct to page update_page
@csrf_exempt
def update_page(request):
    if request.POST:
        stu_id = request.POST.get('stu_id')
        if stu_id == '':
            #if stu_id is empty
            return select_page(request)
        else:
            #if stu_id isn't empty
            stu_id = int(stu_id)
            try:
                select_student = StuInfo.objects.all().get(stu_id=stu_id)
                return render(request, 'update_page.html', {'student': select_student})
            except StuInfo.DoesNotExist:
                raise Http404


#receive post from update page
#update student infor in database
#redirect to show all page
@csrf_exempt
def update(request):
    if request.POST:
        post = request.POST
        stu_id = post.get('stu_id')
        if stu_id != '':
            stu_id = int(stu_id)
            try:
                update_student = StuInfo.objects.all().filter(stu_id=stu_id)
                stu_name = post.get('stu_name')
                stu_tel = post.get('stu_tel')
                stu_mail = post.get('stu_mail')
                stu_want = post.get('stu_want')
                resume_path = post.get('resume_path')
                my_meet = post.get('my_meet')
                update_student.update(stu_name = stu_name,
                                      stu_tel = stu_tel,
                                      stu_mail = stu_mail,
                                      stu_want = stu_want,
                                      resume_path = resume_path,
                                      my_meet = my_meet)
            except StuInfo.DoesNotExist:
                raise Http404
    return show_all(request)


