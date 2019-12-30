> 基于Python开发一个HTTP接口测试工具客户端。

# 一、工具预览

![image-20191230145008462](C:\Users\yaoch\AppData\Roaming\Typora\typora-user-images\image-20191230145008462.png)



# 二、信息介绍

开发语言：Python3.7

第三方库：

- Pyqt5（绘制GUI界面）
- requests（发起http请求）
- xlrd（从excel中读取接口数据）
- PyInstaller（程序打包成exe发布）



# 三、功能清单

**已经实现**

1. `域名或IP`、`端口`、`请求次数`、`请求间隔（秒）`这四个字段的数据可以保存在配置文件中，每次客户端启动都会从配置文件中读取然后初始化在界面上。
2. `请求接口`下拉框选项和接口路径都通过excel文件进行维护并读取。
3. `【发起请求(F10)】`、`【保存信息(Ctrl+S)】`、`【清空日志(Ctrl+L)】`三种按钮操作支持快捷键
4. 日志打印支持Json格式美化输出，客户端界面打印日志的同时，也会在本地存储写入一份日志文件

**等待实现**

1. 接口关联，将A接口响应消息中的某字段值提取出来，自动作为B接口请求参数的值