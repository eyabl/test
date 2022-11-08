import csv

import openpyxl as openpyxl
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
import pandas as pd
from .models import LOVGest, LOVGestForm, NewUserForm, iexps
from django.contrib.auth.models import User


@login_required
def red(request):
    return redirect('dashboard')


@login_required
def index(request):
    return render(request, 'index.html', {'ges': LOVGest.objects.all()[:5], 'nbs':
                                          len(LOVGest.objects.all())})


@login_required
def load(request):
    if request.method == 'POST':
        df = pd.read_excel(r'files/CR_EXPLOIT_TRANSDEV-2022-V04.xlsm', sheet_name="LOVGest")
        for a in range(0, len(df.to_dict()['Code \nGestionnaire'])):
            if not LOVGest.objects.filter(CodeGestionnaire=df.to_dict()['Code \nGestionnaire'][a]).exists():
                LOVGest(CodeGestionnaire=df.to_dict()['Code \nGestionnaire'][a],
                        NomSociete=df.to_dict()['Nom Société'][a]).save()

        return render(request, 'lovgest.html', {'ges': LOVGest.objects.all().order_by('-id'),
                                                'message': 'Importation avec succès'})
    return redirect('lovgest')


@login_required
def load2(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file)
            # databook = Databook()
            return render(request, 'open.html', {
                'uploaded_file_url': uploaded_file_url.ur
            })
            empexceldata = pd.read_csv("." + excel_file, encoding='utf-8', error_bad_lines=False)
            print(type(empexceldata))
            dbframe = empexceldata
            # for dbframe in dbframe.itertuples():
            # fromdate_time_obj = dt.datetime.strptime(dbframe.DOB, '%d-%m-%Y')
            # dbframe.qualification
            # print(type(obj))
            # obj.save()

            return render(request, 'open.html', {
                'uploaded_file_url': excel_file
            })
    except Exception as identifier:
        print(identifier)

    return render(request, 'open.html', {})


@login_required
def open(request):
    if "GET" == request.method:
        return render(request, 'open.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        return render(request, 'open.html', {"excel_data": excel_data})


@login_required
def lovgest(request):
    return render(request, 'lovgest.html', {'ges': LOVGest.objects.all().order_by('-id')})


@login_required
def update(request, id):
    obj = LOVGest.objects.get(id=id)
    form = LOVGestForm(instance=obj)
    if request.method == 'POST':
        form = LOVGestForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
    return render(request, 'update.html', {'form': form})


@login_required
def add(request):
    form = LOVGestForm()
    if request.method == 'POST':
        form = LOVGestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lovgest')
    return render(request, 'add.html', {'form': form})


@login_required
def delete(request, id):
    LOVGest.objects.get(id=id).delete()
    return redirect('lovgest')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, User.objects.get(username=form.cleaned_data['username']))
            return redirect('dashboard')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"form": form})


@login_required
def iexp(request, id):
    return render(request, 'iexp.html', {'iexp': iexps.objects.filter(numFichier=id), 'links': range(1, 10)})


def loadiexp(request):
    for i in range(1, 10):
        try:
            df = pd.read_excel(r'files/2 - Fichier de travail des KPI 202208.xlsx', sheet_name="IEXP" + str(i))
            df = df.to_dict()
            keys = list(df.keys())
            for a in range(2, len(df[keys[0]]) - 1):
                if not iexps.objects.filter(numFichier=i,
                                            etape=df[keys[0]][a],
                                            traitement=df[keys[1]][a],
                                            duree=df[keys[4]][a]).exists():
                    iexps(numFichier=i,
                          etape=df[keys[0]][a],
                          traitement=df[keys[1]][a],
                          duree=df[keys[4]][a]).save()
        except:
            pass
    return redirect('iexp', id=1)
