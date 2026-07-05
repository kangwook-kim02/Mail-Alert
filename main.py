from mail_agent.mail_fetcher import fetch_naver_mails, save_sent_id

mails = fetch_naver_mails()

for mail in mails:
    print(f"제목: {mail['subject']}")
    print(f"발신자: {mail['sender']}")
    
    # 나중에 여기서 agent.run() 호출
    
    save_sent_id(mail['mid'])  # 처리 완료 기록