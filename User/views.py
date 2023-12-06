from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Bank.settings import api_key
import requests, random
from .serializer import Otp_serializer,UserSerializer,UserPersonalInfoSerializer
from .models import Otp,User,UserPersonalInfo
import json




@api_view(['POST'])
def check(request):
    print(request.data['phone_number'])
    return Response({"message":"done"},status=status.HTTP_200_OK)

@api_view(['GET'])
def login_page(request):
    return render(request,'login.html')

@api_view(['POST'])
def user_info(request):
    return render(request,'user_data.html')

@api_view(['GET','POST'])
def registration_verification(request):
    data = request.data
    print(data)
    phone_number = data.get('phone_number')
    otp = data.get('otp')
    user = Otp.objects.filter(phone_number = phone_number , otp = otp).first()
    if user is None:
        return Response({"message : Wrong otp. Please enter correct otp"},status=status.HTTP_404_NOT_FOUND)
    
    user = User.objects.filter(phone_number = phone_number).first()
    if user is None:
        user_data = {
            'phone_number' : phone_number,
            'is_phone_verified' : True,
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'username' : phone_number
        }
        serializer = UserSerializer(data = user_data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        
        s = serializer.save()
        data = {
            'id' : s.id,
        }
        return Response(data , status=status.HTTP_200_OK)
    else:
        data = {
            'id' : user.id,
        }
        return Response(data , status=status.HTTP_200_OK)
    return Response({"message : Registration successfull"} , status=status.HTTP_200_OK)


@api_view(['GET'])
def user_page(request,id):
    context = {"id" : id}
    return render(request,'user_data.html',context)


@api_view(['POST'])
def user_info(request):
    data = request.data
    user = UserPersonalInfo.objects.filter(user_id = data['user_id']).first()
    if user is not None:
        user_info = UserPersonalInfo.objects.get(user_id=user.id)
        user_info = user_info[0]
        
        for field, value in data.items():
            setattr(user_info, field, value)

        user_info.save()
        return Response({"message" : "done"},status=status.HTTP_200_OK)
    
    serializer = UserPersonalInfoSerializer(data = data)
    if not serializer.is_valid():
        print(serializer.error_messages)
        print(serializer.errors)
        return Response({"message" : "Please fill the data correctly"},status=status.HTTP_200_OK)
    
    serializer.save()
    return Response({"message" : "User data submitted successfully"},status=status.HTTP_200_OK)


    return Response({"message" : "success"}, status=status.HTTP_200_OK)


#JYN3B9Q6HJ4VXGPQUPGFTL7L
import os
# from twilio.rest import Client
@api_view(['POST'])
def send_otp(request):
    data = request.data
    if data.get('phone_number') is None:
        return Response({
            'message': 'phone_number is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    # phone_number = "+91" + data['phone_number']
    phone_number = "+91" + data['phone_number']
    
    try:
        otp = random.randint(1000, 9999)
        user = Otp.objects.filter(phone_number=data['phone_number']).first()
        if user is None:
            n_data = {
                'phone_number': data['phone_number'],
                'otp': otp
            }
            serializer = Otp_serializer(data=n_data)
            if serializer.is_valid():
                serializer.save()
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.otp = otp
            user.save()
            # resend_otp(phone_number,otp)

            #2factor
        url = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/AUTOGEN"
        response = requests.get(url)

        # msg91
        # url = "https://control.msg91.com/api/v5/otp?mobile={phone_number}"
        # headers = {
        #     "accept": "application/json",
        #     "content-type": "application/json",
        #     "authkey": "411100ATxzK05iC656b6169P1"
        # }
        # payload = {
        #     "Param1": "value1",
        #     "Param2": "value2",
        #     "Param3": "value3"
        # }
        # response = requests.post(url,json=payload, headers=headers)

        if response.status_code == 200:
            return Response({"message": "Otp sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "something wrong with api"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # twilio
        # account_sid = 'AC5096305e5d145e94cf141d909517518b'
        # auth_token = '156fe76903255e27c0baa0126ac1378c'
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body = f'Your otp is {otp}',
        #     from_ = "+15005550006",
        #     to = phone_number
        # )
        # print(message.sid)

        # return Response({"message" : "Send"},status = status.HTTP_200_OK)




    except Exception as e:
        print(e)
        return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

