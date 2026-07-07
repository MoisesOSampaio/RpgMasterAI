from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

from langgraph.checkpoint.memory import InMemorySaver
import threading

from src.Services.UserService import UserService
from src.classes.State import StateRpg
from src.Services.AgentService import AgentService


def roteador_do_menu(state: StateRpg) -> str:
    """
    Lê o campo 'opcao' do State e decide o próximo nó.
    """
    if state["opcao"] == 1:
        return "cadastrar_usuario"
    elif state["opcao"] == 2:
        return "logar_usuario"
    elif state["opcao"] == 3:
        if state["personagem"] is None:
            return "no_gerar_personagem"
        return "jogar"
    elif state["opcao"] == 4:
        return "ir_para_encerrar"
    else:
        print(state["opcao"])
        print("Opção inválida! Atualizando a ficha...")
        return "ir_para_exibir"
    
def roteador_criador_personagem(state: StateRpg) -> str:
    """
    Lê o campo 'opcao' do State e decide o próximo nó.
    """
    if state["personagem"] is None:
        return "no_gerar_personagem"
    return "no_jogar"

def loop_mestre(state: StateRpg) -> str:
    """
    Lê o campo 'opcao' do State e decide o próximo nó.
    """
    print(state["messages"][-1])
    if state["messages"][-1].content == "sair":
        return "no_menu"
    else:
        return "no_jogar"

class AgentController:
    
    userService : UserService
    agentService : AgentService
    
    def __init__(self, userService, userRepository, agentService):
        self.userService = userService(userRepository)
        self.agentService = agentService()
        
        
    def build_graph(self):
        checkpointer = InMemorySaver()
        

        graph = StateGraph(StateRpg)
        # Registra as funções como nós do Grafo
        graph.add_node("no_menu", self.userService.exibir_menu)
        graph.add_node("no_cadastrar_usuario", self.userService.create_user)
        graph.add_node("no_logar_usuario", self.userService.login)
        graph.add_node("no_encerrar", self.userService.end)
        graph.add_node("no_jogar", self.agentService.acaoJogador)
        graph.add_node("no_chamar_mestre", self.agentService.chamarMestre)
        graph.add_node("no_gerar_personagem", self.agentService.gerarPersonagem)
    # Configura o ponto inicial: Começa exibindo a ficha em branco/padrão
        graph.add_edge(START, "no_menu")

    # Conexões fixas: Após alterar o Nome ou Classe, volta a exibir a ficha atualizada
        graph.add_edge("no_cadastrar_usuario", "no_menu")
        graph.add_edge("no_logar_usuario", "no_menu")
        #graph.add_edge("no_jogar", "no_menu")
        graph.add_edge("no_encerrar", END)
        graph.add_edge("no_gerar_personagem", "no_jogar")
        #graph.add_edge("no_jogar", "no_chamar_mestre")
        graph.add_edge("no_chamar_mestre", "no_jogar")
# Conexão Condicional: Ao terminar o nó de exibição, o roteador escolhe o caminho
        graph.add_conditional_edges(
    "no_menu",
    roteador_do_menu,
    {
        "cadastrar_usuario": "no_cadastrar_usuario",
        "logar_usuario": "no_logar_usuario",
        "jogar": "no_jogar",
        "no_gerar_personagem": "no_gerar_personagem",
        "ir_para_exibir": "no_menu",
        "ir_para_encerrar": "no_encerrar"
    }
)
        # graph.add_conditional_edges(
        #     "no_jogar",
        #     roteador_criador_personagem,
        #     {
        #         "no_gerar_personagem": "no_gerar_personagem",
        #         "no_jogar": "no_jogar"
        #     }
        # )

        graph.add_conditional_edges(
            "no_jogar",
            loop_mestre,
            {
                "no_menu": "no_menu",
                "no_jogar": "no_chamar_mestre"
            }
        )
        app = graph.compile(checkpointer=checkpointer)
        return app