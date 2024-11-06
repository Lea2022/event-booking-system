from django.shortcuts import render, redirect, get_object_or_404


from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from django.views import View

from django.urls import reverse

from .models import Event, Booking

from .serializers import BookingSerializer
from .serializers import  EventSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.db.models import Count

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        return render(request, 'events/booking_form.html', {'event': event})

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        
        # Validación de cupo
        if event.bookings.count() >= event.capacity:
            return Response({"error": "Este evento ha alcanzado su capacidad máxima."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validación de reserva duplicada
        if Booking.objects.filter(event=event, user=request.user).exists():
            return Response({"error": "Ya tienes una reserva para este evento."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear reserva
        booking = Booking(event=event, user=request.user)
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ObtainAuthToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Credenciales inválidas."}, status=status.HTTP_400_BAD_REQUEST)


class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'location']
    

class UserBookingListView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    

class BookingUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)  # Permite que solo el usuario propietario actualice su reserva
    


class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)  # Permite que solo el usuario propietario elimine su reserva
    


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def home(request):
    events = Event.objects.annotate(confirmed_attendees=Count('bookings'))
    return render(request, 'events/home.html', {'events': events})



@login_required
def confirm_booking(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        if "confirm" in request.POST:
            # Crear la reserva
            Booking.objects.create(user=request.user, event=event)
            return redirect('home')  # Redirigir a la página principal después de confirmar
        elif "cancel" in request.POST:
            # Si el usuario cancela, también redirigir a la página principal
            return redirect('home')

    return render(request, 'events/confirm_booking.html', {'event': event})