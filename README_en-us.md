# fg-ffmpeg

## Application Description

This application helps users quickly deploy FFmpeg to function workflows. It provides partial audio and video processing capabilities of FFmpeg, including audio transcoding, video snapshot, frame extraction, duration retrieval, metadata retrieval, video to GIF conversion, video watermarking, and more. This application serves as a basic template for running FFmpeg on functions, and the capabilities provided are not all of FFmpeg's functionalities. Users can refer to our [application construction project](https://github.com/Ma-Chang-an/fg-ffmpeg) and [FFmpeg official documentation](https://ffmpeg.org/ffmpeg.html) for secondary development according to actual needs.

### Introduction to FFmpeg

FFmpeg is an open-source cross-platform audio and video processing tool. It can be used for recording, converting, and streaming audio and video content. It contains a series of audio and video processing libraries and tools, capable of performing various audio and video processing tasks such as format conversion, cropping, merging, splitting, and adding effects. FFmpeg supports almost all common audio and video formats, making it widely used in audio and video processing, transcoding, streaming media services, and other fields. Due to its open-source nature, FFmpeg has also become one of the fundamental technologies for many multimedia software and services.

### Introduction to FunctionGraph

FunctionGraph is an event-driven function hosting compute service. With FunctionGraph, you only need to write business function code and set the running conditions, without configuring and managing servers and other infrastructure. Functions run elastically, maintenance-free, and highly reliable. In addition, fees are incurred based on the actual execution resources of functions, and no fees are incurred if they are not executed.

## Preparations

To use this application, you need to enable the following services, **which may incur charges during use**:
| Service | Description |
|--|--|
| FunctionGraph | Provides computing power for FFmpeg |
| Object Storage Service (OBS) | Stores input and output media files |

This application needs to use the FunctionGraph service to access OBS and SWR services, so it needs to be configured with delegations to access these two services. Please refer to [Delegating Other Cloud Services to Manage Resources](https://support.huaweicloud.com/usermanual-iam/iam_06_0004.html) to create IAM delegations, select FunctionGraph as the cloud service, and click Next.

![](https://support.huaweicloud.com/usermanual-iam/zh-cn_image_0000001152549608.png)

Add the following policies to the delegation policy:

| Policy | Description |
|--|--|
| OBS Administrator | Grants FunctionGraph service access to OBS service |
| SWR Administrator | Grants FunctionGraph service access to SWR service |

Finally, click OK.

## Application Deployment

Enter the FunctionGraph application center in the Beijing 4 or Shanghai 1 region, click "Create Application" to enter the application creation page, click "Create from Template", select the "FFmpeg" template, click "Use Template", enter the parameter configuration page, select the delegation created in the preparation phase, configure other parameters according to actual needs, click "Create Now", and wait for the creation to succeed.

## Application Usage

### Get Function URN

After the application is created successfully, you can see the URN of the created function in the "Resources" section at the bottom of the application details page. The function URN is the unique identifier of the function and needs to be used when calling the function. There are 6 such function URNs, and below is a brief introduction to the function of each function:

| Function URN (Physical Resource Name/ID) | Function Name (Logical Name) | Description |Parameter Example |
|--|--|--|--|
|urn:fss:region:project_id:function:default:ffmpeg-get-duration_2024xxxxxxxx:lastest|ffmpeg-get-duration|Get video duration|{"bucket_name" : "test-bucket","object_key" : "a.mp4"}|
|urn:fss:region:project_id:function:default:ffmpeg-audio-convert_2024xxxxxxxx:lastest|ffmpeg-audio-convert|Audio transcoding|{"bucket_name" : "test-bucket","object_key" : "a.mp3","output_dir" : "output/","dst_type": ".wav","ac": 1,"ar": 4000}|
|urn:fss:region:project_id:function:default:ffmpeg-get-meta_2024xxxxxxxx:lastest|ffmpeg-get-meta|Get audio and video metadata|{"bucket_name" : "test-bucket","object_key" : "a.mp4"}|
|urn:fss:region:project_id:function:default:ffmpeg-get-sprites_2024xxxxxxxx:lastest|ffmpeg-get-sprites|Get video frames|{"bucket_name" : "test-bucket","object_key" : "a.mp4","output_dir" : "output/","tile": "3*4","start": 0,"duration": 10,"itsoffset": 0,"scale": "-1:-1","interval": 2,"padding": 1, "color": "black","dst_type": "jpg"}|
|urn:fss:region:project_id:function:default:ffmpeg-video-gif_2024xxxxxxxx:lastest|ffmpeg-video-gif|视频转 GIF|{"bucket_name" : "test-bucket","object_key" : "a.mp4","output_dir" : "output/","vframes" : 20,"start": 0,"duration": 2}|
|urn:fss:region:project_id:function:default:ffmpeg-video-watermark_2024xxxxxxxx:lastest|ffmpeg-video-watermark|ideo watermarking|{"bucket_name" : "test-bucket","object_key" : "a.mp4","output_dir" : "output/","vf_args" : "drawtext=fontfile=/Cascadia.ttf:text='my-watermark':x=50:y=50:fontsize=24:fontcolor=red:shadowy=1","filter_complex_args": "overlay=0:0:1"}|

#### Introduction to Partial Function Input Parameters

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
tile: Required, rows * cols of the sprite image
start: Optional, default is 0
duration: Optional, indicates the length of time within the video after start for capturing screenshots, e.g., start is 10, duration is 20, indicating capturing screenshots within 10s-30s of the video
interval: Optional, interval in seconds for capturing screenshots, default is 1
scale: Optional, size of the screenshots, default is -1:-1, which is the original size of the video, 320:240, iw/2:ih/2 
itsoffset: Optional, default is 0, delay in seconds, used in conjunction with start and interval
- Assuming start is 0, interval is 10, itsoffset is 0, then the screenshot seconds are 5, 15, 25 ...
- Assuming start is 0, interval is 10, itsoffset is 1, then the screenshot seconds are 4, 14, 24 ...
- Assuming start is 0, interval is 10, itsoffset is 4.999 (don't write as 5, otherwise the 0 second frame will be lost), then the screenshot seconds are 0, 10, 20 ...
- Assuming start is 0, interval is 10, itsoffset is -1, then the screenshot seconds are 6, 16, 26 ...
padding: Optional, spacing between images, default is 0
color: Optional, background color of the sprite image, default is black, https://ffmpeg.org/ffmpeg-utils.html#color-syntax
dst_type: Optional, format of the generated sprite image, default is jpg, mainly jpg or png, https://ffmpeg.org/ffmpeg-all.html#image2-1
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
start: Optional, default is 0
vframes and duration: Optional, when filled in simultaneously, duration takes precedence
When neither is filled in, the entire video is converted to a gif by default
```

##### ffmpeg-video-watermark

```
event format
{
    "bucket_name" : "test-bucket",
    "object_key" : "a.mp4",
    "output_dir" : "output/",
    "vf_args" : "drawtext=fontfile=/Cascadia.ttf:text='my-watermark':x=50:y=50:fontsize=24:fontcolor=red:shadowy=1",
    "filter_complex_args": "overlay=0:0:1"
}

filter_complex_args takes precedence over vf_args

vf_args:
- Text watermark
vf_args = "drawtext=fontfile=/Cascadia.ttf:text='my-watermark':x=50:y=50:fontsize=24:fontcolor=red:shadowy=1"
- Image watermark, static image
vf_args = "movie=/logo.png[watermark];[in][watermark]overlay=10:10[out]"

filter_complex_args: Image watermark, dynamic image gif
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
dst_type: Destination format
ac: Optional, specifies the number of audio channels, i.e., the number of independent channels in the audio file. Typically, 1 represents mono (single channel), 2 represents stereo (dual channel), and 6 represents 5.1 surround sound;
ar: Optional, specifies the audio sampling rate, i.e., the number of times per second that sound samples are collected and recorded.
```

### Create OBS Bucket and Upload Input Files

1. [Get AK/SK](https://support.huaweicloud.com/qs-obs/obs_qs_0005.html);
2. Create an OBS bucket in the region where the Huawei Cloud OBS service is located through the [Huawei Cloud OBS](https://www.huaweicloud.com/product/obs.html) service console;
3. Upload input media files to the OBS bucket.

### Call Function

This document introduces the usage of the application using Python language as an example. It assumes that you already have a Python 3.6 or above runtime environment installed on your local system. The document will not cover the specific installation process of Python environment. There are two ways to call functions through the Function Flow API: the REST API style and the SDK. This document will focus on the SDK method for illustration.

Please refer to the Function Flow API Reference for learning about the REST API related content.

Please refer to the Function Flow SDK Reference for learning about the Function Flow SDK related content.

#### Synchronous Execution

Please refer to [Synchronous Execution of Functions](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_0125.html).

Taking the example of getting the video duration, the Python language call demo is as follows:

```python
# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkfunctiongraph.v2.region.functiongraph_region import FunctionGraphRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkfunctiongraph.v2 import *

if __name__ == "__main__":
    # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    ak = "xxxxxx" # Replace with the AccessKeyID obtained above
    sk = "xxxxxxxxxx" # Replace with the SecretAccessKey obtained above

    credentials = BasicCredentials(ak, sk) \

    # The region where the function is located, taking Shanghai 1 (cn-east-3) as an example
    client = FunctionGraphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(FunctionGraphRegion.value_of("cn-east-3")) \ 
        .build()

    try:
        request = InvokeFunctionRequest()
        request.function_urn = "urn:fss:cn-east-3:xxxxxxxx:function:default:fg-ffmpeg-get-diratuon:latest" # Please replace urn:fss:cn-east-3:xxxxxxxx:function:default:fg-ffmpeg-get-diratuon:latest with your function URN
        listInvokeFunctionRequestBody = {
            "bucket_name": "test-bucket", ## Replace with your OBS bucket name
            "object_key": "a.mp4" ## Replace with the path of the video whose duration needs to be obtained
        }
        request.body = listInvokeFunctionRequestBody
        response = client.invoke_function(request)
        print(response

)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
```

#### Asynchronous Call

Please refer to [Asynchronous Execution of Functions](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_0126.html).

Taking the example of audio transcoding, the Python language call demo is as follows. Asynchronous calls do not directly return the execution result, and users can click the link of the corresponding function in the application details page to enter the function details page, "Settings"-"Asynchronous Settings", to view the execution result of the asynchronous call. The output result file can be downloaded from the output directory of the OBS bucket.

> Note: Getting video duration and getting audio and video metadata require synchronous return result content, so asynchronous calls are not supported.

```python
# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkfunctiongraph.v2.region.functiongraph_region import FunctionGraphRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkfunctiongraph.v2 import *

if __name__ == "__main__":
    # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    ak = "xxxxxx" # Replace with the AccessKeyID obtained above
    sk = "xxxxxxxxxx" # Replace with the SecretAccessKey obtained above

    credentials = BasicCredentials(ak, sk) \

    # The region where the function is located, taking Shanghai 1 (cn-east-3) as an example
    client = FunctionGraphClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(FunctionGraphRegion.value_of("cn-east-3")) \ 
        .build()

    try:
        request = AsyncInvokeFunctionRequest()
        request.function_urn = "urn:fss:<region>:<project_id>:function:default:ffmpeg-get-duration_2024xxxxxxxx:lastest" # Please replace urn:fss:<region>:<project_id>:function:default:ffmpeg-get-duration_2024xxxxxxxx:lastest with your function URN
        listAsyncInvokeFunctionRequestBody = {
            "bucket_name" : "test-bucket", # Replace with your OBS bucket name
            "object_key" : "a.mp3", # Replace with the path of the video whose duration needs to be obtained
            "output_dir" : "output/", # The path where the converted output file is saved
            "dst_type": ".wav", # The format of the converted file
            "ac": 1, # Number of audio channels
            "ar": 4000 # Audio sampling rate
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

#### Disclaimer

1. This application serves only as a simple example for users to refer to and learn from. If used in actual production environments, users are advised to refer to the image building project for self-improvement and optimization. Issues encountered during usage of function workflows can be consulted through service tickets. For issues related to open-source projects, users should seek help from the open-source community or resolve them on their own.