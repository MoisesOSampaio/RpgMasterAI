import psycopg2
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
import os
class UserRepository():

    
    
    def get_user_by_email_and_password(self,email : str, senha :str):
        # print(type(email), type(senha))
        # if not isinstance(email, str) or not isinstance(senha, str):
        #     print("Erro parametro inválido, na hora do login do usuário")
        #     return 
        try:
            load_dotenv()
            conn = psycopg2.connect(
            host=os.getenv("HOST_POSTGRES"),
            database=os.getenv("DATABASE_POSTGRES"),
            user=os.getenv("USER_POSTGRES"),
            password=os.getenv("PASSWORD_POSTGRES"),
            port=os.getenv("PORT_POSTGRES")
        )
            cursor = conn.cursor()
            ph = PasswordHasher()

            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            try:
                ph.verify(usuario[3], senha)
                print("Login realizado! Bem-vindo {usuario[1]}")
                return usuario
            except VerifyMismatchError:
                print("Usuário não encontrado")
                return None
            except TypeError:
                print("Usuário não encontrado")
                return None
        except psycopg2.Error as e:
            print("Erro ao cadastrar usuário:", e)
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def create_user(self, nome : str, email : str, senha : str) -> None:

        # if not isinstance(nome, str) or not isinstance(email, str) or not isinstance(senha, str):
        #     print("Erro parametro inválido, na hora do cadastro do usuário")
        #     return 

        load_dotenv()
        conn = psycopg2.connect(
            host=os.getenv("HOST_POSTGRES"),
            database=os.getenv("DATABASE_POSTGRES"),
            user=os.getenv("USER_POSTGRES"),
            password=os.getenv("PASSWORD_POSTGRES"),
            port=os.getenv("PORT_POSTGRES")
        )
        cursor = conn.cursor()

        try:
        
            ph = PasswordHasher()
            hash = ph.hash(senha)
            

            sql = """
        INSERT INTO usuarios(nome, email, senha)
        VALUES (%s, %s, %s)
        """

            cursor.execute(
            sql,
            (nome, email, hash)
            )

            conn.commit()

            print("Usuário cadastrado!")

        except psycopg2.Error as e:
            print("Erro ao cadastrar usuário:", e)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()
            