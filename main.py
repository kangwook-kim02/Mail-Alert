from apscheduler.schedulers.blocking import BlockingScheduler
from mail_agent.mail_fetcher import fetch_naver_mails, save_sent_id
from mail_agent.agent import MailAgent

agent = MailAgent() # agent 연결

def job():
    mails = fetch_naver_mails()
    
    for mail in mails:
        print(f"제목: {mail['subject']}")
        print(f"발신자: {mail['sender']}")
        
        # 나중에 여기서 agent.run() 호출
        agent.run(mail['sender'], mail['subject'])
        
        save_sent_id(mail['mid'])

scheduler = BlockingScheduler()
scheduler.add_job(job, "interval", minutes=5)  # 5분마다 실행

print("스케줄러 시작!")
scheduler.start()