from rest_framework import serializers
from .models import Booking, Event

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['event', 'user', 'booking_date']
        read_only_fields = ['id', 'booking_date']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'capacity','created_at','updated_at']