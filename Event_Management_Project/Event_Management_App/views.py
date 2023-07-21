from datetime import datetime
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .permissions import *
from rest_framework import status
from django.core import serializers as _ser
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
        event_time = request.POST['date']
        datetime_object = datetime.strptime(event_time, '%Y-%m-%dT%H:%M')
        print(datetime_object)
        print(datetime.now())
        if(datetime_object < datetime.now()):
            return Response({'message': 'DATE/TIME is earlier than the actual time!'}, status=status.HTTP_400_BAD_REQUEST)

        event_serializer = EventCreateSerializer(data=request.data)
        if event_serializer.is_valid():
            Event.objects.create(manager=manager,
                                 date=datetime_object,
                                 title=event_serializer.validated_data['title'],
                                 duration=event_serializer.validated_data['duration'],
                                 capacity=event_serializer.validated_data['capacity'],
                                 image=event_serializer.validated_data['image'],
                                 )
            return Response(data=event_serializer.data, status=status.HTTP_200_OK)
        return Response(data=event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerCheckPerdoruesRegistered(APIView):

    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            manager = Manager.objects.get(user__username=request.user)
        except Exception as e:
            print(e)
            return Response({'message': 'ERROR, NO EVENT REGISTERED OR NO PREMISSION'}, status=status.HTTP_400_BAD_REQUEST)
        print(PerdoruesJoinsEvent.objects.all())
        perdorues_joins_events = PerdoruesJoinsEvent.objects.filter(event__title__contains=event, event__manager=manager)
        print(perdorues_joins_events)
        print(event)
        perdorues_joins_events_serializer = ManagerChecksRegisteredPerdoruesSerializer(perdorues_joins_events, many=True)
        return Response(perdorues_joins_events_serializer.data, status=status.HTTP_200_OK)




class PerdoruesJoinsEventsView(generics.CreateAPIView):
    queryset = PerdoruesJoinsEvent.objects.all()
    serializer_class = PerdoruesJoinsEventSerializer
    permission_classes = (JoinEventPerdoruesPermission, IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        try:
            perdorues = Perdorues.objects.get(user__username=request.user)
        except Exception as e:
            print('Perdorues Not Found')
            return Response({'message': 'ERROR USER NOT FOUND!!'}, status=status.HTTP_400_BAD_REQUEST)
        perdorues_joins_event = PerdoruesJoinsEventSerializer(data=request.data)

        if perdorues_joins_event.is_valid():
            try:
                event_wanted = Event.objects.get(title=perdorues_joins_event.validated_data['event'])
            except Exception as e:
                print('Problem')
                return Response({'message': 'ERROR, could not find the event'}, status=status.HTTP_400_BAD_REQUEST)
            print(event_wanted)
            perdorues_other_events = PerdoruesJoinsEvent.objects.filter(
                event__date__day=event_wanted.date.day).filter(perdorues=perdorues)
            print(event_wanted.duration)
            for the_events_in_the_same_day in perdorues_other_events:
                if the_events_in_the_same_day.event.date + the_events_in_the_same_day.event.duration >= event_wanted.date or event_wanted.date + event_wanted.duration >= the_events_in_the_same_day.event.date:
                    return Response({'message': 'ERROR, Event Collision'}, status=status.HTTP_400_BAD_REQUEST)
            if event_wanted.current_capacity >= event_wanted.capacity:
                return Response({'message': 'ERORR! Event full capacity!!'})
            event_wanted.current_capacity += 1
            event_wanted.save()
            PerdoruesJoinsEvent.objects.create(perdorues=perdorues, **perdorues_joins_event.validated_data)
            return Response(perdorues_joins_event.data, status=status.HTTP_200_OK)
        return Response(perdorues_joins_event.errors, status=status.HTTP_400_BAD_REQUEST)







