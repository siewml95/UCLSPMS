from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate
import requests

from .models import OAuthToken
from cuser.models import CUser as User
from .helpers import generate_state

import os
import json
import requests

UCLAPI_CLIENT_ID= os.environ.get("UCLAPI_CLIENT_ID")
UCLAPI_CLIENT_SECRET=os.environ.get("UCLAPI_CLIENT_SECRET")
UCLAPI_URL= os.environ.get("UCLAPI_URL")
TOKEN_DEBUG_ENABLED=False

def render_login_button(request):
    return render(request, 'login.html')


@csrf_protect
def process_login(request):
    state = generate_state()
    request.session["state"] = state
    auth_url = os.environ.get("UCLAPI_URL") + "/oauth/authorise"
    auth_url += "?client_id=" + os.environ.get("UCLAPI_CLIENT_ID")
    auth_url += "&state=" + state

    return redirect(auth_url)


def callback(request):
    try:
        result = request.GET.get("result")
    except KeyError:
        return JsonResponse({
            "error": "No result parameter passed."
        })

    if result == "allowed":
        print("allowed")
        return allowed(request)
    elif result == "denied":
        return denied(request)
    else:
        return JsonResponse({
            "ok": False,
            "error": "Result was not allowed or denied."
        })


def allowed(request):
    try:
        code = request.GET.get("code")
        print(code)
        client_id = request.GET.get("client_id")
        state = request.GET.get("state")
    except KeyError:
        return JsonResponse({
            "error": "Parameters missing from request."
        })

    try:
        session_state = request.session["state"]
    except KeyError:
        return JsonResponse({
            "ok": False,
            "error": "There is no session cookie set containing a state"
        })

    url = UCLAPI_URL + "/oauth/token"
    params = {
        'grant_type': 'authorization_code',
        'client_id' : os.environ.get("UCLAPI_CLIENT_ID"),
        'code': code,
        'client_secret': os.environ.get("UCLAPI_CLIENT_SECRET")
    }

    r = requests.get(url, params=params)

    print("token_data = r.json()")

    try:
        token_data = r.json()

        if token_data["ok"] is not True:
            return JsonResponse({
                "ok": False,
                "error": "An error occurred: " + token_data["error"]
            })

        if token_data["state"] != state:
            return JsonResponse({
                "ok": False,
                "error": "The wrong state was returned"
            })

        if token_data["client_id"] != client_id:
            return JsonResponse({
                "ok": False,
                "error": "The wrong client ID was returned"
            })

        token_code = token_data["token"]
        scope_data = json.loads(token_data["scope"])
    except KeyError:
        return JsonResponse({
            "ok": False,
            "error": "Proper JSON was not returned by the token endpoint"
        })

    token = OAuthToken(code=token_code)

    token.save()

    url = os.environ.get("UCLAPI_URL")  + "/oauth/user/data"
    params = {
        'token': token_code,
        'client_secret': os.environ.get("UCLAPI_CLIENT_SECRET")
    }

    r = requests.get(url, params=params)
    data = r.json()
    print(data["ok"])
    if data["ok"] == True:
       print("r[ok] == true")
       try:
          user = User.objects.get(email=data["email"])
          print(user.profile.__dict__)

          if user.profile.type == 2:
              print("user.profile.type == 2")
              login(request,user)
              return HttpResponseRedirect("/project")
          else:
             print("user.profile.type != 2")

             return HttpResponseRedirect("/error")

       except User.DoesNotExist:
          print('does not exists')
          user = User.objects.create(email=data["email"],first_name=data["given_name"])
          print('create')
          user.profile.type=2
          user.profile.is_verified = True
          print("profile")
          user.save()
          login(request,user)
          return HttpResponseRedirect("/project")
    else:
        print("not ok")
        return HttpResponseRedirect("/error")

    return JsonResponse(r.json())


def denied(request):
    return render(request, 'denied.html', {
                  "state": request.GET.get("state", None)})

def token_test(request):
    if not os.environ.get("TOKEN_DEBUG_ENABLED"):
        return JsonResponse({
            "ok": False,
            "error": "Token debugging must be enabled to use this endpoint."
        })

    try:
        token = request.GET['token']
    except KeyError:
        return JsonResponse({
            "ok": False,
            "error": "A token must be provided to use this endpoint."
        })

    params = {
        'token': token,
        'client_secret': os.environ.get("UCLAPI_CLIENT_SECRET")
    }

    r = requests.get(url, params=params)

    return JsonResponse(r.json())
