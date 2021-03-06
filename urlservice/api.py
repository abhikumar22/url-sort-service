from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from uuid import uuid4
from decimal import Decimal
from urlservice.models import Urlsortner;
import string 
import random
import socket    
from django.http import HttpResponse 

class GetFullUrl(APIView):
    def post(self, request):

        curr_url = request.data.get("short_url")

        model = Urlsortner.objects.filter(sort_url=curr_url)
        # print("url",model)
        if model.count() > 0:
            data = {
            "full_url" : model[0].full_url,
            "status":status.HTTP_200_OK
            }        
    
        else :
            data = {
            "msg":"bad request",
            "status":status.HTTP_404_NOT_FOUND
        }  


        return Response(data, status=status.HTTP_200_OK)


class GetShortUrl(APIView):
    def post(self, request):

        curr_url = request.data.get("url")

        model = Urlsortner.objects.filter(full_url=curr_url)
        print("url",model)
        if model.count() > 0:
            data = {
            "short_url" : model[0].sort_url,
            "status":status.HTTP_200_OK
            }
        else:
            url_sort = Urlsortner()
            url_sort.full_url = curr_url

            N = 5
            random_str = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N)) 

            # checking if the pair is present in db
            new_model = Urlsortner.objects.filter(sort_url=random_str,full_url=curr_url)
            # print("****new_model****",new_model.query)
            # print("****DatA****",new_model.count())

            # if Combination present
            if new_model.count() > 0:
                data = {
                "short_url" : new_model[0].sort_url,
                "status":status.HTTP_200_OK
                } 
        
            else :
                url_sort.sort_url = random_str
                url_sort.save()
                data = {
                "short_url" : random_str,
                "status":status.HTTP_200_OK
                }

        
        return Response(data, status=status.HTTP_200_OK)

class GetIpInfo(APIView):       
    def get(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        hostname = socket.gethostname()    
        IPAddr = socket.gethostbyname(hostname)    
        print("Your Computer Name is:" + hostname)    
        print("Your Computer IP Address is:" + IPAddr)  

        html = "<html><body> IP Address = "+IPAddr+"..."+ip+"<br>Hostname = "+hostname+"</body></html>"
        return HttpResponse(html)

