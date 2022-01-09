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
from apps.app.forms import *
from apps.app.filters import *
import xlwt
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from textwrap import wrap
import math

def Export_Patient_pdf(request,patient_id,):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    patient=Patient.objects.get(Cin=patient_id)

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.drawCentredString(300, 800, "Information Generale d'un patient")
    p.drawRightString(550, 780, "Dr.Taher Ben Salem")
    p.line(40, 770, 560, 770)
    w=50
    h=100

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.drawString(w, h, " ");h+=350
    p.drawString(w, h, "Profession : {}".format(patient.Profession));h+=30
    p.drawString(w, h, "Telephone : {}".format(patient.Telephone));h+=30
    p.drawString(w, h, "Statut_matrimonial : {}".format(patient.Statut_matrimonial));h+=30
    p.drawString(w, h, "Sexe : {}".format(patient.Sexe));h+=30
    p.drawString(w, h, "Cin : {}".format(patient.Cin));h+=30
    p.drawString(w, h, "Adresse : {}".format(patient.Adresse));h+=30
    p.drawString(w, h, "Lieu_de_naissance : {}".format(patient.Lieu_de_naissance));h+=30
    p.drawString(w, h, "Date_de_naissance : {}".format(patient.Date_de_naissance));h+=30
    p.drawString(w, h, "Prenom : {}".format(patient.Prenom));h+=30
    p.drawString(w, h, "Nom: {}".format(patient.Nom));h+=30
# Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
def write_item_in_pdf(p,x,y,fieldName,Fieldvalue):
    #get the length of the string
    length_of_string = len(str(Fieldvalue))
    #75 is the max length of the line
    #if we reach the max we should come back to the line
    #if it's under 75  we write the line as it is
    if y <= 50:
        p.showPage()
        p.drawCentredString(300, 800, " ")
        p.drawRightString(550, 780, "Dr.Taher Ben Salem")
        p.line(40, 770, 560, 770)
        x=50
        y=735
    if length_of_string < 56:
        p.setFont('Helvetica-Bold', 10)
        p.drawString(x+10, y, "{} :".format(fieldName))
        p.setFont('Helvetica', 10)
        #full page = 595 , max letters per page= 89 , 595/89= 6.6 + add some numbers for beautifying,,,,56 max latters per line
        p.drawString(x+20+(23*6.6), y, " {}".format(Fieldvalue)); y-=20
    else:
        #max number of caracters per line
        cotient=56
        #else we should calculate how much lines we need
        number_of_lines= math.ceil(length_of_string/cotient)
        #split the value to list of words
        list_value_words=Fieldvalue.split(' ')
        #if we have a short word we write it as it is by concatinatin all the words together in the list
        if len(list_value_words) < 2 and number_of_lines > 1 :
            Line_list= [Fieldvalue[i:i+cotient] for i in range(0, len(Fieldvalue), cotient)]
        else:
            # concatinate the words together and write them and return to new line when >75 characters
            Line_list=[]
            line_length=0
            line=''
            for word in list_value_words:
                if line_length <=56:
                    line_length+=len(word)
                    line+=" "+word
                else:
                    line_length=0
                    Line_list.append(line)
                    line=''

        iteration=0
        #write the phrases saved into the pdf page
        for ln in Line_list:
            #if it is in the first line write the title field else no

            if iteration==0:
                p.setFont('Helvetica-Bold', 10)
                p.drawString(x+10, y, "{} :".format(fieldName))
                p.setFont('Helvetica', 10)
                p.drawString(x+10+(23*6.6), y, " {}".format(ln)); y-=20
            else:
                p.setFont('Helvetica', 10)
                p.drawString(x+10+(23*6.6), y, " {}".format(ln)); y-=20
            iteration+=1

    return p,x,y

def Export_Patient_consultation_pdf(request,patient_id,consultation_id):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    patient=Patient.objects.get(Cin=patient_id)
    consultation = Consultation.objects.get(id=consultation_id)
    habitude = Habitude.objects.get(id=consultation.Habitude_id)
    antecedentes = Antecedentes.objects.get(id=consultation.Antecedentes_id)
    examen_phisique = Examen_phisique.objects.get(id=consultation.Examen_phisique_id)
    examen_clinique = Examen_clinique.objects.get(id=consultation.Examen_clinique_id)
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.drawCentredString(300, 800, "Consultation d'un patient")
    p.drawRightString(550, 780, "Dr.Taher Ben Salem")
    p.line(40, 770, 560, 770)
    x=50
    y=735
    p.setFont('Helvetica-Bold', 12)
    p.drawString(x, y, "Information Generale");y-=30
    p, x, y = write_item_in_pdf(p, x, y, "Nom",patient.Nom)
    p, x, y = write_item_in_pdf(p, x, y, "Prénom",patient.Prenom)
    p, x, y = write_item_in_pdf(p, x, y, "Date de naissance",patient.Date_de_naissance)
    y -= 10
    p.setFont('Helvetica-Bold', 12)
    p.drawString(x, y, "Habitude"); y -= 30
    p, x, y = write_item_in_pdf(p, x, y, "Tabagisme",habitude.Tabagisme)
    p, x, y = write_item_in_pdf(p, x, y, "Nombre de Cigarette par jours",habitude.Nombre_de_Cigarette_par_jours)
    p, x, y = write_item_in_pdf(p, x, y, "Alcool",habitude.Alcool)
    p, x, y = write_item_in_pdf(p, x, y, "Allergies medicamenteuses",habitude.Allergies_medicamenteuses)
    p, x, y = write_item_in_pdf(p, x, y, "Autres", habitude.Autres)
    y -= 10
    p.setFont('Helvetica-Bold', 12)
    p.drawString(x, y, "Antecedentes"); y -= 30
    p, x, y = write_item_in_pdf(p, x, y, "Medicaux", antecedentes.Medicaux)
    p, x, y = write_item_in_pdf(p, x, y, "Chururgicaux", antecedentes.Chururgicaux)
    p, x, y = write_item_in_pdf(p, x, y, "Medications en cours", antecedentes.Medications_en_cours)
    y -= 10
    p.setFont('Helvetica-Bold', 12)
    p.drawString(x, y, "Examen_phisique");y-=30
    p, x, y = write_item_in_pdf(p, x, y, "plaintes", examen_phisique.plaintes)
    p, x, y = write_item_in_pdf(p, x, y, "Examen Cinetique", examen_phisique.Examen_Cinetique)
    p, x, y = write_item_in_pdf(p, x, y, "Reste de examen phisique", examen_phisique.Reste_de_examen_phisique)
    y -= 10
    p.setFont('Helvetica-Bold', 12)
    p.drawString(x, y, "Examen_clinique");y-=30
    p, x, y = write_item_in_pdf(p, x, y, "Temperature",examen_clinique.Temperature)
    p, x, y = write_item_in_pdf(p, x, y, "PA",examen_clinique.PA)
    p, x, y = write_item_in_pdf(p, x, y, "SRO",examen_clinique.SRO)
    p, x, y = write_item_in_pdf(p, x, y, "Poids",examen_clinique.Poids)
    p, x, y = write_item_in_pdf(p, x, y, "Taille",examen_clinique.Taille)
    p, x, y = write_item_in_pdf(p, x, y, "RC",examen_clinique.RC)
    p, x, y = write_item_in_pdf(p, x, y, "Reste de examen clinique",examen_clinique.Reste_de_examen_clinique)
    y -= 10
    p.setFont('Helvetica-Bold', 12)
    p.drawString(x, y, "Consultation");y-=30
    p, x, y = write_item_in_pdf(p, x, y, "Date de consultation", consultation.Date_de_consultation)
    p, x, y = write_item_in_pdf(p, x, y, "Explorations", consultation.Explorations)
    p, x, y = write_item_in_pdf(p, x, y, "Traitement", consultation.Traitement)
    p, x, y = write_item_in_pdf(p, x, y, "Evolution", consultation.Evolution)
    p, x, y = write_item_in_pdf(p, x, y, "Remarques", consultation.Remarques)
    p, x, y = write_item_in_pdf(p, x, y, "Prochaine Rondez vous", consultation.Prochaine_Rondez_vous)# Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()


    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

@login_required(login_url="/login/")
class ContactListView(ListView):
    paginate_by = 2
    model = Patient

def Export_excel_single_patient_consultations(request,patient_id):
    columns = ['Nom',
               'Prenom',
               'Date_de_naissance',
               'Habitude_Tabagisme',
               'Habitude_Nombre_de_Cigarette_par_jours',
               'Habitude_Alcool',
               'Habitude_Allergies_medicamenteuses',
               'Habitude_Autres',
               'Antecedentes_Medicaux',
               'Antecedentes_Chururgicaux',
               'Antecedentes_Medications_en_cours',
               'Examen_phisique_plaintes',
               'Examen_phisique_Examen_Cinetique',
               'Examen_phisique_Reste_de_examen_phisique',
               'Examen_clinique_Temperature',
               'Examen_clinique_PA',
               'Examen_clinique_SRO',
               'Examen_clinique_Poids',
               'Examen_clinique_Taille',
               'Examen_clinique_RC',
               'Examen_clinique_Reste_de_examen_clinique',
               'Consultation_Date_de_consultation',
               'Consultation_Examen_phisique',
               'Consultation_Examen_clinique',
               'Consultation_Explorations',
               'Consultation_Traitement',
               'Consultation_Evolution',
               'Consultation_Remarques',
               'Consultation_Prochaine_Rondez_vous']
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=patients{}.xls'.format(str(datetime.datetime.now()))
    patient = Patient.objects.get(Cin=patient_id)
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('Patients')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for columns_num in range(len(columns)):
        sheet.write(row_num, columns_num, columns[columns_num], font_style)
    font_style = xlwt.XFStyle()
    row_num += 1
    patient_consultations = Consultation.objects.filter(Patient__Cin=patient.Cin).order_by('-Date_de_consultation')
    columns = [patient.Nom,patient.Prenom,patient.Date_de_naissance,'','','','','','','','','','','','','','','','','','','','','','','','','']
    for columns_num in range(len(columns)):
        sheet.write(row_num, columns_num, columns[columns_num], font_style)
    row_num+=1
    for consultation in patient_consultations:
        habitude = Habitude.objects.get(id=consultation.Habitude_id)
        antecedentes = Antecedentes.objects.get(id=consultation.Antecedentes_id)
        examen_phisique = Examen_phisique.objects.get(id=consultation.Examen_phisique_id)
        examen_clinique = Examen_clinique.objects.get(id=consultation.Examen_clinique_id)

        consultation_list = ['',
                             '',
                             '',
                             habitude.Tabagisme,
                             habitude.Nombre_de_Cigarette_par_jours,
                             habitude.Alcool,
                             habitude.Allergies_medicamenteuses,
                             habitude.Autres,
                             antecedentes.Medicaux,
                             antecedentes.Chururgicaux,
                             antecedentes.Medications_en_cours,
                             examen_phisique.plaintes,
                             examen_phisique.Examen_Cinetique,
                             examen_phisique.Reste_de_examen_phisique,
                             examen_clinique.Temperature,
                             examen_clinique.PA,
                             examen_clinique.SRO,
                             examen_clinique.Poids,
                             examen_clinique.Taille,
                             examen_clinique.RC,
                             examen_clinique.Reste_de_examen_clinique,
                             str(consultation.Date_de_consultation),
                             consultation.Explorations,
                             consultation.Traitement,
                             consultation.Evolution,
                             consultation.Remarques,
                             str(consultation.Prochaine_Rondez_vous)]

        for columns_num in range(len(consultation_list)):
            sheet.write(row_num, columns_num, consultation_list[columns_num], font_style)
        row_num+=1
    wb.save(response)

    return response

def Export_excel_patient_consultations(request):
    columns = ['Nom',
               'Prenom',
               'Date_de_naissance',
               'Habitude_Tabagisme',
               'Habitude_Nombre_de_Cigarette_par_jours',
               'Habitude_Alcool',
               'Habitude_Allergies_medicamenteuses',
               'Habitude_Autres',
               'Antecedentes_Medicaux',
               'Antecedentes_Chururgicaux',
               'Antecedentes_Medications_en_cours',
               'Examen_phisique_plaintes',
               'Examen_phisique_Examen_Cinetique',
               'Examen_phisique_Reste_de_examen_phisique',
               'Examen_clinique_Temperature',
               'Examen_clinique_PA',
               'Examen_clinique_SRO',
               'Examen_clinique_Poids',
               'Examen_clinique_Taille',
               'Examen_clinique_RC',
               'Examen_clinique_Reste_de_examen_clinique',
               'Consultation_Date_de_consultation',
               'Consultation_Examen_phisique',
               'Consultation_Examen_clinique',
               'Consultation_Explorations',
               'Consultation_Traitement',
               'Consultation_Evolution',
               'Consultation_Remarques',
               'Consultation_Prochaine_Rondez_vous']
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
        patient_consultations = Consultation.objects.filter(Patient__Cin=patient.Cin).order_by('-Date_de_consultation')
        columns = [patient.Nom,patient.Prenom,patient.Date_de_naissance,'','','','','','','','','','','','','','','','','','','','','','','','','']
        for columns_num in range(len(columns)):
            sheet.write(row_num, columns_num, columns[columns_num], font_style)
        row_num+=1
        for consultation in patient_consultations:
            habitude = Habitude.objects.get(id=consultation.Habitude_id)
            antecedentes = Antecedentes.objects.get(id=consultation.Antecedentes_id)
            examen_phisique = Examen_phisique.objects.get(id=consultation.Examen_phisique_id)
            examen_clinique = Examen_clinique.objects.get(id=consultation.Examen_clinique_id)

            consultation_list = ['',
                                 '',
                                 '',
                                 habitude.Tabagisme,
                        habitude.Nombre_de_Cigarette_par_jours,
                        habitude.Alcool,
                        habitude.Allergies_medicamenteuses,
                        habitude.Autres,
                        antecedentes.Medicaux,
                        antecedentes.Chururgicaux,
                        antecedentes.Medications_en_cours,
                        examen_phisique.plaintes,
                        examen_phisique.Examen_Cinetique,
                        examen_phisique.Reste_de_examen_phisique,
                        examen_clinique.Temperature,
                        examen_clinique.PA,
                        examen_clinique.SRO,
                        examen_clinique.Poids,
                        examen_clinique.Taille,
                        examen_clinique.RC,
                        examen_clinique.Reste_de_examen_clinique,
                        str(consultation.Date_de_consultation),
                        consultation.Explorations,
                        consultation.Traitement,
                        consultation.Evolution,
                        consultation.Remarques,
                        str(consultation.Prochaine_Rondez_vous)]

            for columns_num in range(len(consultation_list)):
                sheet.write(row_num, columns_num, consultation_list[columns_num], font_style)
            row_num+=1
    wb.save(response)

    return response

def Export_excel_patient(request):
    columns = ['Nom','Prenom','Date_de_naissance','Lieu_de_naissance','Profession','Adresse','Cin','Sexe','Statut_matrimonial','Telephone']
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=patients{}.xls'.format(str(datetime.datetime.now()))
    patients = Patient.objects.all()
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('Patients')
    row_num = 1
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for columns_num in range(len(columns)):
        sheet.write(row_num, columns_num, columns[columns_num], font_style)
    font_style = xlwt.XFStyle()
    for patient in patients:
        patient_consultations = Consultation.objects.filter(Patient__Cin=patient.Cin).order_by('-Date_de_consultation')

        row_num += 1
        patient_list = [patient.Nom,
                        patient.Prenom,
                        patient.Date_de_naissance,
                        patient.Lieu_de_naissance,
                        patient.Profession,
                        patient.Adresse,
                        patient.Cin,
                        patient.Sexe,
                        patient.Statut_matrimonial,
                        patient.Telephone]
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

def delete_patient(request, patient_id):
    msg = None
    success = False
    html_template = loader.get_template('index.html')
    patient = Patient.objects.get(Cin=patient_id)

    try:
        patient.delete()
        msg = "Le patient {} a été supprimé avec succès".format(patient.Nom)
        success = False
    except:
        msg = "Le patient {} n'a pas été supprimé avec succès".format(patient.Nom)
        success = False
    context = {}
    return HttpResponseRedirect("/")

def view_patient(request, patient_id):
    msg = 'Success'
    try:
        patient = Patient.objects.get(Cin=patient_id)
    except:
        msg = "Le patient n'existe pas"
        success = False
        return HttpResponseRedirect("/")

    return render(request, "./Patient_management/view_patient.html", {"msg": msg, "patient": patient})

def update_patient(request, patient_id):
    msg = ''
    success = False
    try:
        patient = Patient.objects.get(Cin=patient_id)
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
                msg = "Le patient n'existe pas"
                success = False
                return HttpResponseRedirect("/")
            else:
                success = False
                msg = "Le formulaire n'est pas valide: {}".format(form.errors)
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
                                           'telephone': patient.Telephone, })

            patient = Patient.objects.get(Cin=patient_id)
    except:
        form = AddPatientForm()
        msg = "Le patient n'existe pas"
        success = False
        return HttpResponseRedirect("/")
    # return redirect("/login/")

    return render(request, "./Patient_management/update_patient.html", {"success": success, "msg": msg, "form": form, "patient": patient})

def view_consultation_patient(request, patient_id,consultation_id=None):
    msg = ''
    success = True
    try:
       patient = Patient.objects.get(Cin=patient_id)
       consultation = Consultation.objects.get(id=consultation_id)
       habitude = Habitude.objects.get(id=consultation.Habitude_id)
       antecedentes = Antecedentes.objects.get(id=consultation.Antecedentes_id)
       examen_phisique = Examen_phisique.objects.get(id=consultation.Examen_phisique_id)
       examen_clinique = Examen_clinique.objects.get(id=consultation.Examen_clinique_id)
    except:
       msg = "Le patient n'existe pas"
       success = False
       return HttpResponseRedirect("/consultation_patient/{}/".format(patient_id))
    context = {
        "success": success,
        "msg": msg,
        "Habitude": habitude,
        "Antecedentes": antecedentes,
        "Examen_phisique": examen_phisique,
        "Examen_clinique": examen_clinique,
        "Consultation": consultation,
        "patient": patient,
    }
    return render(request, "./Consultations/view_patient_consultation.html", context)

def global_consultation_patient(request):
    habitude = Habitude.objects.all()
    antecedentes = Antecedentes.objects.all()
    examen_phisique = Examen_phisique.objects.all()
    examen_clinique = Examen_clinique.objects.all()
    patient_consultations = Consultation.objects.all().order_by('-Date_de_consultation')
    My_consultation_Filter = ConsultationFilter(request.GET, queryset=patient_consultations)
    Consultations = My_consultation_Filter.qs
    paginator = Paginator(Consultations, 10)
    page_number = request.GET.get('page')
    success=True
    msg="toutes les consultations des patients"
    consultations_page_obj = paginator.get_page(page_number)
    context = {
        "success": success,
        "msg": msg,
        "Habitude": habitude,
        "Antecedentes": antecedentes,
        "Examen_phisique": examen_phisique,
        "Examen_clinique": examen_clinique,
        "consultations_page_obj": consultations_page_obj,
    }

    return render(request, "./Consultations/global_patient_consultation.html", context)

def delete_consultation_patient(request, patient_id, consultation_id=None,source=None):
    msg = None
    success = False
    html_template = loader.get_template('index.html')
    patient = Patient.objects.get(Cin=patient_id)
    consultation = Consultation.objects.get(id=consultation_id)
    habitude = Habitude.objects.get(id=consultation.Habitude_id)
    antecedentes = Antecedentes.objects.get(id=consultation.Antecedentes_id)
    examen_phisique = Examen_phisique.objects.get(id=consultation.Examen_phisique_id)
    examen_clinique = Examen_clinique.objects.get(id=consultation.Examen_clinique_id)

    try:

        print('deleting consultation')
        consultation.delete()
        print('deleting habitude')
        habitude.delete()
        print('deleting antecedentes')
        antecedentes.delete()
        print('deleting examen_phisique')
        examen_phisique.delete()
        print('deleting examen_clinique')
        examen_clinique.delete()
        msg = "la consultation {} de l'utilisateur {} a été supprimée avec succès".format(consultation.Date_de_consultation,patient.Nom)
        success = False
    except:
        msg = "le patient {} n'a pas été supprimé ".format(patient.Nom)
        success = False
    context = {}
    if source == "global" :
        return HttpResponseRedirect("/global_consultation_patient/".format(patient_id),context)
    else:
        return HttpResponseRedirect("/consultation_patient/{}/".format(patient_id),context)

def consultation_patient(request, patient_id, action=None, consultation_id=None):
    msg = None
    success = False
    consultations_page_obj = None
    HabitudeForm = None
    AntecedentesForm = None
    Examen_phisiqueForm= None
    Examen_cliniqueForm= None
    ConsultationForm = None
    selectedPatient = Patient.objects.get(Cin=patient_id)

    try:

        if request.method == "POST":
            HabitudeForm = AddHabitudeForm(request.POST or None)
            AntecedentesForm = AddAntecedentesForm(request.POST or None)
            Examen_phisiqueForm = AddExamen_phisiqueForm(request.POST or None)
            Examen_cliniqueForm = AddExamen_cliniqueForm(request.POST or None)
            ConsultationForm = AddConsultationForm(request.POST or None)
            if ConsultationForm.is_valid() and HabitudeForm.is_valid() and AntecedentesForm.is_valid() and Examen_phisiqueForm.is_valid() and Examen_cliniqueForm.is_valid():
                date = str(timezone.now().day) + str(timezone.now().month) + str(
                    timezone.now().year) + str(timezone.now().hour) + str(timezone.now().minute)+ str(
                    timezone.now().second)
                date = int(date)
                # Add Habitude
                Tabagisme = HabitudeForm.cleaned_data.get("Tabagisme")
                Nombre_de_Cigarette_par_jours = HabitudeForm.cleaned_data.get("Nombre_de_Cigarette_par_jours")
                Alcool = HabitudeForm.cleaned_data.get("Alcool")
                Allergies_medicamenteuses = HabitudeForm.cleaned_data.get("Allergies_medicamenteuses")
                Autres = HabitudeForm.cleaned_data.get("Autres")

                # Add Antecedentes
                Medicaux = AntecedentesForm.cleaned_data.get("Medicaux")
                Chururgicaux = AntecedentesForm.cleaned_data.get("Chururgicaux")
                Medications_en_cours = AntecedentesForm.cleaned_data.get("Medications_en_cours")

                # Add Examen_phisique
                plaintes = Examen_phisiqueForm.cleaned_data.get("plaintes")
                Examen_Cinetique = Examen_phisiqueForm.cleaned_data.get("Examen_Cinetique")
                Reste_de_examen_phisique = Examen_phisiqueForm.cleaned_data.get("Reste_de_examen_phisique")

                # Add Examen_clinique
                Temperature = Examen_cliniqueForm.cleaned_data.get("Temperature")
                PA = Examen_cliniqueForm.cleaned_data.get("PA")
                SRO = Examen_cliniqueForm.cleaned_data.get("SRO")
                Poids = Examen_cliniqueForm.cleaned_data.get("Poids")
                Taille = Examen_cliniqueForm.cleaned_data.get("Taille")
                RC = Examen_cliniqueForm.cleaned_data.get("RC")
                Reste_de_examen_clinique = Examen_cliniqueForm.cleaned_data.get("Reste_de_examen_clinique")

                # Add Consultation
                Date_de_consultation = ConsultationForm.cleaned_data.get("Date_de_consultation")
                Explorations = ConsultationForm.cleaned_data.get("Explorations")
                Traitement = ConsultationForm.cleaned_data.get("Traitement")
                Evolution = ConsultationForm.cleaned_data.get("Evolution")
                Remarques = ConsultationForm.cleaned_data.get("Remarques")
                Prochaine_Rondez_vous = ConsultationForm.cleaned_data.get("Prochaine_Rondez_vous")

                if action == "update_consultation":

                    consultation = Consultation.objects.get(id=consultation_id)
                    habitude = Habitude.objects.get(id=consultation.Habitude_id)
                    antecedentes = Antecedentes.objects.get(id=consultation.Antecedentes_id)
                    examen_phisique = Examen_phisique.objects.get(id=consultation.Examen_phisique_id)
                    examen_clinique = Examen_clinique.objects.get(id=consultation.Examen_clinique_id)

                    habitude.Tabagisme = Tabagisme
                    habitude.Nombre_de_Cigarette_par_jours = Nombre_de_Cigarette_par_jours
                    habitude.Alcool = Alcool
                    habitude.Allergies_medicamenteuses = Allergies_medicamenteuses
                    habitude.Autres = Autres

                    antecedentes.Medicaux = Medicaux
                    antecedentes.Chururgicaux = Chururgicaux
                    antecedentes.Medications_en_cours = Medications_en_cours

                    examen_phisique.plaintes = plaintes
                    examen_phisique.Examen_Cinetique = Examen_Cinetique
                    examen_phisique.Reste_de_examen_phisique = Reste_de_examen_phisique

                    examen_clinique.Temperature = Temperature
                    examen_clinique.PA = PA
                    examen_clinique.SRO = SRO
                    examen_clinique.Poids = Poids
                    examen_clinique.Taille = Taille
                    examen_clinique.RC = RC
                    examen_clinique.Reste_de_examen_clinique = Reste_de_examen_clinique

                    consultation.Date_de_consultation = Date_de_consultation
                    consultation.Explorations = Explorations
                    consultation.Traitement = Traitement
                    consultation.Evolution = Evolution
                    consultation.Remarques = Remarques
                    consultation.Prochaine_Rondez_vous = Prochaine_Rondez_vous
                    habitude.save()
                    antecedentes.save()
                    examen_phisique.save()
                    examen_clinique.save()
                    consultation.save()
                    msg = "Consultation mise à jour avec succès"
                    success = True

                else:
                    New_Habitude = Habitude(date, Tabagisme, Nombre_de_Cigarette_par_jours, Alcool,
                                            Allergies_medicamenteuses, Autres)
                    New_Habitude.save()
                    New_Antecedentes = Antecedentes(date, Medicaux, Chururgicaux, Medications_en_cours)
                    New_Antecedentes.save()
                    New_Examen_phisique = Examen_phisique(date, plaintes, Examen_Cinetique,
                                                          Reste_de_examen_phisique)
                    New_Examen_phisique.save()
                    New_Examen_clinique = Examen_clinique(date, Temperature, PA, SRO, Poids, Taille, RC,
                                                          Reste_de_examen_clinique)
                    New_Examen_clinique.save()
                    New_consultation = Consultation(date, selectedPatient.Cin, Date_de_consultation,
                                                    New_Habitude.id, New_Antecedentes.id, New_Examen_phisique.id,
                                                    New_Examen_clinique.id, Explorations, Traitement, Evolution,
                                                    Remarques, Prochaine_Rondez_vous)
                    New_consultation.save()
                    msg = 'Consultation ajoutée avec succès'
                    success = True
                    selectedPatient = Patient.objects.get(Cin=patient_id)
                    HabitudeForm = AddHabitudeForm()
                    AntecedentesForm = AddAntecedentesForm()
                    Examen_phisiqueForm = AddExamen_phisiqueForm()
                    Examen_cliniqueForm = AddExamen_cliniqueForm()
                    ConsultationForm = AddConsultationForm()
            else:
                success = False
                msg = "Le formulaire n'est pas valide: {}".format(ConsultationForm.errors)
        else:
            selectedPatient = Patient.objects.get(Cin=patient_id)
            if action == "update_consultation":
                consultation = Consultation.objects.get(id=consultation_id)
                habitude = Habitude.objects.get(id=consultation.Habitude_id)
                antecedentes = Antecedentes.objects.get(id=consultation.Antecedentes_id)
                examen_phisique = Examen_phisique.objects.get(id=consultation.Examen_phisique_id)
                examen_clinique = Examen_clinique.objects.get(id=consultation.Examen_clinique_id)

                HabitudeForm = AddHabitudeForm(initial={'Tabagisme': habitude.Tabagisme,
                                                        'Nombre_de_Cigarette_par_jours': habitude.Nombre_de_Cigarette_par_jours,
                                                        'Alcool': habitude.Alcool,
                                                        'Allergies_medicamenteuses': habitude.Allergies_medicamenteuses,
                                                        'Autres': habitude.Autres})
                AntecedentesForm = AddAntecedentesForm(initial={'Medicaux': antecedentes.Medicaux,
                                                                'Chururgicaux': antecedentes.Chururgicaux,
                                                                'Medications_en_cours': antecedentes.Medications_en_cours, })

                Examen_phisiqueForm = AddExamen_phisiqueForm(initial={'plaintes': examen_phisique.plaintes,
                                                                      'Examen_Cinetique': examen_phisique.Examen_Cinetique,
                                                                      'Reste_de_examen_phisique': examen_phisique.Reste_de_examen_phisique, })

                Examen_cliniqueForm = AddExamen_cliniqueForm(initial={'Temperature': examen_clinique.Temperature,
                                                                      'PA': examen_clinique.PA,
                                                                      'SRO': examen_clinique.SRO,
                                                                      'Poids': examen_clinique.Poids,
                                                                      'Taille': examen_clinique.Taille,
                                                                      'RC': examen_clinique.RC,
                                                                      'Reste_de_examen_clinique': examen_clinique.Reste_de_examen_clinique, })

                ConsultationForm = AddConsultationForm(
                    initial={'Date_de_consultation': consultation.Date_de_consultation,
                             'Explorations': consultation.Explorations,
                             'Traitement': consultation.Traitement,
                             'Evolution': consultation.Evolution,
                             'Remarques': consultation.Remarques,
                             'Prochaine_Rondez_vous': consultation.Prochaine_Rondez_vous,
                             })
                msg = "Consultation de {} liée au patient {}".format(consultation.Date_de_consultation,selectedPatient.Nom)
                success = True
            else:
                msg = ''
                success = True
                HabitudeForm = AddHabitudeForm()
                AntecedentesForm = AddAntecedentesForm()
                Examen_phisiqueForm = AddExamen_phisiqueForm()
                Examen_cliniqueForm = AddExamen_cliniqueForm()
                ConsultationForm = AddConsultationForm()
    except:
        selectedPatient = Patient.objects.get(Cin=patient_id)
        HabitudeForm = AddHabitudeForm()
        AntecedentesForm = AddAntecedentesForm()
        Examen_phisiqueForm = AddExamen_phisiqueForm()
        Examen_cliniqueForm = AddExamen_cliniqueForm()
        ConsultationForm = AddConsultationForm()
        msg = "Le patient n'existe pas"
        success = False
        return render(request, "./Consultations/patient_consultation.html",
                      {"consultations_page_obj": consultations_page_obj, "success": success, "msg": msg,
                       "HabitudeForm": HabitudeForm, "AntecedentesForm": AntecedentesForm,
                       "Examen_phisiqueForm": Examen_phisiqueForm, "Examen_cliniqueForm": Examen_cliniqueForm,
                       "ConsultationForm": ConsultationForm, "patient": selectedPatient})

    # Consultation history
    patient_consultations = Consultation.objects.filter(Patient__Cin=selectedPatient.Cin).order_by(
        '-Date_de_consultation')
    My_consultation_Filter = ConsultationFilter(request.GET, queryset=patient_consultations)
    Consultations = My_consultation_Filter.qs
    paginator = Paginator(Consultations, 5)
    page_number = request.GET.get('page')
    consultations_page_obj = paginator.get_page(page_number)
    context = {
        "action": action,
        "consultations_page_obj": consultations_page_obj,
        "success": success,
        "msg": msg,
        "HabitudeForm": HabitudeForm,
        "AntecedentesForm": AntecedentesForm,
        "Examen_phisiqueForm": Examen_phisiqueForm,
        "Examen_cliniqueForm": Examen_cliniqueForm,
        "ConsultationForm": ConsultationForm,
        "patient": selectedPatient,
    }
    if action == "update_consultation":
        context["consultation"]= consultation

    return render(request, "./Consultations/patient_consultation.html", context)

def add_patient(request):
    msg = ''
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
                msg = 'Le patient existe déjà!'
                success = False
                return render(request, "./Patient_management/add_patient.html", {"form": form, "msg": msg, "success": success})

            except:
                new_patient = Patient(Nom, Prenom, Date_de_naissance, Lieu_de_naissance, Profession, Adresse, Cin, Sexe,
                                      Statut_matrimonial, Telephone)
                new_patient.save()
                msg = 'Le patient a été créé avec succès!'
                success = True
                print("An exception occurred")
                form = AddPatientForm()
                return render(request, "./Patient_management/add_patient.html", {"form": form, "msg": msg, "success": success})
            # return redirect("/login/")
        else:
            msg = "Erreur lors de l'ajout d'un nouveau patient, veuillez contacter l'administrateur"
    else:
        form = AddPatientForm()

    return render(request, "./Patient_management/add_patient.html", {"form": form, "msg": msg, "success": success})

def consultations(request):
    msg = None
    success = False
    form = None

    return render(request, "./Consultations/consultation.html", {"form": form, "msg": msg, "success": success})
