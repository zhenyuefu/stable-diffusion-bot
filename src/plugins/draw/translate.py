import json

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from src.plugins.draw.config import Config

api_info = Config()
k_access_key = api_info.k_access_key
k_secret_key = api_info.k_secret_key
k_timeout = 5  # second
k_service_info = ServiceInfo(
    "open.volcengineapi.com",
    {"Content-Type": "application/json"},
    Credentials(k_access_key, k_secret_key, "translate", "cn-north-1"),
    5,
    5,
)


def langDetect(text):
    k_query = {"Action": "LangDetect", "Version": "2020-06-01"}
    k_api_info = {"langdetect": ApiInfo("POST", "/", k_query, {}, {})}
    service = Service(k_service_info, k_api_info)
    body = {
        "TextList": [text],
    }
    res = json.loads(service.json("langdetect", {}, json.dumps(body)))
    return res["DetectedLanguageList"][0]["Language"]


def translate(text):
    k_query = {"Action": "TranslateText", "Version": "2020-06-01"}
    k_api_info = {"translate": ApiInfo("POST", "/", k_query, {}, {})}
    service = Service(k_service_info, k_api_info)
    body = {
        "TargetLanguage": "en",
        "TextList": [text],
    }
    res = json.loads(service.json("translate", {}, json.dumps(body)))
    return res["TranslationList"][0]["Translation"]
