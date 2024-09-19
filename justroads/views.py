import random

from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema_view
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ultralytics import YOLO

from justroads.docs import (
    MarkDocumentation,
    DefectStatusDocumentation,
    DefectDocumentation,
    MarkAnnotationDocumentation,
)
from justroads.models import (
    User,
    Defect,
    MarkAnnotation,
    DefectStatus,
    Mark,
)
from justroads.serializers import (
    LoginSerializer,
    LogoutSerializer,
    DefectSerializer,
    DefectStatusSerializer,
    MarkSerializer,
    TokenSerializer,
    MarkAnnotationSerializer,
)
from justroads_server.settings import BASE_DIR


# Create your views here.

class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            token = get_token(request)
            session = Session.objects.get(session_key=token)
            session_data = session.get_decoded()

            user_id = session_data.get("_auth_user_id")
            user = User.objects.get(id=user_id)

            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "patronymic": user.patronymic,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )
        except (Session.DoesNotExist, User.DoesNotExist):
            return None


class LoginViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            token = Token.objects.get(user=user)
            stoken = TokenSerializer(token).instance.key
            response = Response(
                {
                    "token": stoken,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "patronymic": user.patronymic,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

            return response
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        logout(request)
        response = Response(
            {"detail": "Successfully logged out"}, status=status.HTTP_200_OK
        )

        return response


@extend_schema_view(**DefectDocumentation())
class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']


@extend_schema_view(**MarkAnnotationDocumentation())
class MarkAnnotationViewSet(viewsets.ModelViewSet):
    queryset = MarkAnnotation.objects.all()
    serializer_class = MarkAnnotationSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']

    def list(self, request, *args, **kwargs):
        query_mark_id = self.request.query_params.get("mark_id")

        if query_mark_id is not None:
            queryset = MarkAnnotation.objects.filter(mark_id=query_mark_id)
            serializer = MarkAnnotationSerializer(queryset, many=True)
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema_view(**DefectStatusDocumentation())
class DefectStatusViewSet(viewsets.ModelViewSet):
    queryset = DefectStatus.objects.all()
    serializer_class = DefectStatusSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']


@extend_schema_view(**MarkDocumentation())
class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        # Границы России по широте и долготе
        MIN_LAT, MAX_LAT = 41.0, 81.0
        MIN_LON, MAX_LON = 19.0, 169.0

        if not request.data.get("longitude"):
            longitude = random.uniform(MIN_LON, MAX_LON)
            request.data.update({"longitude": round(longitude, 6)})
        if not request.data.get("latitude"):
            latitude = random.uniform(MIN_LAT, MAX_LAT)
            request.data.update({"latitude": round(latitude, 6)})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        image = serializer.data["image"].split("/")[-1]

        # Загрузка обученной модели
        model = YOLO(f"{BASE_DIR}/model/best.pt")

        # Выполнение детекции на изображении
        path_to_valid_data = f"{BASE_DIR}/media/images/{image}"

        results = model(path_to_valid_data)

        for i in range(len(results[0].__dict__["boxes"])):
            defect_class = int(results[0].__dict__["boxes"][0].cls.item()) + 1
            MarkAnnotation.objects.create(
                mark_id=Mark.objects.get(id=serializer.data["id"]),
                defect_id=Defect.objects.get(id=defect_class),
            )

        results[0].save(path_to_valid_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
