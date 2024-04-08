# fg-ffmpeg

## 应用说明

本应用帮助用户快速将 FFmpeg 部署到函数工作流上。提供了 FFmpeg 的部分音视频处理能力，其中包括音频转码、视频截图、截帧、时长获取、元信息获取，视频转 GIF、视频加水印等功能。本应用作为在函数上运行 FFmpeg 的基础模板，提供的能力并不是 FFmpeg 的全部功能，用户可以根据实际情况，参考我们的[应用构建工程](https://github.com/Ma-Chang-an/fg-ffmpeg)和[FFmpeg 官方文档](https://ffmpeg.org/ffmpeg.html)，进行二次开发。

### FFmpeg 简介

FFmpeg 是一个开源的跨平台音视频处理工具，它可以用来录制、转换以及流式传输音视频内容。它包含了一系列的音视频处理库和工具，能够完成各种各样的音视频处理任务，比如格式转换、裁剪、合并、分割、添加特效等。FFmpeg 支持几乎所有常见的音视频格式，因此被广泛应用于音视频处理、转码、流媒体服务等领域。由于其开源的特性，FFmpeg 也成为了很多多媒体软件和服务的基础技术之一

### FunctionGraph 简介

函数工作流（FunctionGraph）是一项基于事件驱动的函数托管计算服务。通过函数工作流，只需编写业务函数代码并设置运行的条件，无需配置和管理服务器等基础设施，函数以弹性、免运维、高可靠的方式运行。此外，按函数实际执行资源计费，不执行不产生费用。

## 前期准备

使用本应用你需要开通以下服务，**使用中可能产生费用**：
|服务|介绍|
|--|--|
|函数工作流 FunctionGraph|为 FFmpeg 提供算力|
|对象存储服务 OBS|存储输入、输出媒体文件|

本应用需要使用FunctionGraph服务访问 OBS 服务和 SWR服务，因此需要为函数配置具备访问这两个服务的委托。请参考[委托其他云服务管理资源](https://support.huaweicloud.com/usermanual-iam/iam_06_0004.html)创建IAM委托，其中云服务选择FunctionGraph，点击下一步

![](https://support.huaweicloud.com/usermanual-iam/zh-cn_image_0000001152549608.png)

在委托策略中添加以下策略：

|策略|介绍|
|--|--|
|OBS Administrator|授予FunctionGraph服务访问OBS服务的权限|
|SWR Administrator|授予FunctionGraph服务访问SWR服务的权限|

最后点击确定即可。

## 应用部署

进入北京四或者上海一区域的函数工作流应用中心，点击“创建应用”，进入应用创建页面，点击“从模板创建”，选择“FFmpeg”模板，点击“使用模板”，进入参数配置页面，委托请选择前期准备中创建的委托，其他参数根据实际情况进行配置，点击“立即创建”，等待创建成功即可。

## 应用使用

### 获取函数URN
应用创建成功后，在应用详情页面下方的“资源”中可以看到创建出的函数的URN，函数URN是函数的唯一标识，在调用函数时需要使用函数URN。这样的函数URN共有6个，下面简要介绍每个函数的作用：

|函数URN(物理资源名称/ID)|函数名(逻辑名称)|介绍|参数示例|
|--|--|--|--|
|urn:fss:region:project_id:function:default:ffmpeg-get-duration_2024xxxxxxxx:lastest|ffmpeg-get-duration|获取视频时长|{"bucket_name" : "test-bucket","object_key" : "a.mp4"}|
|urn:fss:region:project_id:function:default:ffmpeg-audio-convert_2024xxxxxxxx:lastest|ffmpeg-audio-convert|音频转码|{"bucket_name" : "test-bucket","object_key" : "a.mp3","output_dir" : "output/","dst_type": ".wav","ac": 1,"ar": 4000}|
|urn:fss:region:project_id:function:default:ffmpeg-get-meta_2024xxxxxxxx:lastest|ffmpeg-get-meta|获取音视频元信息|{"bucket_name" : "test-bucket","object_key" : "a.mp4"}|
|urn:fss:region:project_id:function:default:ffmpeg-get-sprites_2024xxxxxxxx:lastest|ffmpeg-get-sprites|获取视频截帧|{"bucket_name" : "test-bucket","object_key" : "a.mp4","output_dir" : "output/","tile": "3*4","start": 0,"duration": 10,"itsoffset": 0,"scale": "-1:-1","interval": 2,"padding": 1, "color": "black","dst_type": "jpg"}|
|urn:fss:region:project_id:function:default:ffmpeg-video-gif_2024xxxxxxxx:lastest|ffmpeg-video-gif|视频转 GIF|{"bucket_name" : "test-bucket","object_key" : "a.mp4","output_dir" : "output/","vframes" : 20,"start": 0,"duration": 2}|
|urn:fss:region:project_id:function:default:ffmpeg-video-watermark_2024xxxxxxxx:lastest|ffmpeg-video-watermark|视频加水印|{"bucket_name" : "test-bucket","object_key" : "a.mp4","output_dir" : "output/","vf_args" : "drawtext=fontfile=/Cascadia.ttf:text='my-watermark':x=50:y=50:fontsize=24:fontcolor=red:shadowy=1","filter_complex_args": "overlay=0:0:1"}|

#### 部分函数输入参数介绍
##### ffmpeg-get-sprites

```
{
    "bucket_name" : "test-bucket",
    "object_key" : "a.mp4",
    "output_dir" : "output/",
    "tile": "3*4",
    "start": 0,
    "duration": 10,
    "itsoffset": 0,
    "scale": "-1:-1",
    "interval": 2,
    "padding": 1, 
    "color": "black",
    "dst_type": "jpg"
}
tile: 必填， 雪碧图的 rows * cols
start: 可选， 默认是为 0
duration: 可选，表示基于 start 之后的多长时间的视频内进行截图，
比如 start 为 10， duration 为 20，表示基于视频的10s-30s内进行截图
interval: 可选，每隔多少秒截图一次， 默认为 1
scale: 可选，截图的大小, 默认为 -1:-1， 默认为原视频大小, 320:240, iw/2:ih/2 
itsoffset: 可选，默认为 0, delay多少秒，配合start、interval使用
- 假设 start 为 0， interval 为 10，itsoffset 为 0， 那么截图的秒数为 5， 15， 25 ...
- 假设 start 为 0， interval 为 10，itsoffset 为 1， 那么截图的秒数为 4， 14， 24 ...
- 假设 start 为 0， interval 为 10，itsoffset 为 4.999(不要写成5，不然会丢失0秒的那一帧图)， 那么截图的秒数为 0， 10， 20 ...
- 假设 start 为 0， interval 为 10，itsoffset 为 -1， 那么截图的秒数为 6， 16，26 ...
padding: 可选，图片之间的间隔, 默认为 0
color: 可选，雪碧图背景颜色，默认黑色， https://ffmpeg.org/ffmpeg-utils.html#color-syntax
dst_type: 可选，生成的雪碧图图片格式，默认为 jpg，主要为 jpg 或者 png， https://ffmpeg.org/ffmpeg-all.html#image2-1
```

##### ffmpeg-video-gif

```
{
    "bucket_name" : "test-bucket",
    "object_key" : "a.mp4",
    "output_dir" : "output/",
    "vframes" : 20,
    "start": 0,
    "duration": 2
}
start 可选， 默认是为 0
vframes  和 duration 可选， 当同时填写的时候， 以 duration 为准
当都没有填写的时候， 默认整个视频转为gif
```

###### ffmpeg-video-watermark

```
event format
{
    "bucket_name" : "test-bucket",
    "object_key" : "a.mp4",
    "output_dir" : "output/",
    "vf_args" : "drawtext=fontfile=/Cascadia.ttf:text='my-watermark':x=50:y=50:fontsize=24:fontcolor=red:shadowy=1",
    "filter_complex_args": "overlay=0:0:1"
}

filter_complex_args 优先级 > vf_args

vf_args:
- 文字水印
vf_args = "drawtext=fontfile=/Cascadia.ttf:text='my-watermark':x=50:y=50:fontsize=24:fontcolor=red:shadowy=1"
- 图片水印, 静态图片
vf_args = "movie=/logo.png[watermark];[in][watermark]overlay=10:10[out]"

filter_complex_args: 图片水印, 动态图片gif
filter_complex_args = "overlay=0:0:1"
```

##### ffmpeg-audio-convert

```
{
    "bucket_name" : "test-bucket",
    "object_key" : "a.mp3",
    "output_dir" : "output/",
    "dst_type": ".wav",
    "ac": 1,
    "ar": 4000
}
dst_type: 目标格式
ac: 可选，这个参数用于指定音频的通道数（Audio Channels），即音频文件中包含的独立声道数。通常情况下，值为1代表单声道（单通道），值为2代表立体声（双通道），值为6代表5.1环绕声等；
ar: 可选，这个参数用于指定音频的采样率（Audio Sampling Rate），即每秒钟采集和记录声音样本的次数。
```

### 创建 OBS 桶并上传输入文件

1. [获取 AK/SK](https://support.huaweicloud.com/qs-obs/obs_qs_0005.html)； 
2. 到[华为云 OBS](https://www.huaweicloud.com/product/obs.html)服务控制台应用所在区域创建一个 OBS 桶； 
3. 将输入媒体文件上传到 OBS 桶中。

### 调用函数

本文档以Python语言为例，介绍应用的使用方法，默认您本地已经具备Python 3.6以上运行环境，不再介绍Python环境具体安装过程，通过函数工作流API调用函数有REST风格API和SDK两种方式，本文以SDK方式为例进行介绍。

请阅读[函数工作流API参考](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_1600.html)学习REST风格API相关内容。

请阅读[函数工作流SDK参考](https://support.huaweicloud.com/sdkreference-functiongraph/functiongraph_07_0100.html)学习函数工作流SDK相关内容。

#### 同步执行

请参考[同步执行函数](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_0125.html)

以获取视频时长为例，Python 语言的调用 demo 如下

```python
# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkfunctiongraph.v2.region.functiongraph_region import FunctionGraphRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkfunctiongraph.v2 import *

if __name__ == "__main__":
    # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    ak = "xxxxxx" # 替换为上述内容中获取的AccessKeyID
    sk = "xxxxxxxxxx" # 替换为上述内容中获取的SecretAccessKey

    credentials = BasicCredentials(ak, sk) \

    # 函数所在区域，以上海一（cn-east-3）为例
    client = FunctionGraphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(FunctionGraphRegion.value_of("cn-east-3")) \ 
        .build()

    try:
        request = InvokeFunctionRequest()
        request.function_urn = "urn:fss:cn-east-3:xxxxxxxx:function:default:fg-ffmpeg-get-diratuon:latest" # 请将urn:fss:cn-east-3:xxxxxxxx:function:default:fg-ffmpeg-get-diratuon:latest替换为你的函数URN
        listInvokeFunctionRequestBody = {
            "bucket_name": "test-bucket", ## 请替换为你的OBS桶名
            "object_key": "a.mp4" ## 请替换为需要获取时长的视频路径
        }
        request.body = listInvokeFunctionRequestBody
        response = client.invoke_function(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
```

#### 异步调用

请参考[异步执行函数](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_0126.html)

以获取音频转码为例，Python 语言的调用 demo 如下，异步调用不会直接返回执行结果，用户可以在应用详情页点击对应函数的链接，进入函数详情页的“设置”-“异步设置”，查看异步调用的执行结果，输出的结果文件请到OBS桶的输出目录下载。

> 注意：获取视频时长和获取音视频元信息需要同步返回结果内容，因此不支持异步调用。

```python
# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkfunctiongraph.v2.region.functiongraph_region import FunctionGraphRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkfunctiongraph.v2 import *

if __name__ == "__main__":
    # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    ak = "xxxxxx" # 替换为上述内容中获取的AccessKeyID
    sk = "xxxxxxxxxx" # 替换为上述内容中获取的SecretAccessKey

    credentials = BasicCredentials(ak, sk) \

    # 函数所在区域，以上海一（cn-east-3）为例
    client = FunctionGraphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(FunctionGraphRegion.value_of("cn-east-3")) \
        .build()

    try:
        request = AsyncInvokeFunctionRequest()
        request.function_urn = "urn:fss:<region>:<project_id>:function:default:ffmpeg-get-duration_2024xxxxxxxx:lastest" # 请将urn:fss:<region>:<project_id>:function:default:ffmpeg-get-duration_2024xxxxxxxx:lastest替换为你的函数URN
        listAsyncInvokeFunctionRequestBody = {
            "bucket_name" : "test-bucket", # 请替换为你的OBS桶名
            "object_key" : "a.mp3", # 请替换为需要获取时长的视频路径
            "output_dir" : "output/", # 转换后的输出文件保存路径
            "dst_type": ".wav", # 转换后的文件格式
            "ac": 1, # 音频的通道数
            "ar": 4000 # 音频的采样率
        }
        request.body = listAsyncInvokeFunctionRequestBody
        response = client.async_invoke_function(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
```
