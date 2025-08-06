# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from qrcode import *
import os
from django.conf import settings
from .forms import UserRegistrationForm
from .models import UserRegistrationModel


def generateQRCode():
    import random
    fixed_digits = 6
    return random.randrange(111111, 999999, fixed_digits)


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                data = generateQRCode()
                request.session['qrcode'] = data
                print("QR Code is :", data)
                img = make(data)
                img_name = 'qrCodeAlex.png'
                img.save(settings.MEDIA_ROOT + '\\' + img_name)
                # return render(request, 'index.html', )
                return render(request, 'GraphicleAuth.html', {'img_name': img_name})
                # return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def qrcodecheck(request):
    if request.method == 'POST':
        server_qr = request.session['qrcode']
        browser_qr = int(request.POST.get('data'))
        print(f"Server Side QR:{type(server_qr)} Browser Side QR:{type(browser_qr)}")
        if server_qr == browser_qr:
            return render(request, 'users/UserHomePage.html', {})
        else:
            messages.success(request, 'Invalid QR Code')
            return render(request, 'UserLogin.html', {})
    else:
        return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def GenerateQRCodes(request):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        import segno
        path = os.path.join('assets','static','qrcodes')
        qrcode = segno.make_qr(msg)
        qrcode.save(path+"/wide_border_qrcode.png", scale=5, border=10,)
        qrcode = segno.make_qr(msg)
        qrcode.save(path+"/darkblue_qrcode.png", scale=5, dark="darkblue",)
        qrcode = segno.make_qr(msg)
        qrcode.save(path+"/lightblue_qrcode.png", scale=5, light="lightblue",)
        qrcode = segno.make_qr(msg)
        qrcode.save(path+"/green_datadark_qrcode.png", scale=5, light="lightblue", dark="darkblue", data_dark="green",)
        import wifi_qrcode_generator.generator

        qr_code = wifi_qrcode_generator.generator.wifi_qrcode(
            ssid='Wireless and Security Applications', hidden=False, authentication_type='WPA', password=msg
        )
        qr_code.print_ascii()
        qrcode = qr_code.make_image()
        qrcode.save(path+"/wifi.png")
        return render(request, 'users/genCodes.html', {'msg': msg})
    else:
        return render(request, 'users/qrCodes.html', {})
