# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from apps.app.models import *
from apps.app.forms import AddPatientForm


@login_required(login_url="/login/")

def index(request):
    patients=Patient.objects.all()
    msg=''
    success=''
    html_template = loader.get_template('index.html')
    return render(request, "./index.html", {"patients": patients, "msg": msg, "success": success})


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


def  updade_patient(request, pk):
    msg = None
    success = False
    form = AddPatientForm()

    return render(request, "./update_patient.html", {"form": form, "msg": msg, "success": success})

def  delete_patient(request, pk):
    msg = None
    success = False
    html_template = loader.get_template('index.html')
    patient=Patient.objects.get(cin=pk)

    try:
        patient.delete()
        msg = "patient{} has been successfully deleted"
        success = False
    except:
        msg = "patient {} has not been deleted! ".format(patient.nom)
        success = False
    context={}
    return HttpResponseRedirect("/")

def add_patient(request):
    msg = None
    success = False
    if request.method == "POST":
        form = AddPatientForm(request.POST or None)
        if form.is_valid():
            nom = form.cleaned_data.get("nom")
            prenom = form.cleaned_data.get("prenom")
            date_de_naissance = form.cleaned_data.get("date_de_naissance")
            lieu_de_naissance = form.cleaned_data.get("lieu_de_naissance")
            profession = form.cleaned_data.get("profession")
            adresse = form.cleaned_data.get("adresse")
            cin = form.cleaned_data.get("cin")
            statut_matrimonial = form.cleaned_data.get("statut_matrimonial")
            telephone = form.cleaned_data.get("telephone")
            tabagisme = form.cleaned_data.get("tabagisme")
            antecedentes = form.cleaned_data.get("antecedentes")
            medication_en_cours = form.cleaned_data.get("medication_en_cours")
            plaintes = form.cleaned_data.get("plaintes")
            reste_de_examen = form.cleaned_data.get("reste_de_examen")
            T = form.cleaned_data.get("T")
            PA = form.cleaned_data.get("PA")
            Slo = form.cleaned_data.get("Slo")
            RC = form.cleaned_data.get("RC")
            explorations = form.cleaned_data.get("explorations")
            traitement = form.cleaned_data.get("traitement")
            evolution = form.cleaned_data.get("evolution")
            try:
                patient = Patient.objects.get(cin=cin)
                msg = 'Patient Already exists!'
                success = False
                return render(request, "./add_patient.html", {"form": form, "msg": msg, "success": success})

            except:
                new_patient=Patient(nom,prenom,date_de_naissance,lieu_de_naissance,profession,adresse,cin,statut_matrimonial,telephone,tabagisme,antecedentes,medication_en_cours,plaintes,reste_de_examen,T,PA,Slo,RC,explorations,traitement,evolution)
                new_patient.save()
                msg = 'Patient has been successfully created !'
                success = True
                print("An exception occurred")
                form = AddPatientForm()
                return render(request, "./add_patient.html", {"form": form, "msg": msg, "success": success})
            # return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = AddPatientForm()

    return render(request, "./add_patient.html", {"form": form, "msg": msg, "success": success})
