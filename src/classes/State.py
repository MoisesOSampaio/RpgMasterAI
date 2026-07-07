from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import add_messages, StateGraph
from src.classes.UserDTO import UserDTO
from src.classes.Personagem.Personagem import Personagem

class StateRpg(TypedDict):
    user: UserDTO
    personagem : Personagem
    opcao : int
    tema_desejado : str
    messages : Annotated[Sequence[BaseMessage], add_messages]
    messages_geradorPersonagem : Annotated[Sequence[BaseMessage], add_messages]