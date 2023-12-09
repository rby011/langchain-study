########################################################################################
# 4th generation chatbot
# - agent based execution 
# 
# [Agent] langchain's "Tool"
# - make a plan and execute the plan given objective
# - check execution results and enhance the plan
# - loop until satifying the objective
# 
# [Differnce with 3rd gen]
# - Copilot 이 Agent 기반 
# - Intent 에 따라 구성된 Pipe 는 Skill Set (Tool) 로 구성
#
# [Agent Type]
# - Conversational : 1~2 턴 이내에 빠르게 해결
# - Planning : 목표가 주어졌을 때 스킬셋 기반으로 해결 과정을 설게하고 하나씩 수행
# - Mutli Agent : 여러 Agent 의 집단 협력
#
# [특정]
# - LLM 답을 내기 위해 해결 방식 고민
# - 시나리오 방식에서 벗어날 수 있음. 너무 발산하지 않도록 최소한의 intent 분기는 필요
# - 실험 단계, GPT-4 비싸서 엄청 돈이 많이 나갈 수 있음
# - 디버깅 어려움 . langchain 의 경우 ★ Wandb 같은 Tracing 라이브러리 사용이 권장됨 ★ 
# ######################################################################################
import os

from dotenv import load_dotenv
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
# Agent
from langchain_experimental.plan_and_execute import (
    PlanAndExecute, 
    load_agent_executor,
    load_chat_planner,
)
from langchain.llms import OpenAI

load_dotenv()

# https://serpapi.com/manage-api-key
# pip install google-search-results or poetry add google-search-results
llm = OpenAI(temperature=0)
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
tools = [  # Agent 가 사용할 수 있느 도구들
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
]

model = ChatOpenAI(temperature=0)  # Agent 는 chatgpt 로 함
planner = load_chat_planner(model)
executor = load_agent_executor(model, tools, verbose=True)
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)
