from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView

from .models import Student
from .serializers import StudentSerializer
from .users_serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = {
        "age": ["exact", "gte", "lte"],
    }

    search_fields = ["name", "email"]

    ordering_fields = ["name", "age", "created_at"]

    ordering = ["-id"]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Student.objects.all().order_by("-id")

        return Student.objects.filter(owner=user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)