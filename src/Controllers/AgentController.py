from langgraph.graph import StateGraph, START, END

from src.Services.UserService import UserService
from src.classes.State import StateRpg

def roteador_do_menu(state: StateRpg) -> str:
    """
    Lê o campo 'opcao' do State e decide o próximo nó.
    """
    if state["opcao"] == 1:
        return "cadastrar_usuario"
    elif state["opcao"] == 2:
        return "logar_usuario"
    elif state["opcao"] == 4:
        return "ir_para_encerrar"
    else:
        print(state["opcao"])
        print("Opção inválida! Atualizando a ficha...")
        return "ir_para_exibir"
    
    
class AgentController:
    
    userService : UserService

    def __init__(self, userService, userRepository):
        self.userService = userService(userRepository)
        
    def build_graph(self):
        graph = StateGraph(StateRpg)
        # Registra as funções como nós do Grafo
        graph.add_node("no_menu", self.userService.exibir_menu)
        graph.add_node("no_cadastrar_usuario", self.userService.create_user)
        graph.add_node("no_logar_usuario", self.userService.login)
        graph.add_node("no_encerrar", self.userService.end)
      
    # Configura o ponto inicial: Começa exibindo a ficha em branco/padrão
        graph.add_edge(START, "no_menu")

    # Conexões fixas: Após alterar o Nome ou Classe, volta a exibir a ficha atualizada
        graph.add_edge("no_cadastrar_usuario", "no_menu")
        graph.add_edge("no_logar_usuario", "no_menu")
        graph.add_edge("no_encerrar", END)
# Conexão Condicional: Ao terminar o nó de exibição, o roteador escolhe o caminho
        graph.add_conditional_edges(
    "no_menu",
    roteador_do_menu,
    {
        "cadastrar_usuario": "no_cadastrar_usuario",
        "logar_usuario": "no_logar_usuario",
        "ir_para_exibir": "no_menu",
        "encerrar": "no_encerrar"
    }
)
        app = graph.compile()
        return app