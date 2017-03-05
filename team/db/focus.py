from team.models import Focus, Job, Team
from rest_framework import serializers
from student.models import StuInfo, StuSkill

class FocusJobSerializer(serializers.ModelSerializer):
    job_detail = serializers.SerializerMethodField()

    class Meta:
        model = Focus
        fields = ('focuser_id', 'focus_id', 'job_detail')

    def get_job_detail(self, obj):
        job = Job.objects.get(pk=obj.focus_id)
        if job is None:
            return None

        res = {}
        team = Team.objects.get(pk=job.team_id)
        res['name'] = job.name
        res['j_type'] = job.j_type
        res['team_name'] = team.name
        res['job_cmd'] = job.job_cmd
        res['min_salary'] = job.min_salary
        res['max_salary'] = job.max_salary
        res['team_logo'] = team.logo_path
        return res

class FocusTeamSerializer(serializers.ModelSerializer):
    team_detail = serializers.SerializerMethodField()

    class Meta:
        model = Focus
        fields = ('focuser_id', 'focus_id', 'team_detail')

    def get_team_detail(self, obj):
        team = Team.objects.get(pk=obj.focus_id)
        if team is None:
            return None

        res = {}
        res['name'] = team.name
        res['b_type'] = team.b_type
        res['slogan'] = team.slogan
        res['logo_path'] = team.logo_path
        return res

class FocusStuSerializer(serializers.ModelSerializer):
    stu_detail = serializers.SerializerMethodField()

    class Meta:
        model = Focus
        fields = ('focuser_id', 'focus_id', 'stu_detail')

    def get_stu_detail(self, obj):
        stu = StuInfo.objects.get(pk=obj.focus_id)
        if stu is None:
            return None

        skills = StuSkill.objects.filter(stu__id=stu.id)
        res = {}
        res['name'] = stu.name
        res['title'] = stu.title
        res['avatar_path'] = stu.avatar_path
        res['skills'] = [skill.name for skill in skills]
        return res