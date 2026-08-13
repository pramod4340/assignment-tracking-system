"""
views.py — the "brain" of the assignments app.

A Django VIEW is just a Python function that receives a request
(what the user asked for) and returns a response (a web page).

For this page we write a plain FUNCTION-BASED VIEW — the simplest
kind of view — because we want every concept to be easy to see.
"""

from django.shortcuts import redirect, render

from rest_framework import status, viewsets
from rest_framework.response import Response

from .forms import AssignmentForm
from .models import Assignment
from .serializers import AssignmentSerializer


def assignment_list(request):
    """
    Show the "add assignment" form AND the list of assignments on ONE page.

    HTTP methods:

      * GET  -> "give me the page"
      * POST -> "here is form data, please save it"

    This function handles BOTH:
      1. GET  -> show an empty form and the assignments.
      2. POST -> validate and save the submitted assignment.
    """

    # ---- 1. Did the user submit the form? -------------------------
    if request.method == "POST":

        # Put submitted data into the form.
        form = AssignmentForm(request.POST)

        if form.is_valid():
            # Save the valid assignment to the database.
            form.save()

            # POST/Redirect/GET pattern.
            return redirect("assignments:assignment_list")

        # If the form is invalid, fall through and show the errors.

    else:
        # ---- 2. Normal page visit (GET) ----------------------------
        form = AssignmentForm()

    # Get all assignments from the database.
    assignments = Assignment.objects.all()

    # Render the HTML page.
    return render(
        request,
        "assignments/assignment_list.html",
        {
            "form": form,
            "assignments": assignments,
        },
    )


# ---------------------------------------------------------------------
# REST API
# ---------------------------------------------------------------------
class AssignmentViewSet(viewsets.GenericViewSet):
    """
    Complete CRUD API for assignments.

    GET     /api/assignments/       -> list all
    POST    /api/assignments/       -> create one
    GET     /api/assignments/{id}/  -> fetch one
    PUT     /api/assignments/{id}/  -> fully update one
    PATCH   /api/assignments/{id}/  -> partially update one
    DELETE  /api/assignments/{id}/  -> delete one
    """

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    # GET /api/assignments/
    def list(self, request):
        """Return every assignment."""

        assignments = Assignment.objects.all()

        serializer = AssignmentSerializer(
            assignments,
            many=True
        )

        return Response(serializer.data)

    # POST /api/assignments/
    def create(self, request):
        """Create a new assignment."""

        serializer = AssignmentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # GET /api/assignments/{id}/
    def retrieve(self, request, pk=None):
        """Return one assignment."""

        try:
            assignment = Assignment.objects.get(pk=pk)

        except Assignment.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AssignmentSerializer(assignment)

        return Response(serializer.data)

    # PUT /api/assignments/{id}/
    def update(self, request, pk=None):
        """Fully update an existing assignment."""

        try:
            assignment = Assignment.objects.get(pk=pk)

        except Assignment.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AssignmentSerializer(
            assignment,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PATCH /api/assignments/{id}/
    def partial_update(self, request, pk=None):
        """Partially update an existing assignment."""

        try:
            assignment = Assignment.objects.get(pk=pk)

        except Assignment.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AssignmentSerializer(
            assignment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE /api/assignments/{id}/
    def destroy(self, request, pk=None):
        """Delete an existing assignment."""

        try:
            assignment = Assignment.objects.get(pk=pk)

        except Assignment.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        assignment.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )