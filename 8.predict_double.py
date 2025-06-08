import cv2
import numpy as np
from ultralytics import YOLO


def detect_gap_and_calculate_distance(slider_img_path, bg_img_path, model):
    """
    识别滑块和背景缺口，并计算滑动距离
    :param slider_img_path: 滑块图片路径（小图）
    :param bg_img_path: 背景图片路径（含缺口的大图）
    :param model: YOLO 模型（需能检测滑块和缺口）
    :return: 滑动距离（像素）
    """
    # 读取图片
    slider_img = cv2.imread(slider_img_path)
    bg_img = cv2.imread(bg_img_path)
    if slider_img is None or bg_img is None:
        print("错误：图片读取失败！")
        return None

    # YOLO 检测滑块和缺口
    slider_results = model(slider_img)  # 检测滑块（小图）
    bg_results = model(bg_img)  # 检测缺口（大图）

    # 解析滑块位置（从滑块小图中检测）
    slider_box = None
    if len(slider_results[0].boxes) > 0:
        slider_box = slider_results[0].boxes.xyxy[0].cpu().numpy().astype(int)  # [x1, y1, x2, y2]

    # 解析缺口位置（从背景大图中检测）
    gap_box = None
    if len(bg_results[0].boxes) > 0:
        gap_box = bg_results[0].boxes.xyxy[0].cpu().numpy().astype(int)  # [x1, y1, x2, y2]

    # 计算滑动距离（缺口x1 - 滑块x1）
    distance = None
    if slider_box is not None and gap_box is not None:
        distance = gap_box[0] - slider_box[0]  # 水平移动距离
        print(f"滑块位置: {slider_box}, 缺口位置: {gap_box}, 滑动距离: {distance}")

    # 可视化结果（可选）
    if slider_box is not None:
        cv2.rectangle(slider_img, (slider_box[0], slider_box[1]), (slider_box[2], slider_box[3]), (0, 255, 0), 2)
        cv2.putText(slider_img, "Slider", (slider_box[0], slider_box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow("Slider Detection", slider_img)

    if gap_box is not None:
        cv2.rectangle(bg_img, (gap_box[0], gap_box[1]), (gap_box[2], gap_box[3]), (0, 0, 255), 2)
        cv2.putText(bg_img, "Gap", (gap_box[0], gap_box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Gap Detection", bg_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return distance


def main():
    # 加载训练好的 YOLO 模型（需能检测滑块和缺口）
    model = YOLO("models/slider_gap.pt")  # 替换为你的模型路径

    # 输入滑块图片和背景图
    slider_img_path = "slider.png"  # 滑块小图
    bg_img_path = "bg.png"  # 背景大图（含缺口）

    # 计算滑动距离
    distance = detect_gap_and_calculate_distance(slider_img_path, bg_img_path, model)
    print(f"滑动距离: {distance}")


if __name__ == "__main__":
    main()
