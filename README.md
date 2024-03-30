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

最后后点击确定即可。

## 应用部署

进入北京四或者上海一区域的函数工作流应用中心，点击“创建应用”，进入应用创建页面，点击“从模板创建”，选择“FFmpeg”模板，点击“使用模板”，进入参数配置页面，委托请选择前期准备中创建的委托，其他参数根据实际情况进行配置，点击“立即创建”，等待创建成功即可。

## 应用使用

### 获取函数URN
应用创建成功后，在应用详情页面下方的“资源”中可以看到创建出的函数的URN，函数URN是函数的唯一标识，在调用函数时需要使用函数URN。这样的函数URN共有6个，下面简要介绍每个函数的作用：

|函数URN(物理资源名称/ID)|函数名(逻辑名称)|介绍|
|--|--|--|
|urn:fss:region:project_id:function:default:ffmpeg-get-duration_2024xxxxxxxx:lastest|ffmpeg-get-duration|获取视频时长|
|urn:fss:region:project_id:function:default:ffmpeg-audio-convert_2024xxxxxxxx:lastest|ffmpeg-audio-convert|音频转码|
|urn:fss:region:project_id:function:default:ffmpeg-get-meta_2024xxxxxxxx:lastest|ffmpeg-get-meta|获取音视频元信息|
|urn:fss:region:project_id:function:default:ffmpeg-get-sprites_2024xxxxxxxx:lastest|ffmpeg-get-sprites|获取视频截帧|
|urn:fss:region:project_id:function:default:ffmpeg-video-gif_2024xxxxxxxx:lastest|ffmpeg-video-gif|视频转 GIF|
|urn:fss:region:project_id:function:default:ffmpeg-video-watermark_2024xxxxxxxx:lastest|ffmpeg-video-watermark|视频加水印|


### 创建 OBS 桶并上传输入文件

1. [获取 AK/SK](https://support.huaweicloud.com/qs-obs/obs_qs_0005.html)； 
2. 到[华为云 OBS](https://www.huaweicloud.com/product/obs.html)服务控制台应用所在区域创建一个 OBS 桶； 
3. 将输入媒体文件上传到 OBS 桶中。

### 调用函数

请参见[如何调用 API](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_0200.html)。

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

    client = FunctionGraphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(FunctionGraphRegion.value_of("cn-east-3")) \ # 函数所在区域，以上海一（cn-east-3）为例
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

    client = FunctionGraphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(FunctionGraphRegion.value_of("cn-east-3")) \ # 函数所在区域，以上海一（cn-east-3）为例
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
