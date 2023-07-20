from rest_framework import serializers
from .models import User, Manager, Perdorues, Event, PerdoruesJoinsEvent

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
        )


class EventListSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField()
    class Meta:
        model = Event
        fields = (
            'manager',
            'title',
            'date',
            'duration',
            'capacity',
            'image',
        )


class PerdoruesSignUpSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Perdorues
        fields = ('user', )

    def create(self, validated_data):
        print(validated_data)
        user_details = dict(validated_data.pop('user'))
        print(user_details)
        user = User.objects.create(is_active=True, **user_details)
        perdorues = Perdorues.objects.create(user=user)
        return perdorues

class EventCreateSerializer(serializers.ModelSerializer):

    image = serializers.ImageField()
    class Meta:
        model = Event
        fields = (
            'title',
            'date',
            'duration',
            'capacity',
            'image',
                  )


class AllEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
