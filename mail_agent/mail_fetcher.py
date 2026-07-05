# mail_fetcher.py
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

def fetch_naver_mails():
    imap = imaplib.IMAP4_SSL("imap.naver.com", 993)
    imap.login(os.getenv("NAVER_EMAIL"), os.getenv("NAVER_APP_PASSWORD"))
    imap.select("INBOX")



    today = date.today().strftime("%d-%b-%Y")  # 예: 05-Jul-2026
    _, message_ids = imap.search(None, f'ON {today}')

    mails = []
    for mid in message_ids[0].split():
        _, msg_data = imap.fetch(mid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # 제목 디코딩
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        # 발신자 디코딩
        sender, encoding = decode_header(msg["From"])[0]
        if isinstance(sender, bytes):
            sender = sender.decode(encoding or "utf-8")

        mails.append({
            "subject": subject,
            "sender": sender
        })

    imap.logout()
    return mails