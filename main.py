import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap
from myDetect import myDetect
from takePhoto import capture_and_save_image

modelPath = 'yolov8s.pt'
detectLists = []
count = 0

class DetectionThread(QThread):
    finished = pyqtSignal(str, list)  # 发送完成信号，传递图片路径和识别结果
    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path

    def run(self):
        # 在后台线程中捕获图像
        image_path = capture_and_save_image('./raw.jpg')
        if not image_path:
            self.finished.emit('', ['无法从摄像头读取图像'])
            return
        # 调用识别函数，并传递结果
        detected_names = myDetect(self.model_path, image_path)
        self.finished.emit(image_path, detected_names)
class CameraTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.垃圾识别总数 = 0
        self.total_detections = 0  # 统一变量名
        self.setWindowTitle('垃圾分类')
        self.setGeometry(400, 400, 640, 480)
        # Create layout
        layout = QVBoxLayout()
        # Add photo label
        self.photo_label = QLabel('请点击拍摄')
        layout.addWidget(self.photo_label)

        # Add Take button
        self.take_button = QPushButton('拍摄')
        self.take_button.clicked.connect(self.take_photo)
        layout.addWidget(self.take_button)

        # Add Record button (Not functional here)
        self.record_button = QPushButton('模型加载')
        layout.addWidget(self.record_button)

        # Add success text box
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)
        self.text_box.setText('请加载模型')
        self.setLayout(layout)

    def take_photo(self):
        self.text_box.setText('正在处理...')
        self.take_button.setDisabled(True)  # 禁用按钮防止重复点击
        # 开启后台线程处理图像捕获和识别
        self.thread = DetectionThread(modelPath)
        self.thread.finished.connect(self.on_detection_finished)
        self.thread.start()

    def on_detection_finished(self, image_path, detected_names):
        # 更新界面显示结果
        detectLists = detected_names

        pixmap = QPixmap('./result.jpg')
        if pixmap.isNull():
            self.text_box.setText('加载图片失败！')
        else:
            self.photo_label.setPixmap(pixmap)
            if not detectLists:
                self.text_box.setText('未检测到物体！')
            elif len(detectLists) > 1:
                self.text_box.setText('检测到多个物体！')
            else:
                self.text_box.setText('识别成功！\n识别结果为：' + ''.join(detectLists) + '\n下面进行垃圾分类')
                self.total_detections += 1
                self.text_box.append(f'已经分类 {self.total_detections} 个物体')
        self.take_button.setEnabled(True)  # 识别结束后重新启用按钮

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraTestApp()
    ex.show()
    sys.exit(app.exec_())
