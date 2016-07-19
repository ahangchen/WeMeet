from team.models import Job, Team

DB_OK = 0
DB_ACC_NOT_FOUND = 1


def id_job(job_id):
    job = Job.objects.filter(id=job_id).first()
    if job is None:
        return None
    else:
        return job

