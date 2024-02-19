from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import requests

# Create your views here.
#Se connecter
def se_connecter(request):

    user = request.user

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            # if request.user.role in ["admin", "alarmeur"]:
            return redirect('accueil')
    return redirect('login_page')

@login_required(login_url='login')
def se_deconnecter(request):
    logout(request)
    return redirect('login_page')

def home_page(request):
    alertes = Alerte.objects.all().order_by('-id')
    latitude = 1.7749
    longitude = -1.4194
    status = 0
    if request.method == 'POST':
        lieu = request.POST.get('lieu')
        url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + lieu
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]['lat']
                longitude = data[0]['lon']
        status = 1

    return render(request, "index.html", {"alertes": alertes, "latitude":latitude, "longitude":longitude, "status":status})
 

def detail_alerte(request):
    pk = request.GET.get('pk')
    alerte = Alerte.objects.filter(pk=pk).first()
    return render(request, "detail_alerte.html", {"alerte": alerte})

def signaler_alerte(request):
    pk = request.GET.get('pk')
    alerte = Alerte.objects.filter(pk=pk).first()
    alerte.etat = True
    alerte.save()
    alertes = Alerte.objects.all().order_by('-id')
    latitude = 1.7749
    longitude = -1.4194
    status = 0
    return render(request, "index.html", {"alertes": alertes, "latitude":latitude, "longitude":longitude, "status":status})

def capture_page(request):
    captures = Capture.objects.all().order_by('-id')
    return render(request, "captures.html", {"captures": captures})

def users_page(request):
    users = CustomUser.objects.all().order_by('-id')
    return render(request, "liste_users.html", {"users": users})

def detail_user(request):
    pk = request.GET.get('pk')
    user = CustomUser.objects.get(pk = pk)
    return render(request, "detail_user.html", {"user": user})
    
def generate_password():
    password = make_password("coco")
    return password

def save_user(request):
    if request.method == 'POST':
        pk = request.GET.get('pk')
        user = CustomUser()
        if pk:
            user = CustomUser.objects.filter(pk = pk).first()
        user.nom = request.POST.get("nom")
        user.prenom = request.POST.get("prenom")
        user.username = user.email = request.POST.get("email")
        user.role = request.POST.get("role")
        user.password = generate_password()
        user.save()
        return redirect('list_users')
    return redirect('creer_user')

def check_capture(capture):
    taux = 88
    return taux
    
def save_capture(request):
    status = 0
    if request.method == 'POST':
        capture = Capture()
        capture.base64 = request.POST.get("base64")
        capture.save()
        taux = check_capture(capture.base64)
        if taux > 80:
            alerte = Alerte()
            alerte.taux = taux
            alerte.capture = capture
            alerte.save()
            status = 2
        status = 1
    return JsonResponse({"status": status})