from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib import messages
from .models import Image
from .forms import UploadForm
# Create your views here.
from django.conf import settings
from .tasks import startAPI
import celery
import os
# def index(request):
#     """
#     pybo 질문 목록 출력
#     """
#     question_list = Question.objects.order_by('-create_date')
#     print(list(question_list))
#     print(Question.objects.all().values())
#     context = {'question_list': question_list}
#     print(context)
#     return render(request, 'ClothesSeparationAPI/question_list.html', context)

def index(request):
    return HttpResponse('Hello world')

def upload(request):
    print(request)
    print(settings.MEDIA_ROOT)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        print(1)
        print(request.FILES['image'])
        print(type(request.FILES['image'].name))
        print(request.FILES['image'].content_type)
        print(request.FILES['image'].size)
        
        if form.is_valid():
            # startAPI.delay(2)
            # print(form.save().id)
            print(os.listdir(settings.MEDIA_ROOT))
            image_id = form.save().id
            print(os.listdir('/home/ubuntu/media/images/'))
            print(3)
            image = Image.objects.filter(id=image_id)
            print(image.values())
            image_name = str(list(image.values())[0]['image'])
            print(image_name)
            print(type(image_name))
            task_id = startAPI.delay(str(settings.MEDIA_ROOT) + '/' + image_name)
            print(form)
            # messages.success(request, task_id)
            # 세션 부여
            # request.session['task_id'] = task_id
            return redirect('image_show', image_id, task_id)
            # return render(request, 'imaging/list.html', {"foo": "bar"})
    else:
        form = UploadForm()
    return render(request, 'ClothesSeparationAPI/upload.html', {
        'form' : form
    })

def image_list(request):
    print(request)
    return render(request, 'ClothesSeparationAPI/list.html')

# def image_show(request, image_id):
#     return HttpResponse(f'image id: {image_id}')

def image_show(request, image_id, task_id):
    image = Image.objects.filter(id=image_id)
    # redirect : url에 붙어오는 값
    print('task ID : ', task_id)
    # issue : 실제 task_id와 일치하지 않더라도 result.status가 PENDING 을 반환함
    result = celery.result.AsyncResult(task_id)
    print('task STATUS : ', result.status)

    # 세션 확인
    # session_id = request.session.session_key
    # session_value = request.session['task_id']
    # print(session_value)

    # storage = messages.get_messages(request)
    # for message in storage:
    #     print('message : ', celery.result.AsyncResult(message))
    # print(image.values())
    # image_name = str(list(image.values())[0]['image'])
    # print(image_name)
    # print(type(image_name))
    # startAPI.delay(str(settings.MEDIA_ROOT) + '/' + image_name)
    return render(request, 'ClothesSeparationAPI/show.html', {
        'image' : image,
        'task_status' : result.status
    })
