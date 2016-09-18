from team.models import Product
from team.db.tag import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'img_path', 'content', 'reward', 'team',
                  'last_visit_cnt', 'week_visit_cnt')


def update(id, name=None, img_path=None, content=None,
           reward=None, team_id=None):
    """
        查询product,如果存在,更新项目信息,否则,返回错误信息
        成功：返回{'err': PRODUCT_SUCCEED, 'msg': product}
        失败：返回{'err': ERR_PROD_NOT_EXIT/ERR_PROD_TABLE,
                'msg': 错误信息}
    """
    prod_dict = ['name', 'img_path','content','reward', 'team_id']
    try:
        prod = Product.objects.all().get(id=id)
        prod_arg = locals()
        for key in prod_dict:
            if prod_arg[key] != None:
                prod.__dict__[key] = prod_arg[key]
        prod.save()
        return {'err': PRODUCT_SUCCEED,
                'msg': prod}
    except Product.DoesNotExist:
        return {'err': ERR_PROD_NOT_EXIT,
                'msg': MSG_PROD_NOT_EXIT}
    except:
        return {'err': ERR_PROD_TABLE,
                'msg': MSG_PROD_TABLE}

def select(prod_id):
    """
        查询product,如果存在,返回项目信息,否则,返回错误信息
        成功：返回{'err': PRODUCT_SUCCEED, 'msg': product}
        失败：返回{'err': ERR_PROD_NOT_EXIT/ERR_PROD_TABLE,
                'msg': 错误信息}
    """
    try:
        product = Product.objects.all().get(id=prod_id)
        return {'err': PRODUCT_SUCCEED,
                'msg': product}
    except Product.DoesNotExist:
        return {'err': ERR_PROD_NOT_EXIT,
                'msg': MSG_PROD_NOT_EXIT}
    except:
        return {'err': ERR_PROD_TABLE,
                'msg': MSG_PROD_TABLE}


def insert(team_id, name=None, content=None, reward=None):
    """
        插入项目信息
        成功：返回{'err': PRODUCT_SUCCEED, 'msg': product}
        失败：返回{'err': ERR_PROD_NOT_EXIT/ERR_PROD_TABLE,
                 'msg': 错误信息}
    """
    prod_dict = ['name', 'content', 'reward']
    try:
        prod = Product(team_id=team_id)
        prod_arg = locals()
        for key in prod_dict:
            if prod_arg[key] != None:
                prod.__dict__[key] = prod_arg[key]
        prod.save()
        return {'err': PRODUCT_SUCCEED,
                'msg': prod}
    except:
        return {'err': ERR_PROD_TABLE,
                'msg': MSG_PROD_TABLE}


def newest():
    products = Product.objects.all().order_by('-id')[: 3]
    products_ret = [
        {'pid': product.id,
         'tid': product.team_id,
         'p_img': product.img_path,
         'p_name': product.name,
         't_name': product.team.name
         } for product in products
        ]
    return products_ret