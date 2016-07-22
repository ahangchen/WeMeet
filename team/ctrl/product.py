from team.db import product
from team.db.tag import *
from student.util import file_helper
import logging

DEFAULT_IMG = 'team/product/default.jpg'
IMG_PATH_ROOT = 'team/product'

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