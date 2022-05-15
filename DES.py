from pyDes import des, ECB, PAD_PKCS5
import base64

# 秘钥
KEY = 'LT-14746146-VegandgF9ENS3ZFOaicz2YTcECC3Jd-https://csxrz.cqnu.edu.cn/cas'


def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    secret_key = KEY[0:8]  # 密码
    iv = secret_key  # 偏移
    # secret_key:加密密钥，CBC:加密模式，iv:偏移, padmode:填充
    des_obj = des(secret_key, ECB, secret_key, pad=None, padmode=PAD_PKCS5)
    # 返回为字节
    secret_bytes = des_obj.encrypt(s, padmode=PAD_PKCS5)
    # 返回为16进制
    return base64.encodebytes(secret_bytes)

print(des_encrypt("084413").decode())