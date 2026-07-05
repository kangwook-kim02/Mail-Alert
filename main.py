# main.py
from mail_agent.mail_fetcher import fetch_naver_mails

mails = fetch_naver_mails()
print(mails)