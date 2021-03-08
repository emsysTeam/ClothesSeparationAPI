from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Image
from .forms import UploadForm
# Create your views here.
from django.conf import settings
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
            # print(form.save().id)
            print(os.listdir(settings.MEDIA_ROOT))
            image_id = form.save().id
            print(os.listdir('/home/ubuntu/media/images/'))
            print(3)
            print(form)
            return redirect('image_show', image_id)
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

def image_show(request, image_id):
    image = Image.objects.filter(id=image_id)
    print(image.values())
    return render(request, 'ClothesSeparationAPI/show.html', {
        'image' : image
    })
