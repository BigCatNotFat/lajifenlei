import cv2
import os
def capture_and_save_image(file_path):
    print('开始进行拍照')
    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 0是默认摄像头的索引

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 读取一帧
    ret, frame = cap.read()

    if not ret:
        print("无法从摄像头读取图像")
        return

    # 指定图片保存路径和文件名
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # 保存图片
    cv2.imwrite(file_path, frame)

    # 释放摄像头资源
    cap.release()
    cv2.destroyAllWindows()

    return file_path

