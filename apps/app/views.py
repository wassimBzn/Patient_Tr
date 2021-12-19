# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from apps.app.models import *
from apps.app.forms import AddPatientForm
from apps.app.filters import PatientFilter
import xlwt
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render


@login_required(login_url="/login/")
class ContactListView(ListView):
    paginate_by = 2
    model = Patient


def Export_excel(request):
    columns = ['nom', 'prenom', 'date_de_naissance', 'lieu_de_naissance', 'profession', 'adresse', 'cin',
               'statut_matrimonial', 'telephone', 'tabagisme', 'antecedentes', 'medication_en_cours', 'plaintes',
               'reste_de_examen', 'T', 'PA', 'Slo', 'RC', 'explorations', 'traitement', 'evolution']
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=patients{}.xls'.format(str(datetime.datetime.now()))
    patients = Patient.objects.all()
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('Patients')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for columns_num in range(len(columns)):
        sheet.write(row_num, columns_num, columns[columns_num], font_style)
    font_style = xlwt.XFStyle()
    for patient in patients:
        row_num += 1
        patient_list = [patient.nom, patient.prenom, patient.date_de_naissance, patient.lieu_de_naissance,
                        patient.profession, patient.adresse, patient.cin, patient.statut_matrimonial, patient.telephone,
                        patient.tabagisme, patient.antecedentes, patient.medication_en_cours, patient.plaintes,
                        patient.reste_de_examen, patient.T, patient.PA, patient.Slo, patient.RC, patient.explorations,
                        patient.traitement, patient.evolution]
        for columns_num in range(len(patient_list)):
            sheet.write(row_num, columns_num, patient_list[columns_num], font_style)
    wb.save(response)

    return response


def index(request):
    patients = Patient.objects.get_queryset().order_by('Nom')
    msg = ''
    success = ''
    MyFilter = PatientFilter(request.GET, queryset=patients)
    patients = MyFilter.qs
    paginator = Paginator(patients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "./index.html",
                  {'page_obj': page_obj, "MyFilter": MyFilter, "patients": patients, "msg": msg, "success": success})


def charts_patient(request):
    context = {}
    patients = Patient.objects.all()
    msg = ''
    success = ''
    html_template = loader.get_template('charts-morris.html')
    T_Number = Patient.objects.filter(T=True).count()
    PA_Number = Patient.objects.filter(PA=True).count()
    SLO_Number = Patient.objects.filter(Slo=True).count()
    RC_Number = Patient.objects.filter(RC=True).count()
    context['T_Number'] = T_Number
    context['PA_Number'] = PA_Number
    context['SLO_Number'] = SLO_Number
    context['RC_Number'] = RC_Number
    context['Patients_Number'] = patients.count()
    context['patients'] = patients
    context['msg'] = msg
    context['success'] = success
    return render(request, "./charts-morris.html", context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


def delete_patient(request, pk):
    msg = None
    success = False
    html_template = loader.get_template('index.html')
    patient = Patient.objects.get(Cin=pk)

    try:
        patient.delete()
        msg = "patient{} has been successfully deleted"
        success = False
    except:
        msg = "patient {} has not been deleted! ".format(patient.Nom)
        success = False
    context = {}
    return HttpResponseRedirect("/")


def view_patient(request, pk):
    msg = 'Success'
    try:
        patient = Patient.objects.get(Cin=pk)
    except:
        msg = 'Patient does not exists!'
        success = False
        return HttpResponseRedirect("/")

    return render(request, "./view_patient.html", {"msg": msg, "patient": patient})


def update_patient(request, pk):
    msg = None
    success = False
    try:
        patient = Patient.objects.get(Cin=pk)
        if request.method == "POST":
            form = AddPatientForm(request.POST or None)
            if form.is_valid():
                Nom = form.cleaned_data.get("nom")
                Prenom = form.cleaned_data.get("prenom")
                Date_de_naissance = form.cleaned_data.get("date_de_naissance")
                Lieu_de_naissance = form.cleaned_data.get("lieu_de_naissance")
                Profession = form.cleaned_data.get("profession")
                Adresse = form.cleaned_data.get("adresse")
                Cin = form.cleaned_data.get("cin")
                Sexe = form.cleaned_data.get("sexe")
                Statut_matrimonial = form.cleaned_data.get("statut_matrimonial")
                Telephone = form.cleaned_data.get("telephone")
                patient.Nom = Nom
                patient.Prenom = Prenom
                patient.Date_de_naissance = Date_de_naissance
                patient.Lieu_de_naissance = Lieu_de_naissance
                patient.Profession = Profession
                patient.Adresse = Adresse
                patient.Cin = Cin
                patient.Sexe = Sexe
                patient.Statut_matrimonial = Statut_matrimonial
                patient.Telephone = Telephone

                patient.save()
                msg = 'Patient Already exists!'
                success = False
                return HttpResponseRedirect("/")
            else:
                success = False
                msg = 'Form is not valid: {}'.format(form.errors)
        else:
            form = AddPatientForm(initial={'nom': patient.Nom,
                                           'prenom': patient.Prenom,
                                           'date_de_naissance': patient.Date_de_naissance,
                                           'lieu_de_naissance': patient.Lieu_de_naissance,
                                           'profession': patient.Profession,
                                           'adresse': patient.Adresse,
                                           'cin': patient.Cin,
                                           'sexe': patient.Sexe,
                                           'statut_matrimonial': patient.Statut_matrimonial,
                                           'telephone': patient.Telephone,})

            patient = Patient.objects.get(Cin=pk)
    except:
        form = AddPatientForm()
        msg = 'Patient does not exists!'
        success = False
        return HttpResponseRedirect("/")
    # return redirect("/login/")


    return render(request, "./update_patient.html", {"success":success,"msg":msg,"form": form, "patient": patient})


def add_patient(request):
    msg = None
    success = False
    if request.method == "POST":
        form = AddPatientForm(request.POST or None)
        if form.is_valid():
            Nom = form.cleaned_data.get("nom")
            Prenom = form.cleaned_data.get("prenom")
            Date_de_naissance = form.cleaned_data.get("date_de_naissance")
            Lieu_de_naissance = form.cleaned_data.get("lieu_de_naissance")
            Profession = form.cleaned_data.get("profession")
            Adresse = form.cleaned_data.get("adresse")
            Cin = form.cleaned_data.get("cin")
            Sexe = form.cleaned_data.get("sexe")
            Statut_matrimonial = form.cleaned_data.get("statut_matrimonial")
            Telephone = form.cleaned_data.get("telephone")
            try:
                patient = Patient.objects.get(Cin=Cin)
                msg = 'Patient Already exists!'
                success = False
                return render(request, "./add_patient.html", {"form": form, "msg": msg, "success": success})

            except:
                new_patient = Patient(Nom, Prenom, Date_de_naissance, Lieu_de_naissance, Profession, Adresse, Cin, Sexe,
                                      Statut_matrimonial, Telephone)
                new_patient.save()
                msg = 'Patient has been successfully created !'
                success = True
                print("An exception occurred")
                form = AddPatientForm()
                return render(request, "./add_patient.html", {"form": form, "msg": msg, "success": success})
            # return redirect("/login/")
        else:
            msg = form.errors
    else:
        form = AddPatientForm()

    return render(request, "./add_patient.html", {"form": form, "msg": msg, "success": success})
