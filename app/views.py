from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.serializers import *

from app.models import *


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
            return list project
        """
        try:
            user = CustomUser.objects.get(username=str(request.user))
            # check permission in AssignProject
            list_project = AssignProject.objects.filter(user=user.id)
            list_project_serializer = AssignProjectSerializer(list_project, many=True)
            return Response(
                {"list_project": list_project_serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
            auto add role PM
        """
        user = CustomUser.objects.get(username=str(request.user))
        try:
            assert user.is_management, "You are not management"
            # create project
            project_serializer = ProjectSerializer(data={
                "name_project": request.data["name_project"],
                "description_project": request.data["description_project"],
                "start_date_project": request.data["start_date_project"],
                "end_date_project": request.data["end_date_project"],
                "manager": user.id
            })
            project_serializer.is_valid(raise_exception=True)
            project_serializer.save()

            # add Role PM to Role of project
            role_serializer = RoleSerializer(data={
                "name_role": "PM",
                "description_role": "Project Manager",
                "author": user.id,
                "project": project_serializer.data["id_project"]
            })
            role_serializer.is_valid(raise_exception=True)
            role_serializer.save()

            if request.data["create_role_template"]:
                """
                    Developer (Dev) : Nhân viên phát triển
                    Tester (QC: Quality Control) – Nhân viên kiểm thử
                    Business Analysis (BA) : Nhân viên phân tích
                    Support Analysis (SPA) : Nhân viên hỗ trợ
                    Quality assurance (QA) : Nhân viên đảm bảo chất lượng
                    Technical Architect (TA) : Kiến trúc sư
                """
                dev_serializer = RoleSerializer(data={
                    "name_role": "Dev",
                    "description_role": "Nhân viên phát triển",
                    "author": user.id,
                    "project": project_serializer.data["id_project"]
                })
                dev_serializer.is_valid(raise_exception=True)
                dev_serializer.save()
                tester_serializer = RoleSerializer(data={
                    "name_role": "Tester",
                    "description_role": "Nhân viên kiểm thử",
                    "author": user.id,
                    "project": project_serializer.data["id_project"]
                })
                tester_serializer.is_valid(raise_exception=True)
                tester_serializer.save()
                ba_serializer = RoleSerializer(data={
                    "name_role": "BA",
                    "description_role": "Nhân viên phân tích",
                    "author": user.id,
                    "project": project_serializer.data["id_project"]
                })
                ba_serializer.is_valid(raise_exception=True)
                ba_serializer.save()
                spa_serializer = RoleSerializer(data={
                    "name_role": "SA",
                    "description_role": "Nhân viên hỗ trợ",
                    "author": user.id,
                    "project": project_serializer.data["id_project"]
                })
                spa_serializer.is_valid(raise_exception=True)
                spa_serializer.save()
                qa_serializer = RoleSerializer(data={
                    "name_role": "QA",
                    "description_role": "Nhân viên đảm bảo chất lượng",
                    "author": user.id,
                    "project": project_serializer.data["id_project"]
                })
                qa_serializer.is_valid(raise_exception=True)
                qa_serializer.save()
                ta_serializer = RoleSerializer(data={
                    "name_role": "TA",
                    "description_role": "Kiến trúc sư",
                    "author": user.id,
                    "project": project_serializer.data["id_project"]
                })
                ta_serializer.is_valid(raise_exception=True)
                ta_serializer.save()

            # add PM to AssignProject
            assign_project_serializer = AssignProjectSerializer(data={
                "project": project_serializer.data["id_project"],
                "user": user.id,
                "start_date_assign_project": project_serializer.data["start_date_project"],
                "end_date_assign_project": project_serializer.data["end_date_project"],
                "role_assign": role_serializer.data["id_role"]
            })
            assign_project_serializer.is_valid(raise_exception=True)
            assign_project_serializer.save()

            # add project to ProjectEditable 'id', 'id_user', 'id_project', 'is_activate'
            project_editable_serializer = ProjectEditSerializer(data={
                "id_user": user.id,
                "id_project": project_serializer.data["id_project"],
                "is_activate": True
            })
            project_editable_serializer.is_valid(raise_exception=True)
            project_editable_serializer.save()

            return Response(
                {"message": "Project created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        try:
            user = CustomUser.objects.get(username=str(request.user))
            assert user.is_management, "You are not management"

            current_project = Project.objects.get(id_project=request.data["id_project"])
            data = request.data
            project_serializer = ProjectSerializer(current_project, data={
                "name_project": data["name_project"]["content"] if data["name_project"][
                    "edit"] else current_project.name_project,
                "description_project": data["description_project"]["content"] if data["description_project"][
                    "edit"] else current_project.description_project,
                "start_date_project": data["start_date_project"]["content"] if data["start_date_project"][
                    "edit"] else current_project.start_date_project,
                "end_date_project": data["end_date_project"]["content"] if data["end_date_project"][
                    "edit"] else current_project.end_date_project,
                "manager": user.id,
            })
            project_serializer.is_valid(raise_exception=True)
            project_serializer.save()
            return Response(
                {"message": "Project updated successfully"},
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        try:
            user = CustomUser.objects.get(username=str(request.user))
            assert user.is_management, "You are not management"
            current_project = Project.objects.get(id_project=request.data["id_project"])
            del_serializer = ProjectSerializer(current_project)
            del_serializer.delete(current_project)

            return Response(
                {"message": "Project deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProcessAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = CustomUser.objects.get(username=str(request.user))
            # check permission in AssignProjectProcess
            list_process = AssignProjectProcess.objects.filter(id_assign=user.id)
            list_process_serializer = AssignProjectProcessSerializer(list_process, many=True)
            return Response(
                {"list_process": list_process_serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            user = CustomUser.objects.get(username=str(request.user))
            option = request.data["option"]
            if option == "process":
                # check permission in project editable
                project_editable = ProjectEditable.objects.get(id_project=request.data["id_project"], id_user=user.id)
                # create process, before add count num process and specifile rank of process
                count_process = Process.objects.filter(project=request.data["id_project"]).count()
                rank_process = count_process + 1
                process_serializer = ProcessSerializer(data={
                    "name_process": request.data["name_process"],
                    "description_process": request.data["description_process"],
                    "start_date_process": request.data["start_date_process"],
                    "end_date_process": request.data["end_date_process"],
                    "project": request.data["id_project"],
                    "manager": user.id,
                    'root_process': None,
                    "rank_process": rank_process
                })
                process_serializer.is_valid(raise_exception=True)
                process_serializer.save()

                # add PM to process editable if PM create process
                process_edit_serializer = ProcessEditableSerializer(data={
                    "id_user": user.id,
                    "id_process": process_serializer.data["id_process"],
                })
                process_edit_serializer.is_valid(raise_exception=True)
                process_edit_serializer.save()
                # add process to AssignProjectProcess
                assign_project_process_serializer = AssignProjectProcessSerializer(data={
                    "id_assign": user.id,
                    "id_process": process_serializer.data["id_process"]
                })
                assign_project_process_serializer.is_valid(raise_exception=True)
                assign_project_process_serializer.save()

                return Response(
                    {"message": "Process created successfully"},
                    status=status.HTTP_201_CREATED,
                )
            elif option == "sub_process":
                pass

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AssignProjectAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = CustomUser.objects.get(username=str(request.user))

        data = request.data
        option = data["option"]
        try:
            # check permission in project editable
            project_editable = ProjectEditable.objects.get(id_user=user.id, id_project=data["id_project"])
            assert project_editable.is_activate, "You are not permission"
            if option == "join_project":
                # check exist user in AssignProject
                user_assign = CustomUser.objects.get(username=data["user"])
                project_assign = Project.objects.get(id_project=data["id_project"])
                role_assign = Role.objects.get(name_role=data["role"], project=data["id_project"])
                assign_project = AssignProject.objects.filter(user=user_assign.id, project=project_assign.id_project,
                                                              role_assign=role_assign.id_role)
                assert not assign_project, "User already exists in AssignProject"

                # add user to AssignProject
                user_assign = CustomUser.objects.get(username=data["user"])
                project_assign = Project.objects.get(id_project=data["id_project"])
                role_assign = Role.objects.get(name_role=data["role"], project=data["id_project"])
                assign_project_serializer = AssignProjectSerializer(data={
                    "project": project_assign.id_project,
                    "user": user_assign.id,
                    "start_date_assign_project": data["start_date_assign_project"],
                    "end_date_assign_project": data["end_date_assign_project"],
                    "role_assign": role_assign.id_role
                })
                assign_project_serializer.is_valid(raise_exception=True)
                assign_project_serializer.save()


            elif option == "join_process":
                # add user to AssignProjectProcess
                user_assign_new = CustomUser.objects.get(username=data["user"])
                process_assign = AssignProject.objects.get(project=data["id_project"],
                                                           user=user_assign_new.id)
                assign_project_process_serializer = AssignProjectProcessSerializer(data={
                    "id_assign": process_assign.id_assign_project,
                    "id_process": data["id_process"]
                })

                assign_project_process_serializer.is_valid(raise_exception=True)
                assign_project_process_serializer.save()
            elif option == "join_task":
                # add user to Task editable
                user_assign_new = CustomUser.objects.get(username=data["user"])
                assign_project = AssignProject.objects.get(project=data["id_project"],
                                                           user=user_assign_new.id)
                assign_project_process = AssignProjectProcess.objects.get(id_assign=assign_project.id_assign_project,
                                                                          id_process=data["id_process"])
                current_task = Task.objects.get(id_task=data["id_task"])
                task_edit_serializer = TaskEditableSerializer(data={
                    "id_user": user_assign_new.id,
                    "id_task": current_task.id_task,
                })
                task_edit_serializer.is_valid(raise_exception=True)
                task_edit_serializer.save()
            return Response(
                {"message": f"User added {option} successfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": "You are not permission"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # check permissioin and get all task and status task in process which have user
        try:
            user = CustomUser.objects.get(username=str(request.user))
            # check permission in process editable
            list_task = Task.objects.filter(manager=user.id)
            list_task_serializer = TaskSerializer(list_task, many=True)
            return Response(
                {"list_task": list_task_serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def put(self, request):
        # check permission in task editable and update task
        try:
            user = CustomUser.objects.get(username=str(request.user))
            task_editable = TaskEditable.objects.get(id_user=user.id, id_task=request.data["id_task"])
            assert task_editable.is_activate, "You are not permission"
            current_task = Task.objects.get(id_task=request.data["id_task"])
            data = request.data

            project = current_task.project if not data["id_project"]["edit"] else Project.objects.get(id_project=data["id_project"]["content"])
            process = current_task.process if not data["id_process"]["edit"] else Process.objects.get(id_process=data["id_process"]["content"])
            print("status", data["status_task"]["edit"])
            task_serializer = TaskSerializer(current_task, data={
                "name_task": data["name_task"]["content"] if data["name_task"]["edit"] else current_task.name_task,
                "description_task": data["description_task"]["content"] if data["description_task"][
                    "edit"] else current_task.description_task,
                "create_date_task": data["create_date_task"]["content"] if data["create_date_task"][
                    "edit"] else current_task.create_date_task,
                "status_task": data["status_task"]["content"] if data["status_task"][
                    "edit"] else current_task.status_task,
                "start_date_task": data["start_date_task"]["content"] if data["start_date_task"][
                    "edit"] else current_task.start_date_task,
                "end_date_task": data["end_date_task"]["content"] if data["end_date_task"][
                    "edit"] else current_task.end_date_task,
                "project": project.id_project,
                "process": process.id_process,
                "manager": user.id,
            })
            task_serializer.is_valid(raise_exception=True)
            task_serializer.save()
            return Response(
                {"message": "Task updated successfully"},
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        # check permission in process editable
        try:
            user = CustomUser.objects.get(username=str(request.user))
            process_editable = ProcessEditable.objects.get(id_user=user.id, id_process=request.data["id_process"])
            assert process_editable.is_activate, "You are not permission"
            # count task with process, project
            count_task = Task.objects.filter(process=request.data["id_process"]).count()
            rank_task = count_task + 1
            # create task
            task_serializer = TaskSerializer(data={
                "name_task": request.data["name_task"],
                "description_task": request.data["description_task"],
                "create_date_task": request.data["create_date_task"],
                "start_date_task": request.data["start_date_task"],
                "end_date_task": request.data["end_date_task"],
                "project": request.data["id_project"],
                "process": request.data["id_process"],
                "manager": user.id,
                "rank_task": rank_task
            })
            task_serializer.is_valid(raise_exception=True)
            task_serializer.save()
            # add PM to task editable if PM create task
            task_edit_serializer = TaskEditableSerializer(data={
                "id_user": user.id,
                "id_task": task_serializer.data["id_task"],
            })
            task_edit_serializer.is_valid(raise_exception=True)
            task_edit_serializer.save()
            return Response(
                {"message": "Task created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
