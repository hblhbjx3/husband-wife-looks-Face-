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


#拍照
def face_photo(num):
    cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象 1调用外接摄像头
    while (cap.isOpened()):  # 循环读取每一帧
        ret_flag, Vshow = cap.read()  # 返回两个参数，第一个是bool是否正常打开，第二个是照片数组，如果只设置一个则变成一个tumple包含bool和图片
        cv2.imshow("Capture_Test", Vshow)  # 窗口显示，显示名为 Capture_Test
        k = cv2.waitKey(1) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
        if k == ord('s'):  # 若检测到按键 ‘s’，打印字符串
            cv2.imwrite("getpics/" + str(num) + ".png", Vshow)
            print(cap.get(3));  # 得到长宽
            print(cap.get(4));
            print("success to save" + str(num) + ".png")
            print("-------------------------")
            num += 1
        elif k == ord('q'):  # 若检测到按键 ‘q’，退出
            break
    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 删除建立的全部窗口
    return num

def photo():
    # 拍照并保存
    t = open('num.txt', 'r')
    number = t.read()  # 递增，用来保存文件名
    t.close()
    num = int(number)
    t = open('num.txt', 'w')
    num = face_photo(num)
    number = str(num)
    t.write(number)
    t.close()
