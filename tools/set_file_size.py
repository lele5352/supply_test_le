import os

from PIL import Image, ImageFile, ImageFilter, ImageEnhance
import io

def set_size_file(fileName, w_size):
    filePaht = '/Users/huanglele/Desktop/' + fileName
    print(filePaht)
    while True:
        img_size = (os.path.getsize(filePaht)) / (1024 * 1024)
        print(img_size)
        if img_size > w_size:
            break
        else:
            with open(filePaht, "a+") as f:
                f.write("1234567890009876543211234567890987654323456789098765432123456789000987654321123456789098765432345678909876543212345678900098765432")
    print(img_size)

def add_pic(fileName,size):
    filePaht = '/Users/huanglele/Desktop/' + fileName

    # 防止图片超过178956970 pixels 而报错
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    Image.MAX_IMAGE_PIXELS = None
    # 读取原始图片
    with open(filePaht, 'rb') as f:
        image_data = f.read()

    # 指定目标内存大小（单位为字节）
    target_size = 1024 * 1024 * size  # 1 MB

    # 尝试增加分辨率和/或压缩质量来达到目标大小
    width, height = Image.open(io.BytesIO(image_data)).size
    while True:
        # 创建新的空白图片，并将原始图片粘贴到其中
        new_image = Image.new('RGB', (width, height), color='white')
        new_image.paste(Image.open(io.BytesIO(image_data)))

        # 将图片压缩到指定质量
        output = io.BytesIO()
        new_image.save(output, format='JPEG')
        new_image_data = output.getvalue()
        print(len(new_image_data))

        # 检查是否达到目标大小
        if len(new_image_data) >= target_size:
            break

        # 增加分辨率和/或压缩质量并重试
        width += 2000
        height += 2000

    # 保存图片到文件
    with open(filePaht, 'wb') as f:
        f.write(new_image_data)



if __name__ == '__main__':
    # set_size_file("1.jpeg", 5)
    # add_pic_v2("1.png", 15)
    # add_pic("unsplash.jpg", 12)

    """=当前可用信用额度+MAX((本次交易金额- MAX((当前已用额度+当前可用余额-当前信用额度),0),0)"""
    quota = 26000   #当前额度
    now_quota = 23000 #当前可用信用额度
    used_quota = 3000 #当前已用信用额度
    this = 6000 #本次交易金额

    abc = now_quota + max((this - max((used_quota + now_quota - quota), 0), 0))

    print(abc)

