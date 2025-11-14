from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from django.contrib.auth.models import User
from .models import Pregunta