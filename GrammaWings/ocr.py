from urllib import parse
import base64
import hashlib
import time
import requests
from api_config import OCR_API, OCR_ID

# OCR手写文字识别接口地址
URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"
APPID = OCR_ID  # 应用ID
API_KEY = OCR_API  # API密钥

def getHeader(language="en", location="true"):
    """
    生成 OCR 请求所需的 HTTP 头信息
    :param language: 识别语言（默认 "en"）
    :param location: 是否返回文本位置信息（默认 "true"）
    :return: 请求头字典
    """
    curTime = str(int(time.time()))  # 获取当前时间戳
    param = f'{{"language":"{language}","location":"{location}"}}'
    paramBase64 = base64.b64encode(param.encode('utf-8')).decode('utf-8')

    # 计算校验和
    md5 = hashlib.md5()
    md5.update((API_KEY + curTime + paramBase64).encode('utf-8'))
    checkSum = md5.hexdigest()

    return {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }

def getBody(filepath):
    """
    读取图片并转换为 base64
    :param filepath: 图片路径
    :return: 包含 base64 图片数据的字典
    """
    with open(filepath, 'rb') as f:
        imgfile = f.read()
    return {'image': base64.b64encode(imgfile).decode('utf-8')}

def extract_text_from_response(response_json):
    """
    提取 OCR 返回结果中的文本
    :param response_json: OCR 返回的 JSON 数据
    :return: 组合后的文本字符串
    """
    text_blocks = response_json.get("data", {}).get("block", [])
    full_text = []

    for block in text_blocks:
        lines = block.get("line", [])
        for line in lines:
            words = line.get("word", [])
            line_text = " ".join(word["content"] for word in words)
            full_text.append(line_text)

    return "\n".join(full_text)

# 设置语种和是否返回文本位置信息
language = "en"
location = "true"
picFilePath = r"D:\desk\GrammaWings\GrammaWings\ocr.jpg"  # 确保路径格式正确

# 发送请求
response = requests.post(URL, headers=getHeader(language, location), data=getBody(picFilePath))
print(response.text)
response_json = response.json()
# 输出结果
extracted_text = extract_text_from_response(response_json)

if __name__ == "__main__":
    print(extracted_text)
