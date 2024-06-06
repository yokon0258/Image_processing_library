#--------------------------------------------------------#
#   该文件用于调整标签的格式
#--------------------------------------------------------#
import os

import numpy as np
from PIL import Image
from tqdm import tqdm

#-----------------------------------------------------------------------------------#
#   Origin_SegmentationClass_path   原始标签所在的路径
#   Out_SegmentationClass_path      输出标签所在的路径
#                                   处理后的标签为灰度图，如果设置的值太小会看不见具体情况。
#-----------------------------------------------------------------------------------#
Origin_SegmentationClass_path   = "D:\PythonProgram\segmentation-format-fix-main\out1"
Out_SegmentationClass_path      = "D:\PythonProgram\segmentation-format-fix-main\out2"

#-----------------------------------------------------------------------------------#
#   Origin_Point_Value  原始标签对应的像素点值
#   Out_Point_Value     输出标签对应的像素点值
#                       Origin_Point_Value需要与Out_Point_Value一一对应。
#   举例如下，当：
#   Origin_Point_Value = np.array([0, 255])；Out_Point_Value = np.array([0, 1])
#   代表将原始标签中值为0的像素点，调整为0，将原始标签中值为255的像素点，调整为1。
#
#   示例中仅调整了两个像素点值，实际上可以更多个，如：
#   Origin_Point_Value = np.array([0, 128, 255])；Out_Point_Value = np.array([0, 1, 2])
#
#   也可以是数组（当标签值为RGB像素点时），如
#   Origin_Point_Value = np.array([[0, 0, 0], [1, 1, 1]])；Out_Point_Value = np.array([0, 1])
#-----------------------------------------------------------------------------------#
list1 = []
list2 = []
# 将灰度值按照128分开
for i in range(256):
    list1.append(i)

for i in range(128):
    list2.append(0)

for i in range(128, 256):
    list2.append(255)

# list2[0] = 0
# print(list1)
# print(list2)
Origin_Point_Value              = np.array(list1)
Out_Point_Value                 = np.array(list2)

if __name__ == "__main__":
    if not os.path.exists(Out_SegmentationClass_path):
        os.makedirs(Out_SegmentationClass_path)

    #---------------------------#
    #   遍历标签并赋值
    #---------------------------#
    png_names = os.listdir(Origin_SegmentationClass_path)
    print("正在遍历全部标签。")
    for png_name in tqdm(png_names):
        png     = Image.open(os.path.join(Origin_SegmentationClass_path, png_name))
        w, h    = png.size
        
        png     = np.array(png)
        out_png = np.zeros([h, w])
        # 这段代码的功能是将一张图片（png）中指定像素点的值（Origin_Point_Value）替换为另一个像素点的值（Out_Point_Value）。
        #
        # 具体实现方法是先用循环遍历Origin_Point_Value中的每一个像素点的值，然后用numpy库生成一个布尔型的掩码（mask）数组，其中与Origin_Point_Value[i]
        # 值相等的像素点为True，其他为False。如果png是一个彩色图片，则先将mask数组从3维转换为2维。最后将out_png中符合掩码条件的像素点的值替换为Out_Point_Value[i]。
        for i in range(len(Origin_Point_Value)):
            mask = png[:, :] == Origin_Point_Value[i]
            if len(np.shape(mask)) > 2:
                mask = mask.all(-1)
            out_png[mask] = Out_Point_Value[i]
        
        out_png = Image.fromarray(np.array(out_png, np.uint8))
        out_png.save(os.path.join(Out_SegmentationClass_path, png_name))

    #-------------------------------------#
    #   统计输出，各个像素点的值得个数
    #-------------------------------------#
    print("正在统计输出的图片每个像素点的数量。")
    classes_nums        = np.zeros([256], np.int)
    for png_name in tqdm(png_names):
        png_file_name   = os.path.join(Out_SegmentationClass_path, png_name)
        if not os.path.exists(png_file_name):
            raise ValueError("未检测到标签图片%s，请查看具体路径下文件是否存在以及后缀是否为png。"%(png_file_name))
        
        png             = np.array(Image.open(png_file_name), np.uint8)
        classes_nums    += np.bincount(np.reshape(png, [-1]), minlength=256)
        
    print("打印像素点的值与数量。")
    print('-' * 37)
    print("| %15s | %15s |"%("Key", "Value"))
    print('-' * 37)
    for i in range(256):
        if classes_nums[i] > 0:
            print("| %15s | %15s |"%(str(i), str(classes_nums[i])))
            print('-' * 37)