from typing import TypedDict

class mailState(TypedDict):
    """
    메일 제목을 담고, 메일 제목을 통해 분류를 하기 위한 State
    """
    mail_sender: str # 메일 보낸 사람
    mail_title: str # 메일 제목
    mail_class: str # 제목을 통한 메일 분류
    isSuccess: bool # 성공 여부