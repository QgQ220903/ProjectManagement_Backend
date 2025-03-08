from django.shortcuts import render
from django.http import JsonResponse
from account.serializers import AccountSerializer
from account.models import Account
# Create your views here.

def account_list(request):
  account = Account.objects.all()
  serializer = AccountSerializer(account, many = True)
  return JsonResponse({
    'data' : serializer.data
  })

# Create your views here.
from rest_framework import generics
from .models import Account
from .serializers import AccountSerializer

class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

