import requests
import json
import cv2

#人脸数检测
def find_face_num(img_path):
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
    # 返回人脸矩形位置信息
    #print(data['face_num'])    #人脸数
    return data['face_num']

#人脸检测
def face_check(img_path):
    num = find_face_num(img_path)
    flag = 2
    if num == 0:
        flag = 0
    elif num == 1:
        flag = 1
    else:
        pass
    return flag
