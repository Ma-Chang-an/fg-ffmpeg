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
    "vframes" : 20,
    "start": 0,
    "duration": 2
}
start 可选， 默认是为 0
vframes  和 duration 可选， 当同时填写的时候， 以 duration 为准
当都没有填写的时候， 默认整个视频转为gif
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
        ss = str(body.get("start", 0))
        vframes = body.get("vframes")
        if vframes:
            vframes = str(vframes)

        t = body.get("duration")
        if t:
            t = str(t)

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
        
        gif_path = os.path.join("/tmp", shortname + ".gif")
        
        cmd = ["ffmpeg", "-y",  "-ss", ss, "-accurate_seek",
           "-i", savePath, "-pix_fmt", "rgb24", gif_path]
        if t:
            cmd = ["ffmpeg", "-y", "-ss", ss, "-t", t,  "-accurate_seek",
                "-i", savePath, "-pix_fmt", "rgb24", gif_path]
        else:
            if vframes:
                cmd = ["ffmpeg", "-y",  "-ss", ss,  "-accurate_seek", "-i",
                    savePath, "-vframes", vframes, "-y", "-f", "gif", gif_path]
        
        app.logger.info(cmd)

        subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        os.remove(savePath)
        gif_key = os.path.join(output_dir, fileDir, shortname + ".gif")
        resp = obsClient.putFile(obsBucketName, gif_key, gif_path, headers=headers)
        os.remove(gif_path)
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