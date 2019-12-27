import requests
import json
import base64
from face_change import face_change
from face_change import find_face

str2 = '出错'

def face_compare(img_path):
    face_token = find_face(img_path)
    face_token_1 = face_token[0]['face_token']
    face_token_2 = face_token[1]['face_token']
    url_add = "https://api-cn.faceplusplus.com/facepp/v3/compare"
    data = {"api_key": '******',
            "api_secret": '******',
            "face_token1": face_token_1,
            "face_token2": face_token_2
            }
    # 调用URL对应API接口，实现相似度检测
    response = requests.post(url_add, data=data)
    # 通过JSON分析响应的数据
    data = json.loads(response.text)
    #print(response.text)
    return data['confidence']
    """"""

#美颜
def beauty_face(img_path,image_result):
    #调用URL对应接口
    url_add = "https://api-cn.faceplusplus.com/facepp/v1/beautify"
    face = open(img_path, 'rb')
    face_64 = base64.b64encode(face.read()) #将图片编码成Base64二进制数据
    face.close()
    #按接口定义传递参数
    data = {"api_key": '2kgLjhMYkoXVXGCYMq9al1H0Nl1Aag7o',
            "api_secret": 'yityIEaogQ9PZLNgv71Wn0Hsj9_JdR9Z',
            "image_base64": face_64
            #"whitening": 50,
            #"smoothing": 50
            }
    response = requests.post(url_add, data = data)
    #通过JSON分析响应的数据，得到图片数据
    data = json.loads(response.text)
    #print(data)
    result = data['result']
    #将base64编码的二进制图片数据解码
    imgdata = base64.b64decode(result) #解码
    #写入图片文档
    file = open(image_result, 'wb')
    file.write(imgdata) #保存图片到指定位置
    file.close()

#人脸关系
def relationship(img_path):
    str = '夫妻'
    face = find_face(img_path)
    face_1 = face[0]['attributes']
    face_2 = face[1]['attributes']
    gender_1 = face_1['gender']['value']  # 性别
    gender_2 = face_2['gender']['value']
    age_1 = face_1['age']['value']  #年龄
    age_2 = face_1['age']['value']
    age_0 = age_1 - age_2
    if age_0 < -15 or age_0 > 15:
        if gender_1 == gender_2:
            if gender_1 == 'Male':
                str = '父子'
            else:
                str = '母女'
        else:
            if (age_1 > age_2 and gender_1 == 'Male') or (age_1 < age_2 and gender_2 == 'Male'):
                str = '父女'
            else:
                str = '母子'
    else:
        if gender_1 == gender_2:
            if gender_1 == 'Male':
                str = '兄弟'
            else:
                str = '姐妹'
        else:
            pass
    return str

#人脸相似度
def compare(img_path,num):
    face = find_face(img_path)
    face_1 = face[0]['attributes']
    face_2 = face[1]['attributes']
    beauty_1 = (face_1['beauty']['female_score'] + face_1['beauty']['male_score']) / 2  #颜值
    beauty_2 = (face_2['beauty']['female_score'] + face_2['beauty']['male_score']) / 2
    #num = img_path[:-4]
    #image_result1 = "beauty/" + num + "(beauty).png"
    image_result2 = "change/" + num + "(change).png"
    #beauty_face(img_path, image_result1)
    #face_change(image_result1, image_result2)
    face_change(img_path, image_result2)
    #相似度
    sim_sore = face_compare(img_path)
    str = relationship(img_path)
    if sim_sore < 20:
        str2 = "没有"+str+"相"
    elif sim_sore < 30 and sim_sore >= 20:
        str2 = "有"+str+"相"
    else:
        str2 = "非常有"+str+"相"
    return str2
    #print(gender_1, gender_2)
    #print(beauty_1, beauty_2)

"""
image_path = "5.png"
num = image_path[:-4]
image_result = "beauty/" + num + "(beauty).png"

beauty_face(image_path, image_result)

compare('20.png')"""