import datetime
import time

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .permissions import *
from rest_framework import status
from django.utils import timezone
# Create your views here.


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer

class PerdoruesSignUpView(generics.CreateAPIView):
    queryset = Perdorues.objects.all()
    serializer_class = PerdoruesSignUpSerializer


class EventCreatedByManager(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = (CreateEventPermission, )

    def create(self, request, *args, **kwargs):
        username = request.user
        try:
            manager = Manager.objects.get(user__username=username)
        except Exception as e:
            print('Manager not Found')
            return Response({'message': 'Errror Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        print(request.data['date'])
        print(timezone.now())
        # if(request.data['data'] < datetime.datetime.now().__str__()):
        #     return Response({'message': 'DATE/TIME is earlier than the actual time!'}, status=status.HTTP_400_BAD_REQUEST)
        event_serializer = EventCreateSerializer(data=request.data)
        if event_serializer.is_valid():
            Event.objects.create(manager=manager, **event_serializer.validated_data)
            return Response(data=event_serializer.data, status=status.HTTP_200_OK)
        return Response(data=event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


