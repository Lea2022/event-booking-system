from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)  # Nombre del evento
    description = models.TextField()  # Descripción del evento
    location = models.CharField(max_length=100)  # Ubicación del evento
    date = models.DateTimeField()  # Fecha y hora del evento
    capacity = models.PositiveIntegerField()  # Capacidad máxima de asistentes
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del evento
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización

    def __str__(self):
        return self.title


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")  # Evento reservado
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")  # Usuario que reserva
    booking_date = models.DateTimeField(auto_now_add=True)  # Fecha de reserva

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    
    class Meta:
        unique_together = ('event', 'user')  # Restringe una reserva única por usuario y evento