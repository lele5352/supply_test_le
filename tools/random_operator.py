import random
import string
from faker import Faker
import time
def generate_random_str(randomlength=16):
  """
  生成一个指定长度的随机字符串，其中
  string.digits = 0123456789
  string.ascii_letters = abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
  string.punctuation = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

  """
  str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
  random_str = ''.join(str_list)
  return random_str


def generate_random_info(random_num):
    """
    生成一个指定数量的随机信息，包含但不限于：名字、地址、邮箱、电话等等，具体可百度了解Faker第三方库使用方法
    @param random_num: 数量
    @return:
    """
    faker = Faker(locale='zh_CN')
    list = []
    for i in range(random_num):
        str_info = {
            "name": faker.name(),
            "address": faker.address(),
            "email": faker.email(),
            "phone_number": faker.phone_number()
        }
        list.append(str_info)
    return list

def generate_random_no(prefix,i,suffix=None):
    """
    盘古系统随机单号生成器,例如：
    @param prefix:前缀，类似：DC、CK等
    @param i:单据尾号
    @param suffix:单号后缀
    @return:
    """
    year = '12'
    # 自动补齐8位长度，不足时左侧用"0"填充
    s = str(i).rjust(8, "0")
    if suffix:
        no = prefix + year + s + suffix
    else:
        no = prefix + year + s
    return no


if __name__ == '__main__':
    # generate_random_str()
    # generate_random_info(5)
    generate_random_no("DC", 1, suffix="-1")