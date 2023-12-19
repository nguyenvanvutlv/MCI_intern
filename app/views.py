from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.serializers import UserSerializer, ProjectSerializer, ProcessSerializer, AssignProjectSerializer
from app.models import CustomUser, Project, Process, AssignProject, Role, AssignProjectProcess, Discuss


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
            # get param from request
            option_project = request.GET.get("option")
            if option_project == "all":
                projects = Project.objects.filter(manager=user)
                serializer = ProjectSerializer(projects, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                try:
                    projects = Project.objects.filter(manager=user, id_project=option_project)
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                serializer = ProjectSerializer(projects, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

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
        try:
            user = CustomUser.objects.get(username=str(request.user))
            assert user.is_management, "You are not management"
            assert user.username == request.data["manager"], "You are not management"
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        data = request.data
        data["manager"] = user.id
        try:
            project = Project.objects.get(manager=data["manager"])
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Project updated successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        try:
            user = CustomUser.objects.get(username=str(request.user))
            assert user.is_management, "You are not management"
            assert user.username == request.data["manager"], "You are not management"
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        data = request.data
        data["manager"] = user.id
        try:
            project = Project.objects.get(manager=data["manager"])
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid():
            serializer.delete(project)
            return Response(
                {"message": "Project deleted successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProcessAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = CustomUser.objects.get(username=str(request.user))
        if user.is_management:
            data = request.data
            data["manager"] = user.id

            id_project = data["project"]
            try:
                project = Project.objects.get(id_project=id_project)
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            data["project"] = project.id_project
            serializer = ProcessSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Process created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response({"message": "You are not management"})

    def get(self, request):
        user = CustomUser.objects.get(username=str(request.user))
        if user.is_management:
            # get param from request
            option_process = request.GET.get("option")
            if option_process == "all":
                processes = Process.objects.filter(manager=user)
                serializer = ProcessSerializer(processes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                try:
                    processes = Process.objects.filter(manager=user, id_process=option_process)
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                serializer = ProcessSerializer(processes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not management"})


class AssignProjectAPI(APIView):
    """
        Khi user được assign vào 1 project thì sẽ có 1 bản ghi trong bảng AssignProject, nhưng user đó chưa được xem các task của project đó
        cần phải tạo task trước khi assign user vào task đó
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = CustomUser.objects.get(username=str(request.user))
        if user.is_management:
            data = request.data
            id_user = data["user"]
            id_project = data["project"]
            id_role = data["role_assign"]
            try:
                user = CustomUser.objects.get(id=id_user)
                project = Project.objects.get(id_project=id_project)
                role = Role.objects.get(id_role=id_role)
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            data["user"] = user.id
            data["project"] = project.id_project
            data["role_assign"] = role.id_role
            serializer = AssignProjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Assign Project created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response({"message": "You are not management"})

    def get(self, request):
        user = CustomUser.objects.get(username=str(request.user))
        if user.is_management:
            # get param from request
            option_assign = request.GET.get("option")
            if option_assign == "all":
                assigns = AssignProject.objects.filter(manager=user)
                serializer = AssignProjectSerializer(assigns, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                try:
                    assigns = AssignProject.objects.filter(manager=user, id_assign_project=option_assign)
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                serializer = AssignProjectSerializer(assigns, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not management"})
