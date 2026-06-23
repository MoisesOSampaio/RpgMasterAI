from typing import TypedDict
from src.classes.UserDTO import UserDTO
from src.classes.Personagem.Personagem import Personagem

class StateRpg(TypedDict):
    user: UserDTO
    personagem : Personagem
    opcao : int