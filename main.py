from mail_agent.agent import MailAgent

agent = MailAgent()

# 그래프 이미지 저장
graph_image = agent.graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_image)