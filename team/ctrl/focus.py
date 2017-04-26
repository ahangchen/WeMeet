from team.models import Focus
from team.db.focus import FocusJobSerializer, FocusTeamSerializer, FocusStuSerializer
from rest_framework import mixins, generics, viewsets

class FocusJobList(viewsets.ModelViewSet):
    queryset = Focus.objects.filter(focus_type=0)
    serializer_class = FocusJobSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    #
    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(focus_type=0)

    def get_queryset(self):
        queryset = Focus.objects.all()
        stu_id = self.request.query_params.get('student', None)
        if stu_id is not None:
            queryset = queryset.filter(focuser_id=stu_id)

        job_id = self.request.query_params.get('job', None)
        if job_id is not None:
            queryset = queryset.filter(focus_id=job_id)

        return queryset

class FocusTeamList(viewsets.ModelViewSet):
    queryset = Focus.objects.filter(focus_type=1)
    serializer_class = FocusTeamSerializer

    def perform_create(self, serializer):
        serializer.save(focus_type=1)

    def get_queryset(self):
        queryset = Focus.objects.all()
        stu_id = self.request.query_params.get('student', None)
        if stu_id is not None:
            queryset = queryset.filter(focuser_id=stu_id)

        team_id = self.request.query_params.get('team', None)
        if team_id is not None:
            queryset = queryset.filter(focus_id=team_id)

        return queryset

class FocusStuList(viewsets.ModelViewSet):
    queryset = Focus.objects.filter(focus_type=2)
    serializer_class = FocusStuSerializer

    def perform_create(self, serializer):
        serializer.save(focus_type=2)

    def get_queryset(self):
        queryset = Focus.objects.all()
        stu_id = self.request.query_params.get('student', None)
        if stu_id is not None:
            queryset = queryset.filter(focuser_id=stu_id)

        student_id = self.request.query_params.get('studentfocus', None)
        if student_id is not None:
            queryset = queryset.filter(focus_id=student_id)

        return queryset