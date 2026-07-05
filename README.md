## 카카오톡 메일 알림 서비스
네이버 혹은 구글 메일을 통해 받은 메일을 사용자에게 카카오톡으로 알림을 보내는 서비스

## 구현 계획
1. 메일이 온다
2. 메일 --> 서버로 요청을 보낸다.
3. 서버에서 메일 제목을 파싱한다.
4. mail_agent/agent.py를 통해 agent를 호출한다.
5. 카카오톡으로 사용자에게 알림을 보낸다.

## 구현 진행도
- 최신 메일 응답 [O]
- 랭그래프 구현 [O]
- 스케줄러 [O]
- 카카오톡 API 연동 []
- 모델 변경 []

## 아키텍처

```
┌────────────┐     ┌───────────────────┐     ┌──────────────────────┐     ┌────────────────┐
│ APScheduler │ --> │ mail_fetcher.py   │ --> │ agent.py (LangGraph) │ --> │ 카카오톡 API     │
│ (main.py)   │     │ 네이버 IMAP 조회   │     │ 분류 -> 알림 전송      │     │ (미구현)         │
└────────────┘     └───────────────────┘     └──────────────────────┘     └────────────────┘
```

## 폴더 구조

```
mail-alert/
├── main.py                 # 진입점 및 스케줄러
├── requirement.txt         # 의존 패키지 목록
├── sent_log.json           # 처리된 메일 ID 로그 (자동 생성)
├── .env                     # 실제 환경 변수 (git 미포함)
├── .env.example             # 환경 변수 템플릿
├── .gitignore
├── README.md
└── mail_agent/
    ├── __init__.py          # 패키지 초기화 파일
    ├── agent.py             # LangGraph 기반 MailAgent
    ├── mail_fetcher.py      # 네이버 IMAP 메일 조회
    ├── state.py             # LangGraph 상태(mailState) 정의
    └── graph.png            # 그래프 구조 시각화 이미지
```

