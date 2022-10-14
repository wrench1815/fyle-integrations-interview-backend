from django.urls import path

from .views import TeacherListCreateAPIView

urlpatterns = [
    path(
        'assignments/',
        TeacherListCreateAPIView.as_view(),
        name='teachers-assignments',
    ),
]
