from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.

def index(request):
    """
    pybo 질문 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    print(list(question_list))
    print(Question.objects.all().values())
    context = {'question_list': question_list}
    print(context)
    return render(request, 'ClothesSeparationAPI/question_list.html', context)

def index2(request):
    return HttpResponse("DcLab 서버 입니다.")

