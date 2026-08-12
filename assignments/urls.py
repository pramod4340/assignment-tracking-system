from django.urls import path
from .views import AssignmentViewSet

urlpatterns = [
    path(
        "",
        AssignmentViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),
]