from pydantic import BaseModel
class Personagem(BaseModel):
    nome: str
    vida : int
    vida_max : int
    