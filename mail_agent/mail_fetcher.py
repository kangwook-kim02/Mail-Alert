# mail_fetcher.py
import imaplib
import email
import json
import os
from email.header import decode_header
from datetime import date
from dotenv import load_dotenv

load_dotenv()

SENT_LOG = "sent_log.json"

def load_sent_ids():
    if not os.path.exists(SENT_LOG):
        return []
    with open(SENT_LOG, "r") as f:
        return json.load(f)

def save_sent_id(mid: str):
    sent = load_sent_ids()
    sent.append(mid)
    with open(SENT_LOG, "w") as f:
        json.dump(sent, f)

def fetch_naver_mails():
    imap = imaplib.IMAP4_SSL("imap.naver.com", 993)
    imap.login(os.getenv("NAVER_EMAIL"), os.getenv("NAVER_APP_PASSWORD"))
    imap.select("INBOX")

    # 오늘 온 메일만
    today = date.today().strftime("%d-%b-%Y")
    _, message_ids = imap.search(None, f'ON {today}')

    # 메일 없으면 종료
    if not message_ids[0]:
        imap.logout()
        return []

    # 가장 최근 1개만
    latest = message_ids[0].split()[-1:]
    sent_ids = load_sent_ids()

    mails = []
    for mid in latest:
        mid_str = mid.decode()

        # 이미 처리한 메일 스킵
        if mid_str in sent_ids:
            print(f"이미 처리한 메일: {mid_str}")
            continue

        _, msg_data = imap.fetch(mid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        sender, encoding = decode_header(msg["From"])[0]
        if isinstance(sender, bytes):
            sender = sender.decode(encoding or "utf-8")

        mails.append({
            "mid": mid_str,
            "subject": subject,
            "sender": sender
        })

    imap.logout()
    return mails