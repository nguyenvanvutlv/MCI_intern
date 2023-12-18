from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.serializers import UserSerializer, ProjectSerializer
from app.models import CustomUser, Project


# Create your views here.


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"message": "Logout successfull"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response({"message": "User created unsuccessfully"},
                        status=status.HTTP_400_BAD_REQUEST)


class ProjectAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
            Return a list of all projects of user
        """
        user = CustomUser.objects.get(username=str(request.user))
        if user.is_management:
            projects = Project.objects.filter(manager=user)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "You are not management"})

    def post(self, request):
        user = CustomUser.objects.get(username=str(request.user))
        if user.is_management:
            data = request.data
            data["manager"] = user.id
            serializer = ProjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Project created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response({"message": "You are not management"})

    def put(self, request):
        return Response({"message": "HELLO PUT"})
        user = CustomUser.objects.get(username=str(request.user))
        # if user.is_management:
        #     data = request.data
        #     project = Project.objects.get(id_project=data["id_project"])
        #     serializer = ProjectSerializer(project, data=data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(
        #             {"message": "Project updated successfully"},
        #             status=status.HTTP_201_CREATED,
        #         )
        #     else:
        #         return Response(
        #             serializer.errors,
        #             status=status.HTTP_400_BAD_REQUEST,
        #         )
        # else:
        #     return Response({"message": "You are not management"})
