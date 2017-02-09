import datetime
from haystack import indexes
from team.models import Team, Product, Job

class TeamIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    team_name = indexes.CharField(model_attr='name')
    team_logo = indexes.CharField(model_attr='logo_path')
    team_about = indexes.CharField(model_attr='about')
    team_type = indexes.IntegerField(model_attr='b_type')

    def get_model(self):
        return Team

class JobIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    job_name = indexes.CharField(model_attr='name')
    job_type = indexes.CharField(model_attr='j_type')
    min_salary = indexes.FloatField(model_attr='min_salary')
    max_salary = indexes.FloatField(model_attr='max_salary')
    job_summary = indexes.CharField(model_attr='summary')

    team_id = indexes.CharField(model_attr='team__id')
    team_logo_path = indexes.CharField(model_attr='team__logo_path')
    team_name = indexes.CharField(model_attr='team__name')
    team_type = indexes.IntegerField(model_attr='team__b_type')
    team_about = indexes.CharField(model_attr='team__about')

    def get_model(self):
        return Job

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    product_name = indexes.CharField(model_attr='name')
    product_content = indexes.CharField(model_attr='content')
    product_img_path = indexes.CharField(model_attr='img_path')

    team_id = indexes.CharField(model_attr='team__id')
    team_logo_path = indexes.CharField(model_attr='team__logo_path')
    team_name = indexes.CharField(model_attr='team__name')
    team_type = indexes.IntegerField(model_attr='team__b_type')
    team_about = indexes.CharField(model_attr='team__about')

    def get_model(self):
        return Product