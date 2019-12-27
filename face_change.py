import requests
import json
import base64
import shutil
import os

def find_face(img_path):
    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
    data = {"api_key": '******',
            "api_secret": '******',
            "return_attributes": 'age,gender,beauty'
            }
    files = {"image_file": open(img_path, "rb")}
    # 调用URL对应API接口，实现人脸属性检测
    response = requests.post(http_url, data=data, files=files)
    # 通过JSON分析响应的数据
    data = json.loads(response.text)
    #返回人脸矩形位置信息
    return data['faces']

def merge_face(ff1,ff2,image_template,image_merge,image_result,number):
    rectangele_1 = '{0},{1},{2},{3}'.format(ff1['top'],
                                            ff1['left'],
                                            ff1['width'],
                                            ff1['height'])

    rectangele_2 = '{0},{1},{2},{3}'.format(ff2['top'],
                                            ff2['left'],
                                            ff2['width'],
                                            ff2['height'])

    #使用opencv标记人脸矩形框
    #调用URL对应接口
    url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
    f1 = open(image_template, 'rb')
    f1_64 = base64.b64encode(f1.read()) #将图片编码成Base64二进制数据
    f1.close()
    f2 = open(image_merge, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    #按接口定义传递参数
    data = {"api_key": '2kgLjhMYkoXVXGCYMq9al1H0Nl1Aag7o',
            "api_secret": 'yityIEaogQ9PZLNgv71Wn0Hsj9_JdR9Z',
            "template_base64": f1_64,
            "template_rectangle": rectangele_1,
            "merge_base64": f2_64,
            "merge_rectangle": rectangele_2,
            "merge_rate": number
            }

    response = requests.post(url_add, data = data)
    #print(response.text)

    #通过JSON分析响应的数据，得到图片数据
    data = json.loads(response.text)
    result = data['result']
    #将base64编码的二进制图片数据解码
    imgdata = base64.b64decode(result) #解码
    #写入图片文档
    file = open(image_result, 'wb')
    file.write(imgdata) #保存图片到指定位置
    file.close()

def face_change(image_merge, image_result = 'new.png',image_result0='new2.png', ):
    shutil.copy(image_merge, 'copy.png')
    image_template = 'copy.png'
    ff = find_face(image_template)
    #face1 to face2
    ff1 = ff[0]['face_rectangle']  # 底版
    ff2 = ff[1]['face_rectangle']  # 被换脸 ff2->ff1
    merge_face(ff1,ff2,image_template, image_merge, image_result0, 10)
    #face2 to face1
    ff2 = ff[0]['face_rectangle']  # 底版
    ff1 = ff[1]['face_rectangle']  # 被换脸 ff1->ff2
    merge_face(ff1,ff2,image_result0, image_merge, image_result, 20)
    os.remove(image_template)
    os.remove(image_result0)

"""
#调用融合人脸函数
image_merge = "3.png"
image_name = image_merge[:-4]
image_result = "change/"+image_name+"(change).png"

face_change(image_merge,image_result)
"""


