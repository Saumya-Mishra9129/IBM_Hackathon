from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm
import json
import os
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

naturalLanguageUnderstanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='xFeZQQNYZ4znykw2l4rp6YL3Vl1Mo2Ombnm9kzZwVWDa',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)

model_id = '7c9e2d43-400d-49e3-adae-1f32f0290665'

def api(request, fileurl):
    print(fileurl)
    text = open(fileurl,'r').read()

    response = naturalLanguageUnderstanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(model=model_id))).get_result()
    print(response)
    #print(json.dumps(response, indent=2))

    # with open('upload.txt','U') as f:
    # filedata = f.read()
    for i in range(len(response.get('entities'))):
        x = response.get('entities')[i].get('text')
        while x in text:
            text = text.replace(x, '*' * len(x))
            #print(text)
    with open('./media/upload1.txt', 'w') as new:
        new.write(text)
    print("return")
    txt = "/media/upload1.txt"
    return txt


def home(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        uploaded_file_url = api(request, uploaded_file_url)
        print("tcfascyfycglcsacsdcbsadcsk")
        print(uploaded_file_url)
        return render(request, 'core/home.html', {'uploaded_file_url': uploaded_file_url })
    return render(request, 'core/home.html')

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        print("running")
        myfile = request.FILES['myfile']

        url = os.getcwd()
        url = url.replace(os.sep, '/')
        print(url)
        url = url + '/media/' + myfile.name
        print(url)
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        #print(uploaded_file_url)
        # url = '/media/' + myfile
        txt = api(request,url)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': txt
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
