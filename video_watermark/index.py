import subprocess
import os
import json
from obs import ObsClient, GetObjectHeader, PutObjectHeader
from flask import Flask, request

'''
1. function and bucket locate in same region
2. service's role has OSSFullAccess
3. event format
{
    "bucket_name" : "test-bucket",
    "object_key" : "a.mp4",
    "output_dir" : "output/",
    "vf_args" : "drawtext=fontfile=/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc:text='华为云函数工作流':x=100:y=50:fontsize=24:fontcolor=red:shadowy=2",
    "filter_complex_args": "overlay=0:0:1"
}

filter_complex_args 优先级 > vf_args

vf_args:
- 文字水印
vf_args = "drawtext=fontfile=/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc:text='华为云函数工作流':x=50:y=50:fontsize=24:fontcolor=red:shadowy=1"
- 图片水印, 静态图片
vf_args = "movie=/logo.png[watermark];[in][watermark]overlay=10:10[out]"

filter_complex_args: 图片水印, 动态图片gif
filter_complex_args = "overlay=0:0:1"
'''

app = Flask(__name__, static_folder='static', template_folder='templates')
app.logger.setLevel('INFO')

def splitObjectName(objectName):
    (fileDir, filename) = os.path.split(objectName)
    (shortname, extension) = os.path.splitext(filename)
    return fileDir, shortname, extension

@app.route('/init', methods=['POST'])
def init():
    data = {
        'result_code':200,
        'result_desc':"Success",
        'data':"handler for init"
    }
    return data

@app.route('/invoke', methods=['POST'])
def invoke():
    data = {
        'result_code':200,
        'result_desc':"Success",
        'data':"handler for invoke"
    }
    try:
        body = request.get_json()
        app.logger.info(body)
        obsBucketName = body['bucket_name']
        objectKey = body['object_key']
        output_dir = body["output_dir"]
        vf_args = body.get("vf_args", 0)
        filter_complex_args = body.get("filter_complex_args")
        if not (vf_args or filter_complex_args):
            raise Exception("at least one of 'vf_args' and 'filter_complex_args' has value")

        fileDir, shortname, extension = splitObjectName(objectKey)

        obsClient = ObsClient(
            access_key_id=request.headers.get('x-cff-access-key'),
            secret_access_key=request.headers.get('x-cff-secret-key'),
            server=os.getenv('ENDPOINT'),
        )
        savePath = '/tmp/{0}{1}'.format(shortname, extension)
        headers = GetObjectHeader()
        resp = obsClient.getObject(obsBucketName, objectKey, savePath, headers)
        if resp.status >= 300:
            app.logger.error(resp.body)
            raise Exception('get object failed')
        
        dst_video_path = os.path.join("/tmp", "watermark_" + shortname + extension)
        
        cmd = ["ffmpeg", "-y", "-i", savePath,
           "-vf", vf_args, dst_video_path]

        if filter_complex_args:  # gif
            cmd = ["ffmpeg", "-y", "-i", savePath, "-ignore_loop", "0",
                "-i", "/logo.gif", "-filter_complex", filter_complex_args, dst_video_path]
        
        app.logger.info(cmd)

        subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        os.remove(savePath)
        video_key = os.path.join(output_dir, fileDir, shortname + extension)
        resp = obsClient.putFile(obsBucketName, video_key, dst_video_path, headers=headers)
        # os.remove(dst_video_path)
        if resp.status >= 300:
            app.logger.error(resp.body)
            raise Exception('put object failed')
    except Exception as e:
        app.logger.error(e)
        data['result_code'] = 500
        data['result_desc'] = "Failed"
        data['data'] = str(e)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)