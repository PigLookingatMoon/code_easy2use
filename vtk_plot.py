
import vtk
import numpy as np
import SimpleITK as sitk

# # 读取nii格式的数据
# reader = vtk.vtkNIFTIImageReader()
# reader.SetFileName(r"D:\project-zc\GuXiaoLiang\data\1_CHEN HAO YAN.nii")

# 结合源数据和mask提取ROI
img_path = r"D:\project-zc\GuXiaoLiang\data\case10.nii"
mask_path = r"D:\project-zc\GuXiaoLiang\data\case10_mask.nii"
img_array = sitk.GetArrayFromImage(sitk.ReadImage(img_path))
mask_array = sitk.GetArrayFromImage(sitk.ReadImage(mask_path))
ROI = np.multiply(img_array, mask_array)

# 将 array 数据转换成 vtkImageData 对象
# data_array = np.random.rand(10, 10, 10)  # 随机生成 10x10x10 的数组数据
data_array = ROI
imageData = vtk.vtkImageData()
imageData.SetDimensions(data_array.shape)
imageData.SetSpacing(1, 1, 1)
imageData.SetOrigin(0, 0, 0)
imageData.AllocateScalars(vtk.VTK_DOUBLE, 1)  # 使用 VTK_DOUBLE 类型保存数组数据

# 将数据填充到 vtkImageData 中
for z in range(data_array.shape[2]):
    for y in range(data_array.shape[1]):
        for x in range(data_array.shape[0]):
            pixelValue = data_array[x, y, z]  # 获取像素数据
            idx = imageData.ComputePointId((x, y, z))
            imageData.GetPointData().GetScalars().SetTuple1(idx, pixelValue)

# 设置颜色映射
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-3000, 0, 0, 0)        # 0, 0, 0 黑色
colorFunc.AddRGBPoint(-2000, 0, 0, 0)        # 0, 0, 1 蓝色
colorFunc.AddRGBPoint(-1000, 0, 0, 0)        # 0, 1, 1 青色
colorFunc.AddRGBPoint(0, 0, 0, 0)            # 1, 1, 0 绿色
colorFunc.AddRGBPoint(1000, 1, 1, 0)         # 1, 0.5, 0 黄色
colorFunc.AddRGBPoint(1500, 1, 0, 0)         # 1, 0, 0 红色
colorFunc.AddRGBPoint(1800, 1, 0.5, 1)       # 1, 0.5, 1 紫色
colorFunc.AddRGBPoint(2000, 1, 1, 1)         # 1, 1, 1 白色

# 创建一个Volume（体数据）
volumeMapper = vtk.vtkSmartVolumeMapper()
# volumeMapper.SetInputConnection(reader.GetOutputPort()) # 从reader获得imagedata
volumeMapper.SetInputData(imageData)  # 设置由array_img获得的imagedata
volumeMapper.SetBlendModeToComposite()

# 创建Volume的属性
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorFunc)
volumeProperty.SetScalarOpacityUnitDistance(1.0)
volumeProperty.ShadeOn()
volumeProperty.SetDiffuse(0.7)
volumeProperty.SetSpecular(0.3)
volumeProperty.SetSpecularPower(20)

# 设置不透明度
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(-1000, 0.0)
opacityTransferFunction.AddPoint(-500, 0.0)
opacityTransferFunction.AddPoint(0, 0.1)
opacityTransferFunction.AddPoint(500, 0.2)
opacityTransferFunction.AddPoint(1000, 0.3)
volumeProperty.SetScalarOpacity(opacityTransferFunction)

# 创建Volume对象
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# 创建渲染器
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)
renderer.SetBackground(1.0,1.0,1.0)

# 设置窗口背景色为黑色
renderer.SetBackground(vtk.vtkNamedColors().GetColor3d("Black"))

# 创建RenderWindow
renWin = vtk.vtkRenderWindow()
renWin.SetSize(600, 600)
renWin.AddRenderer(renderer)

# 将黑色背景部分设为透明
ren = renWin.GetRenderers().GetFirstRenderer()
ren.SetUseDepthPeeling(True)
ren.SetOcclusionRatio(0.1)

# 创建交互窗口
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# 开始绘制
renWin.Render()
iren.Start()
