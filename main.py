from ast import While
from src.Repository.UserRepository import UserRepository
from src.model.mestreAgent import init_chatbot

def exibir_menu(logado):
    print("----- MENU -----")
    print("1. Criar Cadastro")
    print("2. Logar")
    if logado:
        print("3. Jogar")
    print("4. Sair")
    print("----------------")

def jogar(chat ):
    print("Bem-vindo ao jogo! Digite 'sair' a qualquer momento para encerrar.")
    while True:
    
        player_input = input("")

        if player_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o jogo. Até mais!")
            break
        response = chat.send_message(str(player_input))
        print(response.text)

def main():
    logado = False
    while True:
        exibir_menu(logado)
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            UserRepository.create_user(
                nome=input("Digite seu nome: "),
                email=input("Digite seu email: "),
                senha=input("Digite sua senha: ")
            )
        elif opcao == '2':
            user = UserRepository.get_user_by_email_and_password(
                email=str(input("Digite seu email: ")),
                senha=str(input("Digite sua senha: "))
            )
            print(user)
            if user:
                logado = True
        elif opcao == '3':
            client,chat = init_chatbot()
            jogar(chat)
        elif opcao == '4':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
        print("\n") 

if __name__ == "__main__":
    main()
