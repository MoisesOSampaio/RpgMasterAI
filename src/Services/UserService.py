from src.Repository.UserRepository import UserRepository
from src.classes.State import StateRpg
from src.classes.UserDTO import UserDTO
class UserService:

    userRepository : UserRepository

    def __init__(self,userRepository):
        self.userRepository = userRepository()

    def exibir_menu(self,stateRpg : StateRpg):
        print("----- MENU -----")
        print("1. Criar Cadastro")
        print("2. Logar")
        if stateRpg["user"] is not None:
            print("3. Jogar")
        print("4. Sair")
        print("----------------")
        op = input("Escolha uma opção: ")
        op = int(op)
        print(type(op))
        print(f"Opção escolhida: {op}")
        return {"opcao": op}
    
    def end(self,stateRpg : StateRpg):
        print("Encerrando execução...")

    def login(self,stateRpg : StateRpg):
        email = stateRpg["user"].email
        senha = stateRpg["user"].senha
        if not isinstance(email, str) or not isinstance(senha, str):
            print("Erro parametro inválido, na hora do login do usuário")
            return None
        user = self.userRepository.get_user_by_email_and_password(email, senha)
        if user is None:
            return None
        user = UserDTO(
            id=user[0],
            name=user[1],
            email=user[2],
            senha=user[3]
        )
        return {"user" : user}

    def create_user(self, stateRpg : StateRpg) -> None:
        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        if not isinstance(nome, str) or not isinstance(email, str) or not isinstance(senha, str):
            print("Erro parametro inválido, na hora do cadastro do usuário")
            return None
        self.userRepository.create_user(nome, email, senha)
        return None
            