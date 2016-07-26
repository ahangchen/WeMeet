import base64
from io import BytesIO

from django.http import HttpResponse

# from student.models import StuInfo
from team.util.image import create_validate_code


def validate(request):
    mstream = BytesIO()

    img, validate_code = create_validate_code()
    img.save(mstream, "GIF")
    request.session['code'] = validate_code
    print(validate_code)
    # StuInfo().save()
    # StuInfo.objects.all()
    img_bytes = base64.b64encode(mstream.getvalue()).decode()
    return HttpResponse(img_bytes)