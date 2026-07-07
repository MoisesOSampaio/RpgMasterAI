import threading
from langgraph.graph.state import RunnableConfig
from src.Controllers.AgentController import AgentController
from src.Services.UserService import UserService
from src.Repository.UserRepository import UserRepository
from src.Services.AgentService import AgentService
from langchain_core.messages import SystemMessage, HumanMessage 


controller = AgentController(UserService, UserRepository, AgentService)
graph = controller.build_graph()

estado_inicial = {
    "user": None,
    "personagem" : None,
    "opcao" : 0,
    "tema_desejado" : "medieval",
    "messages_geradorPersonagem" : [HumanMessage(content="Você é um gerador de personagem para um jogo de RPG Savage Worlds. Crie um personagem com nome, vida, dados de agilidade, dados de astucia, dados de espírito, dados de força e vigor. Considere que o os dados é considerado o tipo de dado que ele vai rodar para cada pericia, exemplo agilidade 4 seria 1d4, a vida deve ser calculada automaticamente conforme a regra do jogo SavageWorld, Siga elas a Risca na criação do Personagem")],
}
config = RunnableConfig(configurable={"thread_id": threading.get_ident()})
graph.invoke(estado_inicial,config=config)    


#print(graph.get_graph().draw_mermaid())
