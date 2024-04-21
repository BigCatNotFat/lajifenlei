from ultralytics import YOLO

def myDetect(modelPath_, imagePath):
    # 加载模型
    model = YOLO(modelPath_)
    # 对指定图片进行推理
    results = model(imagePath)  # 返回 Results 对象列表

    detected_objects = []
    # 遍历结果中的每个物体
    for result in results:
        # 获取每个检测到的物体的类别索引
        for cls in result.boxes.cls:
            # 使用类别索引从 names 字典中获取类别名称
            detected_objects.append(result.names[int(cls)])
    # 可选：将结果保存到文件
    result.save(filename='result.jpg')

    # 返回检测到的所有物体的名称列表
    return detected_objects