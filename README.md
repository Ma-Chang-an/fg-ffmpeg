# fg-ffmpeg

## 应用说明
### FFmpeg简介

### FunctionGraph简介

## 前期准备

使用本应用你需要开通以下服务，**使用中可能产生费用**：
|服务|介绍|
|--|--|
|函数工作流 FunctionGraph|为FFmpeg提供算力|
|对象存储服务OBS|存储输入、输出媒体文件|

## 应用部署

## 应用使用
### 创建OBS桶并上传输入文件

1.[获取AK/SK](https://support.huaweicloud.com/qs-obs/obs_qs_0005.html)和[EndPoint](https://support.huaweicloud.com/qs-obs/obs_qs_0006.html)；
2. 到[华为云OBS](https://www.huaweicloud.com/product/obs.html)服务控制台EndPoint对应区域创建一个OBS桶；
3. 将输入媒体文件上传到OBS桶中。

### 配置环境变量

请参考[配置环境变量](https://support.huaweicloud.com/usermanual-functiongraph/functiongraph_01_0154.html)

|Key|Value|介绍|
|--|--|--|
|AccessKeyID|访问密钥ID（AK）|请参考[访问密钥](https://support.huaweicloud.com/usermanual-ca/ca_01_0003.html)|
|SecretAccessKey|秘密访问密钥（SK）|请参考[访问密钥](https://support.huaweicloud.com/usermanual-ca/ca_01_0003.html)|
|ENDPOINT|OBS桶的终端节点|请参考[终端节点（Endpoint）和访问域名](https://support.huaweicloud.com/productdesc-obs/obs_03_0152.html)|

### 调用函数
请参见[如何调用API](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_0200.html)。
#### 同步执行
请参考[同步执行函数](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_0125.html)
以获取视频时长为例，Python语言的调用demo如下
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
        request.x_cff_request_version = "v1"
        listInvokeFunctionRequestBodybody = {
            "bucket_name": "test-bucket", ## 请替换为你的OBS桶名
            "object_key": "a.mp4" ## 请替换为需要获取时长的视频路径
        }
        request.body = listInvokeFunctionRequestBodybody
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
