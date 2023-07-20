from django.urls import path, include
from . import views

urlpatterns=[

    path('events/', views.EventListView.as_view(), name='Events'),
    path('perdorues/signup/', views.PerdoruesSignUpView.as_view(), name='Perdorues Sign Up'),
    path('event/create/', views.EventCreatedByManager.as_view(), name='Event Form')
]
