from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import  *

from .serializers import  *

User = get_user_model()

# Create your views here.


class UserCreateAPIView(CreateAPIView):
    """docstring for UserCreateAPIView."""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self,request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

def logout_view(request):
    logout(request)
    return redirect("/")

# def login_view(request):
#     next = request.GET.get('next')
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         print(username)
#         login(request, user)
#         if next:
#             return redirect(next)
#         return redirect("/")
#     return render(request, "login.html", {"form":form, "title": "LogIn"})
#
# def signup_view(request):
#     next = request.GET.get('next')
#     form = UserSignupForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         password = form.cleaned_data.get('password')
#         user.set_password(password)
#         user.save()
#         new_user = authenticate(username=user.username, password=password)
#         email = form.cleaned_data.get('email')
#         print(email)
#
#         login(request, new_user)
#         if next:
#             return redirect(next)
#         return redirect("/")
#     #
#     context = {
#         "form": form,
#         "title": "SignUp"
#     }
#     return render(request, "signup.html", context)
