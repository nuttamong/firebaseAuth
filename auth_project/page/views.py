from django.shortcuts import render, redirect

from dotenv import load_dotenv
from django.contrib import messages
import os
import pyrebase

load_dotenv()

config={
    "apiKey": os.environ.get("API_KEY"),
    "authDomain": os.environ.get("AUTH_DOMAIN"),
    "databaseURL": os.environ.get("DB_URL"),
    "projectId": os.environ.get("PROJECT_ID"),
    "storageBucket": os.environ.get("STORAGE_BUCKET"),
    "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
    "appId": os.environ.get("APP_ID")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def LoginPage(req):
    # if 'signIn' in req.session:
    #     del req.session['signIn']
    # if 'signUp' in req.session:
    #     del req.session['signUp']
    try:
        del req.session['uid']
        del req.session['localId']
    except:
        pass
    return render(req, 'index.html')

def HomePage(req):
    if not 'uid' in req.session:
        return redirect('/')
    user_info = auth.get_account_info(req.session['uid'])
    user = user_info['users']
    id = user[0]['localId']
    req.session['localId'] = id
    username = db.child("users").child(id).get().val()['name']
    messages = str(username)
    return render(req, 'home.html', {'username': messages})

def RePWDPage(req):
    if not 'uid' in req.session:
        return render(req, 'resetpwd.html', {'login': False})
    return render(req, 'resetpwd.html', {'login': True})

def PostLogin(req):
    email = req.POST.get('user')
    pwd = req.POST.get('pass')

    if 'signIn' in req.session:
        del req.session['signIn']
    if 'signUp' in req.session:
        del req.session['signUp']

    try:
        user = auth.sign_in_with_email_and_password(email, pwd)
    except:
        message = "Email or Password is incorrect!!!"
        messages.error(req, message)
        req.session['signIn'] = "True"
        return redirect('/')
    session_id = user['idToken']
    req.session['uid'] = str(session_id)
    # check verification
    info = auth.get_account_info(user['idToken'])
    user_info =  info['users']
    checkVerified = user_info[0]['emailVerified']
    if not checkVerified:
        message = "Please verify your email!!!"
        messages.error(req, message)
        req.session['signIn'] = "True"
        return redirect('/')
    return redirect('/home')

def Logout(req):
    try:
        del req.session['uid']
        del req.session['localId']
    except:
        pass
    return redirect('/home')

def Delete(req):
    auth.delete_user_account(req.session['uid'])
    db.child("users").child(req.session['localId']).remove()
    try:
        del req.session['uid']
        del req.session['localId']
    except:
        pass
    return redirect('/home')

def PostRegister(req):
    email = req.POST.get('email')
    pwd = req.POST.get('sign-up-pass')
    re_pass = req.POST.get('re-pass')
    username = req.POST.get('sign-up-user')

    if 'signIn' in req.session:
        del req.session['signIn']
    if 'signUp' in req.session:
        del req.session['signUp']
    
    if re_pass != pwd:
        message = "Passwords don't match!!!"
        messages.error(req, message)
        req.session['signUp'] = "True"
        return redirect('/')
    try:
        user=auth.create_user_with_email_and_password(email,pwd)
        uid = user['localId']
        token = user['idToken']
        req.session['uid'] = token
        
        
    except:
        message = "This email already exists!!!"
        messages.error(req, message)
        req.session['signUp'] = "True"
        return redirect('/')
    
    data = {"email": str(email), "name": str(username)}
    db.child("users").child(uid).set(data)
    # varification email
    auth.send_email_verification(token)
    message = "Please check your email to verify your email."
    messages.error(req, message)
    req.session['signUp'] = "True"
    return redirect('/')

def postReset(req):
    email = req.POST.get('email-re')
    try:
        auth.send_password_reset_email(email)
        message = "A email to reset password is successfully sent"
        return render(req, "resetpwd.html", {"msg":message})
    except:
        message = "Something went wrong, Please check the email you provided is registered or not"
        return render(req, "resetpwd.html", {"msg":message})

