from sre_constants import FAILURE, SUCCESS
import urllib3
import json
import base64
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt 
import matplotlib as mpl
SUCCESS, FAILURE = 0, -1
RESPONSE_OK = 200

http = urllib3.PoolManager()

def detect_object(img_file, return_file):
    with open('etriaikey.txt') as f:
        ai_key = f.read()
    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"

    _, img_type = os.path.splitext(img_file)
    img_type = 'jpg' if img_type == '.jfif' else img_type[1:]
    with open(img_file, 'rb') as file:
        img_contents = base64.b64encode(file.read()).decode("utf8")
    
    request_json = {
        "access_key": ai_key,
        "argument": {
            "type": img_type,
            "file": img_contents
        }
    }
    
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(request_json)
    )
    if response.status != RESPONSE_OK:
        return FAILURE
    
    result = json.loads(response.data)
    try:
        obj_list = result['return_object']['data']
    except:
        return None
    image = Image.open(img_file)
    draw = ImageDraw.Draw(image)
    
    for obj in obj_list:
        name = obj['class']
        x = int(obj['x'])
        y = int(obj['y'])
        w = int(obj['width'])
        h = int(obj['height'])
        draw.text((x+10,y+10), name, font=ImageFont.truetype('malgun.ttf',20), fill=(255,0,0))
        draw.rectangle(((x,y), (x+w,y+h)), outline=(255,0,0), width=2)
    
#    if not return_file:
#        plt.figure(figsize=(12,8))
#        plt.imshow(image)
#        plt.show()
#    else:
#        img_name = os.path.basename(img_file)
#        if not os.path.exists('검출된객체'):
#            os.mkdir('검출된객체')
#        filename = f'검출된객체/{img_name}'
#        image.save(filename)
#        return filename

    img.save(return_file)
    return SUCCESS