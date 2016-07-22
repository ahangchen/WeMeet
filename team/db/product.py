from team.models import Product
from team.db.tag import *


def update(id, name=None, team=None, content=None,img_path=None,
           reward=None, last_visit_cnt=None,week_visit_cnt=None):
    """
        查询product,如果存在,返回项目信息,否则,返回错误信息
        成功：返回{'tag': PRODUCT_SUCCEED, 'msg': product}
        失败：返回{'tag': ERR_PROD_NOT_EXIT/ERR_PROD_TABLE,
                'msg': 错误信息}
    """
    prod_dict = ['name','team','content','img_path','reward','last_visit_cnt','week_visit_cnt']
    try:
        prod = Product.objects.all().get(id=id)
        prod_arg = locals()
        for key in prod_dict:
            if prod_arg[key] != None:
                prod.__dict__[key] = prod_arg[key]
        prod.save()
        return {'tag': PRODUCT_SUCCEED,
                'msg': prod}
    except Product.DoesNotExist:
        return {'tag': ERR_PROD_NOT_EXIT,
                'msg': MSG_PROD_NOT_EXIT}
    except:
        return {'tag': ERR_PROD_TABLE,
                'msg': MSG_PROD_TABLE}

def select(prod_id):
    """
        查询product,如果存在,返回项目信息,否则,返回错误信息
        成功：返回{'tag': PRODUCT_SUCCEED, 'msg': product}
        失败：返回{'tag': ERR_PROD_NOT_EXIT/ERR_PROD_TABLE,
                'msg': 错误信息}
    """
    try:
        product = Product.objects.all().get(id=prod_id)
        return {'tag': PRODUCT_SUCCEED,
                'msg': product}
    except Product.DoesNotExist:
        return {'tag': ERR_PROD_NOT_EXIT,
                'msg': MSG_PROD_NOT_EXIT}
    except:
        return {'tag': ERR_PROD_TABLE,
                'msg': MSG_PROD_TABLE}

