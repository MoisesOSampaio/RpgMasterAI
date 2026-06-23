from src.classes.State import StateRpg
class GraphService:

    def exibir_menu(stateRpg : StateRpg):
        print("----- MENU -----")
        print("1. Criar Cadastro")
        print("2. Logar")
        if stateRpg["user"] is not None:
            print("3. Jogar")
        print("4. Sair")
        print("----------------")
        op = input("Escolha uma opção: ")
        return {"opcao": op}
    
    