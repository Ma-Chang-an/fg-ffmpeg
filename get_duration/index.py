import subprocess
import os
from obs import ObsClient, GetObjectHeader, PutObjectHeader
from flask import Flask, request

'''
1. function and bucket locate in same region
2. service's role has OSSReadAccess
3. event format
{
    "bucket_name" : "test-bucket",
    "object_key" : "a.mp4"
}
'''

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
    return shortname, extension

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
        'result_desc':"Success"
    }
    try:
        body = request.get_json()
        app.logger.info(body)
        obsBucketName = body.get('bucket_name')
        objectKey = body.get('object_key')

        shortname, extension = splitObjectName(objectKey)

        savePath = '/tmp/{0}{1}'.format(shortname, extension)
        headers = GetObjectHeader()
        resp = ObsClient.getObject(obsBucketName, objectKey, savePath, headers)
        if resp.status >= 300:
            app.logger.error(resp.body)
            raise Exception('get object failed')
        
        cmd = ["ffprobe",  "-show_entries", "format=duration",
           "-v", "quiet", "-of", "csv", "-i",  savePath]
        
        app.logger.info(cmd)

        raw_result = subprocess.check_output(cmd)
        result = raw_result.decode().replace("\n", "").strip().split(",")[1]
        data['duration'] = float(result)
    except Exception as e:
        app.logger.error(e)
        data['result_code'] = 500
        data['result_desc'] = "Failed"
        data['err_msg'] = str(e)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)