# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, AddEmployeeForm, Employee
from datetime import datetime,timedelta


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        employee_form = AddEmployeeForm(request.POST)
        if form.is_valid() and employee_form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            Email = form.cleaned_data.get("email")
            Nom = employee_form.cleaned_data.get("nom")
            Prenom = employee_form.cleaned_data.get("prenom")
            Date_de_naissance = employee_form.cleaned_data.get("date_de_naissance")
            Lieu_de_naissance = employee_form.cleaned_data.get("lieu_de_naissance")
            Role = employee_form.cleaned_data.get("role")
            Adresse = employee_form.cleaned_data.get("adresse")
            Cin = employee_form.cleaned_data.get("cin")
            Sexe = employee_form.cleaned_data.get("sexe")
            Statut_matrimonial = employee_form.cleaned_data.get("statut_matrimonial")
            Telephone = employee_form.cleaned_data.get("telephone")
            try:
                employee = Employee.objects.get(Cin=Cin)
                msg = 'Le patient existe déjà!'
                return render(request, "accounts/register.html",
                              {"form": form, "employee_form": employee_form, "msg": msg, "success": success})


            except:
                new_employee = Employee(Nom=Nom,
                                        Prenom=Prenom,
                                        Username=username,
                                        Email=Email,
                                        Date_de_naissance=Date_de_naissance,
                                        Lieu_de_naissance=Lieu_de_naissance,
                                        Role=Role,
                                        Adresse=Adresse,
                                        Statut_matrimonial=Statut_matrimonial,
                                        Sexe=Sexe,
                                        Cin=Cin,
                                        Telephone=Telephone)
                new_employee.save()

                user = authenticate(username=username, password=raw_password)
                form.save()
                msg = "L'utilisateur a été créé avec succès!"
                success = True
                print("An exception occurred")
                # return redirect("/login/")
                msg = 'User created - please <a href="/login">login</a>.'
                success = True
                form = SignUpForm()
                employee_form = AddEmployeeForm()
            # return redirect("/login/")

        else:
            msg = "Erreur lors de l'ajout d'un nouveau utilisateur, vérifier les données"
    else:
        form = SignUpForm()
        employee_form = AddEmployeeForm()

    return render(request, "accounts/register.html", {"form": form, "employee_form":employee_form,"msg": msg, "success": success})



