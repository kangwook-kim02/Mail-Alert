import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def send_kakao_message(subject: str, sender: str):
    access_token = os.getenv("KAKAO_ACCESS_TOKEN")
    
    text = f"네이버 메일이 도착했습니다!\n\n발신자: {sender}\n제목: {subject}\n\n 확인부탁드립니다."
    
    template = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "http://localhost"
        }
    }
    
    response = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "template_object": json.dumps(template, ensure_ascii=False)
        }
    )
    
    return response.status_code == 200
    