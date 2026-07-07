import threading
from langgraph.graph.state import RunnableConfig
from langchain.chat_models import init_chat_model
from src.classes.State import StateRpg
from langchain_core.messages import SystemMessage, HumanMessage
from src.classes.Personagem.SavageWorld import SavageWorld
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
class AgentService:
    def __init__(self):
        self.console = Console()
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
        self.mestre = init_chat_model("google_genai:gemini-2.5-flash")
        self.geradorPersonagem = init_chat_model("google_genai:gemini-2.5-flash")

    def gerarPersonagem(self, stateRpg : StateRpg):
        #stateRpg["messages_geradorPersonagem"] = [SystemMessage(content="Você é um gerador de personagem para um jogo de RPG. Crie um personagem com nome, classe, raça e habilidades. Retorne em formato JSON.")]
        #print(stateRpg["messages_geradorPersonagem"])     
        user_input = "n"
        while user_input == "n":
            personagem = self.geradorPersonagem.with_structured_output(SavageWorld).invoke(stateRpg["messages_geradorPersonagem"])
            print(personagem)
            print(type(personagem))
            user_input = input("Você gostou do personagem gerado? (s/n): ")
        startMessage = [HumanMessage(content=f"Você é um mestre de RPG. Crie uma história de RPG com o tema {stateRpg['tema_desejado']}. Desenvolva a história de forma criativa, buscando fazer plots siga na risca as Regras do SavageWorld, Lembre-se que você é o Mestre o jogador vai interagir com você através das mensagens, e você ira narrar a história e os eventos que vão acontecer. Me passe agora um contexto da historia que se passará a Aventura.")]
        return {"personagem": personagem, "messages": startMessage}
        
        
    
    def acaoJogador(self, stateRpg : StateRpg):

        if len(stateRpg["messages"]) == 1:
            input_text = HumanMessage(content=f"Segue o Personagem que será usado nessa aventura {stateRpg['personagem']}. Agora me passe sobre o contexto da aventura, do mundo e outras informações que achar necessário para a melhor experiencia do roleplay do jogador.")
            return {"messages": [input_text]}
        print("Hue não era p vc estar aqui")
        input_text = input("Digite sua ação: ")

        if input_text.lower() == "sair":
            print("Encerrando o jogo. Até mais!")
            return {"messages": ["sair"]}           #return {"messages": []}  # Retorna uma lista vazia de mensagens para indicar que o jogo terminou
        #llm_result = self.mestre.invoke(stateRpg["messages"])
        return {"messages": [input_text]}
    
    def chamarMestre(self, stateRpg : StateRpg):
        llm_result = self.mestre.invoke(stateRpg["messages"])
        objeto_markdown = Markdown(llm_result.text)
        self.console.print(objeto_markdown)
        #print(llm_result)
        return {"messages": [llm_result]}
