from typing import TypedDict

class mailState(TypedDict):
    """
    메일 제목을 담고, 메일 제목을 통해 분류를 하기 위한 State
    """
    mail_title: str # 메일 제목
    mail_class: str # 제목을 통한 메일 분류
    isSuccess: bool 