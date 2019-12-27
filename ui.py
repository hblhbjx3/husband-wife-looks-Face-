from tkinter import *
import cv2
import os
from PIL import Image
from PIL import ImageTk
from face_compare import compare
from face_check import face_check
from tkinter import filedialog

BOARD_WIDTH = 704
BOARD_HEIGHT = 721
imgDict = {}
def getImgWidget(filePath):
    if os.path.exists(filePath) and os.path.isfile(filePath):
        if filePath in imgDict and imgDict[filePath]:
            return imgDict[filePath]
        img = Image.open(filePath)
        #print(img.size)
        img = ImageTk.PhotoImage(img)
        imgDict[filePath] = img
        return img
    return None

def face_photo(num):
    cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象 1调用外接摄像头
    while (cap.isOpened()):  # 循环读取每一帧
        ret_flag, Vshow = cap.read()  # 返回两个参数，第一个是bool是否正常打开，第二个是照片数组，如果只设置一个则变成一个tumple包含bool和图片
        cv2.imshow("camera", Vshow)     # 窗口显示，显示名为 Capture_Test
        k = cv2.waitKey(1) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
        if k == ord('s'):  # 若检测到按键 ‘s’，打印字符串
            Sshow = cv2.resize(Vshow, (320, 240))
            cv2.imwrite("getpics/" + str(num) + ".png", Sshow)
            str_jieguo.set("已 保 存"+ str(num) + ".png")
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



main = Tk()
str_jieguo = StringVar()
main.title("夫妻相-趣味测试")
main.geometry('704x721')
# 禁止改变窗口大小
main.resizable(width=False, height=False)
# 修改图标
main.iconbitmap('image/fq2.ico')

c1 = Canvas(main, background='white',
    width=BOARD_WIDTH, height=BOARD_HEIGHT)
c1.pack()
bg_img = PhotoImage(file='image/bg3.png')
paiBtn = PhotoImage(file='image/pai.png')
paiBtn2 = PhotoImage(file='image/s.png')
paiBtn3 = PhotoImage(file='image/h.png')
paiBtn4 = PhotoImage(file='image/daoru.png')
c1.create_image(BOARD_WIDTH /2, BOARD_HEIGHT/2, image=bg_img)

Button(main, text = '打开相机', command = photo, relief = FLAT, cursor = "hand2",
       image = paiBtn).place(relx=0.5, rely=0.81, anchor=CENTER)

def compare_str():
    t = open('num.txt', 'r')
    number = t.read()  # 递增，用来保存文件名
    t.close()
    num = int(number) - 1
    num = str(num)
    str_jieguo.set("网络出错 请重试！")
    bg4_img = getImgWidget('image/bg4.png')
    Label(main, image=bg4_img, compound=CENTER,text = '按下换脸按钮显示换脸图片', font = ('汉仪晓波折纸体简',14)
          ).place(relx=0.5, rely=0.4, anchor=CENTER)
    img_path = 'getpics/' + num + '.png'
    # 检查人脸数
    flag = face_check(img_path)
    if flag == 2:
        str1 = compare(img_path, num)
        print(str1)
        str_jieguo.set(str1)
    elif flag == 0:
        str_jieguo.set("未检测到人脸,请重新拍照")
    else:
        str_jieguo.set("仅检测到一张人,脸请重新拍照")

def huanlian():
    t = open('num.txt', 'r')
    number = t.read()  # 递增，用来保存文件名
    t.close()
    num = int(number) - 1
    num = str(num)
    img_path = "change/" + num + "(change).png"
    flag = os.path.exists(img_path)
    if flag == True:
        change_img = getImgWidget(img_path)
        Label(main, image = change_img, compound = CENTER
              ).place(relx=0.5, rely=0.4, anchor=CENTER)
    else:
        original_img = getImgWidget('getpics/' + num + '.png')
        Label(main, image = original_img, compound = CENTER
              ).place(relx=0.5, rely=0.4, anchor=CENTER)
        str_jieguo.set("大于两人才可换脸，显示原图")

def daoru():
    t = open('num.txt', 'r')
    number = t.read()  # 递增，用来保存文件名
    t.close()
    num = int(number) - 1
    num = str(num)
    img_path = filedialog.askopenfilename()
    flag = face_check(img_path)
    if flag == 2:
        str1 = compare(img_path, num)
        str_jieguo.set(str1)
        bg4_img = getImgWidget('image/bg4.png')
        Label(main, image=bg4_img, compound=CENTER, text='选择按钮进行下一步操作', font=('汉仪晓波折纸体简', 14)
              ).place(relx=0.5, rely=0.4, anchor=CENTER)
        image_change = "change/" + num + "(change).png"
        img = cv2.imread(image_change)
        cv2.imshow("imge", img)
        k = cv2.waitKey(0)
    elif flag == 0:
        str_jieguo.set("未检测到人脸,请重新拍照")
    else:
        str_jieguo.set("仅检测到一张人脸,请重新拍照")
    t = open('num.txt', 'w')
    num = int(number) + 1
    number = str(num)
    t.write(number)
    t.close()

#测试按钮
Button(main, text='测试', command=compare_str, relief=FLAT, cursor = "hand2",
       image=paiBtn2).place(relx=0.22, rely=0.81, anchor=CENTER)
#结果文字显示
Label(main, textvariable = str_jieguo, font = ('汉仪晓波折纸体简',18), foreground = 'red'
      ).place(relx=0.5, rely=0.185, anchor= CENTER)
#换脸按钮
Button(main, text='换脸', command=huanlian, relief=FLAT, cursor = "hand2",
       image=paiBtn3).place(relx=0.78, rely=0.81, anchor=CENTER)
#图片导入照片
Button(main, text='导入', command=daoru, relief=FLAT, cursor = "hand2",
       image=paiBtn4).place(relx=0.84, rely=0.15, anchor=CENTER)
main.mainloop()

