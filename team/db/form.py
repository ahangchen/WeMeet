from django import forms


class JobForm(forms.Form):
    name = forms.CharField()
    j_type = forms.IntegerField(required=False, initial=0)
    min_salary = forms.FloatField(required=False,  initial=0)
    max_salary = forms.FloatField(required=False, initial=0)
    prince = forms.IntegerField(required=False, initial=0)
    city = forms.IntegerField(required=False, initial=0)
    town = forms.IntegerField(required=False, initial=0)
    exp_cmd = forms.CharField(required=False, initial='')
    w_type = forms.IntegerField(required=False, initial=0)
    job_cmd = forms.CharField(required=False, initial='')
    work_cmd = forms.CharField(required=False, initial='')
    pub_state = forms.IntegerField(required=False, initial=0)
    team_id = forms.IntegerField(required=False, initial=2)
    address = forms.CharField(required=False, initial='')

    def clean(self):
        cleaned_data = super(JobForm, self).clean()
        if self.is_valid():
            for name in self.fields:
                if  not self[name].html_name in self.data and self.fields[name].initial is not None or not cleaned_data[name]:
                    cleaned_data[name] = self.fields[name].initial
        return  cleaned_data

class ProductForm(forms.Form):
    name = forms.CharField()
    content = forms.CharField(required=False, initial='')
    # img_path = forms.CharField(required=False, initial='')
    reward = forms.CharField(required=False, initial='')
    # last_visit_cnt = forms.IntegerField(required=False, initial=0)
    # week_visit_cnt = forms.IntegerField(required=False, initial=0)
    team_id = forms.IntegerField(required=False, initial=2)

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        if self.is_valid():
            for name in self.fields:
                if  not self[name].html_name in self.data and self.fields[name].initial is not None or not cleaned_data[name]:
                    cleaned_data[name] = self.fields[name].initial
        return  cleaned_data
