from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from .state import mailState

load_dotenv()

class MailAgent:
    def __init__(self):
        self.llm = init_chat_model("gpt-5-nano", temperature=0.5)
        self.graph = self._build_graph()


    def _build_graph(self): # private: _로 시작하는 함수
        builder = StateGraph(mailState)
        
        builder.add_node('mail_classification', self._mail_classification)
        builder.add_node('kakaotalkSend', self._kakaotalkSend)

        builder.add_edge(START, 'mail_classification')
        builder.add_conditional_edges(
            'mail_classification',
            self._routing,
            [END, 'kakaotalkSend']
            )
        builder.add_edge('kakaotalkSend', END)

        return builder.compile()

    def _mail_classification(self, state: mailState): # private
        print("STEP 1: LLM이 메일을 분류 중입니다. 잠시만 기다려주세요...")

        prompt = f"""
        당신은 메일 제목을 분류하는 분류기입니다.
        메일 제목을 보고 클래스를 분류하세요.
        클래스는 다음과 같습니다: 'normal', 'abnormal'

        normal은 사용자가 확인해야하는 메일을 의미하고,
        abnormal은 스팸이나 광고와 같이 사용자가 확인할 필요 없는 메일입니다.
        
        ---
        메일 작성자: {state['mail_sender']}
        메일 제목:{state['mail_title']}
        응답 형식은 무조건 'normal' 혹은 'abnormal'로만 응답해주세요.
        응답 형식: normal or abnormal
        """

        response = self.llm.invoke(prompt)
        if (response.content == 'normal'):
            print("사용자가 읽어야 하는 메일 입니다.")
            return {"mail_class": 'normal'}
        
        if (response.content == 'abnormal'):
            print("사용자가 읽을 필요가 없는 메일 입니다.")
            return {"mail_class": 'abnormal'}
        
        print("메일 분류에 실패하였습니다.")
        return {"mail_class": 'error', "isSuccess": False}


    def _kakaotalkSend(self, state: mailState): # priavte
        print("STEP 2: 카카오톡으로 알림을 보내는 중입니다. 잠시만 기다려주세요...")
        """
        카카오톡 메시지 전송 노드
        """

        # kakao API 호출

        return {"isSuccess": True}

    def _routing(self, state: mailState): # private
        mail_class = state['mail_class']

        if mail_class == 'error' or 'abnormal':
            return END
        
        return 'kakaotalkSend'
    
    def run(self, mail_sender: str, mail_title: str):
        return self.graph.invoke({'mail_sender': mail_sender , 'mail_title':mail_title}) 