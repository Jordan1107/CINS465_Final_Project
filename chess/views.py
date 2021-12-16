from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from chess.forms import JoinForm, LoginForm
from .models import *
import os
import pygame

@login_required(login_url='/login/')
def home(request):
    return render(request, 'chess/home.html')

def about(request):
    return render(request, 'chess/about.html')

def tic(request):
    return render(request, 'chess/tic.html')

@login_required(login_url='/login/')
def room(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        option = request.POST.get('option')
        room_code = request.POST.get('room_code')

        if option == '1':
            game = Game.objects.filter(room_code = room_code).first()

            if game is None:
                message.success(request , "Room code not found")
                return redirect('/')

            if game.is_over:
                message.success(request , "Game is over")
                return redirect('/')

            game.game_opponent = username
            game.save()
        else:
            game = Game(game_creator = username , room_code = room_code)
            game.save()
            return redirect('/play/' + room_code + '?username='+username)

    return render(request, 'chess/gameroom.html')

@login_required(login_url='/login/')
def play(request , room_code):
    username = request.GET.get('username')
    context = {
    'room_code' : room_code ,
    'username' : username
    }
    return render(request, 'chess/play.html' , context)

def login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    auth_login(request,user)
                    # Send the user back to original page requested, or home page
                    next = request.POST.get('next', '/')
                    return HttpResponseRedirect(next)
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'chess/login.html', {"login_form": LoginForm() } )
    else:
        return render(request, 'chess/login.html', { "login_form": LoginForm() })

@login_required(login_url='/login/')
def logout(request):
    # Log out the user.
    auth_logout(request)
    # Return to homepage.
    return redirect('/')

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect('/')
        else:
            # Form invalid, print errors to console
            print(join_form.errors)
            return render(request, 'chess/join.html', { "join_form": join_form })
    else:
        return render(request, 'chess/join.html', { "join_form": JoinForm() })

def board(request):
    if(Chess.objects.all().filter()):
        reset(request)

    page_data = { "rows" : [], "chess_form":ChessForm }
    if (request.method == 'POST'):
        chess_form = ChessForm(request.POST);
        if (chess_form.is_valid()):
            Move_From = chess_form.cleaned_data["Move_From"]
            Move_To = chess_form.cleaned_data["Move_To"]
            Chess(name=Move_From, value=Move_To).save()
        else:
            page_data["chess_form"] = chess_form

    for row_num in range(1,10):
        row = {}
        for col_num in range(1,10):
            name = "r{}c{}".format(row_num,col_num)
            try:
                record = Chess.objects.get(name=name)
                row[name] = record.value
            except Chess.DoesNotExist:
                row[name] = ""
        page_data.get("rows").append(row)
    return render(request, 'chess/play.html' , page_data)

def reset(request):
    page_data = {
    "rows": [
    {"r1c1": '1', "r1c2": "&#9820;", "r1c3": "&#9822;", "r1c4": "&#9821;", "r1c5": "&#9818;", "r1c6": "&#9819;", "r1c7": "&#9821;", "r1c8": "&#9822;", "r1c9": "&#9820;"},
    {"r2c1": '2', "r2c2": "&#9823;", "r2c3": "&#9823;", "r2c4": "&#9823;", "r2c5": "&#9823;", "r2c6": "&#9823;", "r2c7": "&#9823;", "r2c8": "&#9823;", "r2c9": "&#9823;"},
    {"r3c1": '3', "r3c2": "&nbsp", "r3c3": "&nbsp", "r3c4": "&nbsp", "r3c5": "&nbsp", "r3c6": "&nbsp", "r3c7": "&nbsp", "r3c8": "&nbsp", "r3c9": "&nbsp"},
    {"r4c1": '4', "r4c2": "&nbsp", "r4c3": "&nbsp", "r4c4": "&nbsp", "r4c5": "&nbsp", "r4c6": "&nbsp", "r4c7": "&nbsp", "r4c8": "&nbsp", "r4c9": "&nbsp"},
    {"r5c1": '5', "r5c2": "&nbsp", "r5c3": "&nbsp", "r5c4": "&nbsp", "r5c5": "&nbsp", "r5c6": "&nbsp", "r5c7": "&nbsp", "r5c8": "&nbsp", "r5c9": "&nbsp"},
    {"r6c1": '6', "r6c2": "&nbsp", "r6c3": "&nbsp", "r6c4": "&nbsp", "r6c5": "&nbsp", "r6c6": "&nbsp", "r6c7": "&nbsp", "r6c8": "&nbsp", "r6c9": "&nbsp"},
    {"r7c1": '7', "r7c2": "&#9817;", "r7c3": "&#9817;", "r7c4": "&#9817;", "r7c5": "&#9817;", "r7c6": "&#9817;", "r7c7": "&#9817;", "r7c8": "&#9817;", "r7c9": "&#9817;"},
    {"r8c1": '8', "r8c2": "&#9814;", "r8c3": "&#9816;", "r8c4": "&#9815;", "r8c5": "&#9813;", "r8c6": "&#9812;", "r8c7": "&#9815;", "r8c8": "&#9816;", "r8c9": "&#9814;"},
    {"r9c1": '', "r9c2": "a", "r9c3": "b", "r9c4": "c", "r9c5": "d", "r9c6": "e", "r9c7": "f", "r9c8": "g", "r9c9": "h"}
    ]
    }

    Chess.objects.all().delete()
    for row in page_data.get("rows"):
        for name,value in row.items():
            Chess(name=name,value=value).save()
