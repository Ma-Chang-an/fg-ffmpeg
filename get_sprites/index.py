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
        tile = body["tile"]
        ss = str(body.get("start", 0))
        t = body.get("duration")
        if t:
            t = str(t)

        itsoffset = str(body.get("itsoffset", 0))
        scale = body.get("scale", "-1:-1")
        interval = str(body.get("interval", 1))
        padding = str(body.get("padding", 0))
        color = str(body.get("color", "black"))
        dst_type = str(body.get("dst_type", "jpg"))

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
        
        cmd = ['ffmpeg', '-ss', ss, '-itsoffset', itsoffset, '-y', '-i', savePath,
           '-f', 'image2', '-vf', "fps=1/{0},scale={1},tile={2}:padding={3}:color={4}".format(
               interval, scale, tile, padding, color),
           '/tmp/{0}%d.{1}'.format(shortname, dst_type)]
        
        if t:
            cmd = ['ffmpeg', '-ss', ss, '-itsoffset', itsoffset, '-t', t, '-y', '-i', savePath,
                '-f', 'image2', '-vf', "fps=1/{0},scale={1},tile={2}:padding={3}:color={4}".format(
                    interval, scale, tile, padding, color),
                '/tmp/{0}%d.{1}'.format(shortname, dst_type)]
        
        app.logger.info(cmd)

        subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        os.remove(savePath)
        for filename in os.listdir('/tmp/'):
            filepath = '/tmp/' + filename
            if filename.startswith(shortname):
                headers = PutObjectHeader()
                headers.contentType = 'text/plain'
                objectKey = os.path.join(output_dir, fileDir, filename)
                resp = obsClient.putFile(obsBucketName, objectKey, filepath, headers=headers)
                os.remove(filepath)
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