import subprocess
import os
from obs import ObsClient, GetObjectHeader, PutObjectHeader
from flask import Flask, request

app = Flask(__name__, static_folder='static', template_folder='templates')
app.logger.setLevel('INFO')

ObsClient = ObsClient(
    access_key_id=os.getenv("AccessKeyID"),
    secret_access_key=os.getenv("SecretAccessKey"),
    server=os.getenv('ENDPOINT'),
)

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
        obsBucketName = body.get('bucket_name')
        objectKey = body.get('object_key')
        outputDir = body.get('output_dir')
        dstType = body.get('dst_type')
        ac = body.get('ac')
        ar = body.get('ar')

        fileDir, shortname, extension = splitObjectName(objectKey)

        headers = GetObjectHeader()
        resp = ObsClient.getObject(obsBucketName, objectKey, '/tmp/{0}{1}'.format(shortname, extension), headers)
        if resp.status >= 300:
            app.logger.error(resp.body)
            raise Exception('get object failed')
        
        inputPath = '/tmp/{0}{1}'.format(shortname, extension)
        cmd = ['ffmpeg', '-i', inputPath,
           '/tmp/{0}{1}'.format(shortname, dstType)]
        if ac:
            if ar:
                cmd = ['ffmpeg', '-i', inputPath, "-ac",
                    str(ac), "-ar", str(ar),  '/tmp/{0}{1}'.format(shortname, dstType)]
            else:
                cmd = ['ffmpeg', '-i', inputPath, "-ac",
                    str(ac), '/tmp/{0}{1}'.format(shortname, dstType)]
        else:
            if ar:
                cmd = ['ffmpeg', '-i', inputPath, "-ar",
                    str(ar),  '/tmp/{0}{1}'.format(shortname, dstType)]
        
        app.logger.info(cmd)

        subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        os.remove(inputPath)
        for filename in os.listdir('/tmp/'):
            filepath = '/tmp/' + filename
            if filename.startswith(shortname) and filename.endswith(dstType):
                headers = PutObjectHeader()
                headers.contentType = 'text/plain'
                objectKey = os.path.join(outputDir, fileDir, filename)
                resp = ObsClient.putFile(obsBucketName, objectKey, filepath, headers=headers)
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