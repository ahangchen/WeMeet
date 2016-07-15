import datetime

OUT_DATE_DAYS = 2


def pre_date(pre_days=OUT_DATE_DAYS+1):
    """
    设置日期为OUT_DATE_DAYS+1天前
    返回OUT_DATE_DAYS+1天前的日期字符串（Y-m-d)
    @OUT_DATE_DAYS：过期时长
    """
    d = datetime.datetime.now()
    date_str = '%s-%s-%s' % (d.year, d.month, d.day - pre_days)
    return date_str


def pass_days(pre_d_str):
    """
    计算pre_d_str到现在经过的天数
    @pre_d_str：日期字符串（Y-m-d)
    返回经过的天数
    """
    pre_d = datetime.datetime.strptime(pre_d_str, '%Y-%m-%d')
    now_d = datetime.datetime.now()
    return (now_d - pre_d).days


def now():
    """
    返回当前日期的字符串（Y-m-d)
    """
    d = datetime.datetime.now()
    date_str = '%s-%s-%s' % (d.year, d.month, d.day)
    return date_str

