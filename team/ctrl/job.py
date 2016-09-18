from team.db import job
from rest_framework.views import APIView
from team.models import Job
from django.http import Http404
from team import db
from rest_framework.response import Response
from rest_framework import status

from enum import Enum

import logging
# PUB_STATE = Enum('待发布', '已发布', '已下架')
JOB_NOT_FOUND = -1


def info(job_id):
    obj = job.id_job(job_id)
    if obj is not None:
        return obj
    else:
        return JOB_NOT_FOUND

class JobList(APIView):
    def get(self, request):
        pk = request.GET.get('teamId', '')
        jobTags = request.GET.getlist('jobTags', [])
        jobTags = [ int(jobTag) for jobTag in jobTags ]

        job = Job.objects.filter(j_type__in=jobTags,team__id=pk).all()
        jobSerializes = db.job.JobSerializer(job, many=True)
        return Response(jobSerializes.data)

    def post(self, request):
        jobSerializer = db.job.JobSerializer(data=request.data)

        if not jobSerializer.is_valid():
            return Response(jobSerializer.errors, status.HTTP_400_BAD_REQUEST)

        jobSerializer.save()
        return Response(jobSerializer.data, status=status.HTTP_201_CREATED)

class JobDetail(APIView):
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404("The job is not exist.")

    def get(self, request, pk):
        job = self.get_object(pk)
        jobSerial = db.job.JobSerializer(job)
        return Response(jobSerial.data)

    def put(self, request, pk):
        job = self.get_object(pk=pk)
        jobSerializer = db.job.JobSerializer(job, data=request.data)
        if not jobSerializer.is_valid():
            return Response(jobSerializer.errors, status.HTTP_400_BAD_REQUEST)

        jobSerializer.save()
        return Response(jobSerializer.data)

    def delete(self, request, pk):
        job = self.get_object(pk=pk)
        logging.error(job)
        job.delete()
        return Response(status.HTTP_204_NO_CONTENT)