from django.urls import path, include  
from .views import BookingCreateView, ObtainAuthToken, EventListView, UserBookingListView, CustomAuthToken
from .views import BookingUpdateView, BookingDeleteView
from .views import event_list
from . import views

urlpatterns = [
    # Ruta para la lista de eventos
    path('events/', EventListView.as_view(), name='event-list'),  # Asumiendo que EventListView maneja esta ruta

    # Ruta para la creación de reservas
    path('events/<int:event_id>/book/', BookingCreateView.as_view(), name='book_event'),

    # Ruta para la lista de reservas del usuario
    path('bookings/', UserBookingListView.as_view(), name='user_bookings'),

    # Rutas para autenticación
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),  # Autenticación básica
    path('api-token-auth/custom/', CustomAuthToken.as_view(), name='custom_api_token_auth'),  # Ruta personalizada para autenticación

    # Rutas para actualizar y eliminar reservas
    path('api/bookings/<int:pk>/', BookingUpdateView.as_view(), name='booking-update'),  # pk es el ID de la reserva
    path('api/bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking-delete'),  # pk es el ID de la reserva

    path('events/<int:event_id>/confirm-booking/', views.confirm_booking, name='confirm_booking'),

]

