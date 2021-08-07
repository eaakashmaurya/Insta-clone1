from django.http import HttpResponse
from django.views.generic import DetailView, FormView, UpdateView
from .forms import SandhiForm, DictForm, SandhiSplitterForm
from django.shortcuts import render
from .apis import sandhi_api, sans_to_eng_api, eng_to_sans_api, sandhi_splitter_api

def index(request):
    return render(request, 'tools/basic.html')

def sandhi(request):

    if request.method == 'POST':
        form = SandhiForm(request.POST)
        if form.is_valid():

            txt1 = form.cleaned_data['txt1']
            txt2 = form.cleaned_data['txt2']

            result = txt1 + " + " + txt2 + " = "
            result += sandhi_api(txt1, txt2)

            return render(request, 'tools/sandhi.html', {'form' : form, 'result': result})

    form = SandhiForm()
    return render(request, 'tools/sandhi.html', {'form' : form, 'result':False})


def dictionary(request):

    if request.method == 'POST':
        form = DictForm(request.POST)
        if form.is_valid():

            txt = form.cleaned_data['txt']
            type = form.cleaned_data['type']

            if (type == "sans"):
                result = sans_to_eng_api(txt)
            else:
                result = eng_to_sans_api(txt)

            return render(request, 'tools/dictionary.html', {'form' : form, 'result': result})

    form = DictForm()
    return render(request, 'tools/dictionary.html', {'form' : form, 'result':False})

def sandhi_splitter(request):

    if request.method == 'POST':
        form = SandhiSplitterForm(request.POST)
        if form.is_valid():

            txt = form.cleaned_data['txt']
            type = form.cleaned_data['type']

            result = sandhi_splitter_api(txt, type)

            return render(request, 'tools/sandhi_splitter.html', {'form' : form, 'result': result})

    form = SandhiSplitterForm()
    return render(request, 'tools/sandhi_splitter.html', {'form' : form, 'result':False})

def resources(request):
    return render(request, 'tools/resources.html')