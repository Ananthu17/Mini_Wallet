from django.shortcuts import render
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


#Init_Token
class Main_class(APIView):

    def post(self,request):
        try:
            received_data=json.loads(request.body)
            try:
                user = Customer.objects.get(customer_xid=received_data['customer_xid'])
                serilazer = Userserializers(user)
                return Response(serilazer.data)
            except:
                user_account = Customer(customer_xid=received_data['customer_xid'])
                token = Token.objects.create( user = User.objects.get(pk=1))
                user_account.token = token
                user_account.save()
                user = Customer.objects.get(customer_xid=received_data['customer_xid'])
                wallet = Wallet(customer=user)
                wallet.save()
                serilazer = Userserializers(user)
                return Response(serilazer.data,status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
#Wallets
class Wallet_view(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            customer = Customer.objects.get(token=request.auth)
            wallet = Wallet.objects.get(customer=customer)
            if wallet != None and wallet.active == True:
                data = {
                        "status": "success",
                        "data": {
                            "wallet": {
                            "id": wallet.id,
                            "owned_by": wallet.customer.customer_xid,
                            "status": "enabled",
                            "balance": wallet.balance }
                            }
                        }
                return Response(data)
            else:
                data = {
                        "status": "error",
                        "data": {
                            "wallet": {
                            "status": "disabled",
                            }
                        }
                    }
                return Response(data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) 

    def post(self,request):
        try:
            customer = Customer.objects.get(token=request.auth)
            wallet = Wallet.objects.get(customer=customer)
            if wallet != None and wallet.active == False:
                wallet.active = True
                wallet.save()
                data = {
                        "status": "success",
                        "data": {
                            "wallet": {
                            "id": wallet.id,
                            "owned_by": wallet.customer.customer_xid,
                            "status": "enabled",
                            "balance": wallet.balance
                            }
                        }
                    }
                return Response(data)
            else:
                return Response({"status": "Already activated"})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) 

    def patch(self, request):
        try:
            received_data=json.loads(request.body)
            customer = Customer.objects.get(token=request.auth)
            wallet = Wallet.objects.get(customer=customer)
            if wallet != None and wallet.active == True and received_data["is_disabled"]==True:
                wallet.active = False
                wallet.save()
                data = {
                    "status": "success",
                    "data": {
                        "wallet": {
                            "status": "disabled",
                            "balance": wallet.balance
                        }
                    }
                }
                return Response(data)
            else:
                data = {
                    "status": "error",
                    "data": {
                        "wallet": {
                            "status": "disabled"
                        }
                    }
                }
                return Response(data)
        except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 

#Deposits
class Topup_view(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            received_data=json.loads(request.body)
            customer = Customer.objects.get(token=request.auth)
            wallet = Wallet.objects.get(customer=customer)
            if wallet != None and wallet.active == True:
                wallet.balance += received_data['amount']
                wallet.save()
                if received_data['reference_id']:
                    transaction = Transaction(amount=received_data['amount'],reference_id=received_data['reference_id'])
                    transaction.save()
                data = {
                        "status": "success",
                        "data": {
                            "wallet": {
                            "id": wallet.id,
                            "owned_by": wallet.customer.customer_xid,
                            "status": "enabled",
                            "balance": wallet.balance
                            }
                        }
                    }
                return Response(data)
            else:
                data = {
                        "status": "error",
                        "data": {
                            "wallet": {
                            "status": "disabled",
                            }
                        }
                    }
                return Response(data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) 

#Withdrawals
class Transfer_view(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            received_data=json.loads(request.body)
            customer = Customer.objects.get(token=request.auth)
            wallet = Wallet.objects.get(customer=customer)
            if wallet != None and wallet.active == True:
                wallet.balance -= received_data['amount']
                wallet.save()
                if received_data['reference_id']:
                    transaction = Transaction(amount=received_data['amount'],reference_id=received_data['reference_id'])
                    transaction.save()
                data = {
                        "status": "success",
                        "data": {
                            "wallet": {
                            "id": wallet.id,
                            "owned_by": wallet.customer.customer_xid,
                            "status": "enabled",
                            "balance": wallet.balance
                            }
                        }
                    }
                return Response(data)
            else:
                data = {
                        "status": "error",
                        "data": {
                            "wallet": {
                            "status": "disabled",
                            }
                        }
                    }
                return Response(data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) 