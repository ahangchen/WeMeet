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

class FocusTeamList(viewsets.ModelViewSet):
    queryset = Focus.objects.filter(focus_type=1)
    serializer_class = FocusTeamSerializer

    def perform_create(self, serializer):
        serializer.save(focus_type=1)

class FocusStuList(viewsets.ModelViewSet):
    queryset = Focus.objects.filter(focus_type=2)
    serializer_class = FocusStuSerializer

    def perform_create(self, serializer):
        serializer.save(focus_type=2)