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
    path(
        "<int:pk>/",
        AssignmentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
    ),
]