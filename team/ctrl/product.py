from team.db import product
from team.db.tag import *
from student.util import file_helper
from team.db.product import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from team.models import Product
from rest_framework import status
from rest_framework.decorators import api_view

import logging

DEFAULT_IMG = 'team/product/default.jpg'
IMG_PATH_ROOT = 'team/product'

class ProductList(APIView):
    def get(self, request):
        pk = request.GET.get('teamId', '')
        products = Product.objects.filter(team__id=pk).all()
        productSerializes = ProductSerializer(products, many=True)
        return Response(productSerializes.data)

    def post(self, request):
        productSerializer = ProductSerializer(data=request.data)

        if not productSerializer.is_valid():
            return Response(productSerializer.errors, status.HTTP_400_BAD_REQUEST)

        product = productSerializer.save()
        prod_img = request.FILES.get('prod_img')
        if prod_img:
            res_img = save_img(prod_id=product.id, prod_img=prod_img)
            if res_img['err'] != PRODUCT_SUCCEED:
                return Response(productSerializer.errors, status.HTTP_400_BAD_REQUEST)
            product.img_path = res_img['msg']

        productSerializer.save()
        return Response(productSerializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        product = ProductSerializer(product).data
        return Response(product)

    # def post(self, request, pk):
    #     productSerializer = ProductSerializer(data=request.data)
    #
    #     if not productSerializer.is_valid():
    #         return Response(productSerializer.errors, status.HTTP_400_BAD_REQUEST)
    #
    #     product = productSerializer.save()
    #     prod_img = request.FILES.get('prod_img')
    #     if prod_img:
    #         res_img = save_img(prod_id=product.id, prod_img=prod_img)
    #         if res_img['err'] != PRODUCT_SUCCEED:
    #             return Response(productSerializer.errors, status.HTTP_400_BAD_REQUEST)
    #         product.img_path = res_img['msg']
    #
    #     productSerializer.save()
    #     return Response(productSerializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        product = self.get_object(pk=pk)
        productSerializer = ProductSerializer(product, data=request.data)
        if not productSerializer.is_valid():
            return Response(productSerializer.errors, status.HTTP_400_BAD_REQUEST)

        prod_img = request.FILES.get('prod_img')
        if prod_img:
            res_img = save_img(prod_id=product.id, prod_img=prod_img)
            if res_img['err'] != PRODUCT_SUCCEED:
                return Response(productSerializer.errors, status.HTTP_400_BAD_REQUEST)
            product.img_path = res_img['msg']

        productSerializer.save()
        return Response(productSerializer.data)

    def delete(self, request, pk):
        product = self.get_object(pk=pk)
        delete_img(product.id)
        product.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    # @api_view(['GET'])
    # def list(request):
    #     pk = request.GET.get('teamId', '')
    #     products = Product.objects.filter(team__id=pk).all()
    #     productSerializes = ProductSerializer(products, many=True)
    #     return Response(productSerializes.data)

def save_img(prod_id, prod_img):
    """
    保存项目照片
    @prod_id: 项目id
    @prod_img: 照片文件
    成功：返回{'err': PRODUCT_SUCCEED, 'path': img_path}
    失败：返回{'err': ERR_PROD_TABLE/ERR_PROD_NOT_EXIT/ERR_PROD_SAVE_IMG/ERR_PROD_CHECK_IMG,
             'msg': 错误信息}
    """

    def check_img_file(file):  # TODO: Check avatar file
        """return true if avatar file is valid"""
        return True

    def get_img_path(file_name, file_type):
        return '%s/%s.%s' % (IMG_PATH_ROOT, file_name, file_type)

    # 确认项目是否存在
    prod_msg = product.select(prod_id)
    if prod_msg['err'] == PRODUCT_SUCCEED:
        prod = prod_msg['msg']
    else:
        return prod_msg

    # 项目存在，如果项目照片合法
    pre_img_path = prod.img_path
    if check_img_file(prod_img):
        # 使用项目ID作为照片名
        img_path = get_img_path(file_name=prod_id,
                                file_type=file_helper.get_file_type(prod_img.name))
        # 更新项目照片路径
        res = product.update(id=prod_id, img_path=img_path)
        # 更新项目照片路径
        if res['err'] == PRODUCT_SUCCEED:
            # 更新项目照片路径成功
            if file_helper.save(prod_img, img_path):
                return {'err': PRODUCT_SUCCEED,
                        'msg': img_path}
            # 更新项目照片路径成功失败， 回滚
            else:
                roll_tag = product.update(id=prod_id, img_path=img_path)
                # 如果回滚失败
                if roll_tag['err'] == PRODUCT_SUCCEED:
                    logging.error('更新项目照片，但数据库异常导致无法将更新的项目照片路径恢复')
                return {'err': ERR_PROD_SAVE_IMG,
                        'msg': MSG_PROD_SAVE_IMG}

        # 如果写入路径失败
        else:
            return res
    # 如果项目照片不合法
    else:
        return {'err': ERR_PROD_CHECK_IMG,
                'msg': MSG_PROD_CHECK_IMG}

def delete_img(prod_id):
    """
    删除项目照片
    @prod_id: 项目id
    成功：返回{'err': PRODUCT_SUCCEED, 'path': 操作成功}
    失败：返回{'err': ERR_PROD_DELETE_IMG/ERR_PROD_TABLE/ERR_PROD_NOT_EXIT,
             'msg': 错误信息}
    """

    # 确认项目是否存在
    prod_msg = product.select(prod_id)
    if prod_msg['err'] == PRODUCT_SUCCEED:
        prod = prod_msg['msg']
    else:
        return prod_msg

    # 项目照片删除出错
    if not file_helper.delete(prod.img_path):
        return {'err': ERR_PROD_DELETE_IMG, 'msg': MSG_PROD_DELETE_IMG}

    return {'err': PRODUCT_SUCCEED, 'msg': MSG_PRODUCT_SUCCEED}