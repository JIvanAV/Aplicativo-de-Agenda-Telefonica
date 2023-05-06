import pandas as pd #importar o pandas - biblioteca para o uso da planilha
import os, tkinter #importar os e Tkinter - biblioteca para procurar arquivos e criar a interface
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
if os.path.isfile('contatos.csv'): contatos = pd.read_csv('contatos.csv') #cria um framedata caso não exista o arquivo
else: contatos = pd.DataFrame(columns=['Nome', 'Telefone']) #caso exista o arquivo, utiliza ele
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def criar_contato():
    nome = input("Digite o nome do contato: ") #input do nome
    telefone = input("Digite o telefone do contato: ") #input do telefone
    novo_contato = pd.DataFrame({'Nome': [nome], 'Telefone': [telefone]}) #cadastrar no contatos.csv o contato
    global contatos #transformar contatos em global
    contatos = pd.concat([contatos, novo_contato], ignore_index=True) #concatenar o novo contato a lista antiga
    contatos.to_csv("contatos.csv", index=False) #salvar o arquivo
    print(f"Contato {nome} criado com sucesso.") #print de sucesso

    menu() #volta para o menu
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def ler_contatos():
    try: contatos = pd.read_csv('contatos.csv') #tentar ler o arquivo contatos.csv
    except FileNotFoundError: #caso dê erro
        print('Arquivo de contatos não encontrado.') #print de erro
        return #encerrar a função
    
    print(f"{'Nome':<20} {'Telefone':<15}") ; print('-' * 65) #print do contato
    contatos = contatos.fillna('') # preenche valores nulos com strings vazias
    contatos = contatos.applymap(lambda x: str(x).strip()) # remove espaços em branco no início e fim de cada valor
    
    for i, row in contatos.iterrows(): print(f"{row['Nome']:<20} {row['Telefone']:<15}") #percorre todo o arquivo contatos.csv e os printa
    print() #dá um espaço vazio

    menu() #volta para o menu
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def pesquisar_contato():
    remover_contatos_nan() #remove os contatos nan e organiza alfabeticamente

    termo_pesquisa = input('Digite o nome ou parte do nome do contato a pesquisar: ') #input para saber o nome
    resultados = contatos[contatos['Nome'].str.contains(termo_pesquisa, case=False)] #procura no arquivo contatos.csv o contato com nome aproximado
    if resultados.empty: print('Nenhum contato encontrado.') #printa que não achou caso não exista o nome parecido
    else: print(resultados.to_string(index=False).capitalize()) #printa o contato formatado (captalize)

    menu() #volta para o menu
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def deletar_contato():
    nome = input("Digite o nome do contato a ser deletado: ") #procura o nome exato
    indice = contatos.loc[contatos['Nome'] == nome].index[0] #pega o indice do contato
    contatos.drop(indice, inplace=True) #apaga o contato
    contatos.to_csv("contatos.csv", index=False) #salva
    print(f"Contato {nome} deletado com sucesso!") #printa que apagou

    menu() #volta para o menu
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def salvar_contatos():
    try: #tentar o seguinte:
        contatos.to_csv('contatos.csv', index=False) #salva os contatos em contato.csv
        print('Contatos salvos com sucesso!') #printa que salvou
    except Exception as e: print('Ocorreu um erro ao salvar os contatos:', e) #caso dê erro, printa o erro 
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def remover_contatos_nan(nome_arquivo="contatos.csv"):
    contatos = pd.read_csv(nome_arquivo) #pega o arquivo e transforma em pd
    for indice, contato in contatos.iterrows(): #percorre as linhas
        if pd.isna(contato['Nome']): #se o nome do contato for um NaN
            contatos.drop(indice, inplace=True) #apagar o contato
    contatos.to_csv(nome_arquivo, index=False) #salva o arquivo

    contatos = pd.read_csv(nome_arquivo) #lê novamente
    contatos_ordenados = contatos.sort_values(by='Nome') #organiza por ordem afabética
    contatos_ordenados.to_csv(nome_arquivo, index=False) #salva o arquivo

    salvar_contatos() #usa a função apra salvar a tabela
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def buscar_indice(contatos, nome):
    indice = contatos.index[contatos['Nome'] == nome].tolist() #pega o indice do nome
    if not indice: #se não encontrar o indice
        print(f"Contato {nome} não encontrado.") #printa que não encontrou o contato
        return None #encerra a função retornando valor vazio
    return indice[0] #encerra a função retornando o indice
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def menu():
    print("======================")
    print('1 - Criar novo contato')
    print('2 - Listar contatos')
    print('3 - Pesquisar contato')
    print('4 - Excluir contato')
    print('5 - Sair')
    print("======================")
    opcao = int(input('Escolha uma opção: '))
    if opcao == 1:
        criar_contato()
        salvar_contatos()
    elif opcao == 2:
        ler_contatos()
        salvar_contatos()
    elif opcao == 3:
        pesquisar_contato()
        salvar_contatos()
    elif opcao == 4:
        deletar_contato()
        salvar_contatos()
    elif opcao == 5:
        salvar_contatos()
        print('Programa encerrado.')
        return
    else:
        print('Opção inválida.')
        menu()
#menu()
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
''' ANOTAÇÕES DAS COISAS PARA FAZER:
criar hyperlink (incerto)
tirar todos os prints
criar uma interface de respeito
transformar em executável
'''
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
import tkinter as tk
import pandas as pd

class ContatoApp:
    def __init__(self, df):
        self.df = df
        self.idx = 0

        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("Contatos")

        # Criação dos widgets
        self.label_nome = tk.Label(self.root, text="Nome:")
        self.label_nome.grid(row=0, column=0, padx=5, pady=5)

        self.entry_nome = tk.Entry(self.root, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        self.label_telefone = tk.Label(self.root, text="Telefone:")
        self.label_telefone.grid(row=1, column=0, padx=5, pady=5)

        self.entry_telefone = tk.Entry(self.root, width=30)
        self.entry_telefone.grid(row=1, column=1, padx=5, pady=5)

        self.btn_novo = tk.Button(self.root, text="Novo", command=self.novo_contato)
        self.btn_novo.grid(row=0, column=2, padx=5, pady=5)

        self.btn_deletar = tk.Button(self.root, text="Deletar", command=self.deletar_contato)
        self.btn_deletar.grid(row=1, column=2, padx=5, pady=5)

        self.btn_anterior = tk.Button(self.root, text="Anterior", command=self.contato_anterior)
        self.btn_anterior.grid(row=2, column=0, padx=5, pady=5)

        self.btn_proximo = tk.Button(self.root, text="Próximo", command=self.proximo_contato)
        self.btn_proximo.grid(row=2, column=1, padx=5, pady=5)

        self.btn_buscar = tk.Button(self.root, text="Buscar", command=self.buscar_contato)
        self.btn_buscar.grid(row=2, column=2, padx=5, pady=5)

        self.label_info = tk.Label(self.root, text="Contato 0 de 0")
        self.label_info.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Exibição inicial do primeiro contato, se houver
        self.exibir_contato_atual()

        # Loop principal do Tkinter
        self.root.mainloop()

    def novo_contato(self):
        # Criação do novo contato a partir dos dados informados
        novo_contato = {
            "nome": self.entry_nome.get(),
            "telefone": self.entry_telefone.get()
        }

        # Adiciona o novo contato ao dataframe e exibe-o
        self.df = self.df.append(novo_contato, ignore_index=True)
        self.idx = len(self.df) - 1
        self.exibir_contato_atual()

    def deletar_contato(self):
        # Exclusão do contato atual e exibição do próximo contato
        self.df = self.df.drop(self.idx)
        if self.idx == len(self.df):
            self.idx -= 1
        self.exibir_contato_atual()

    def contato_anterior(self):
        # Exibição do contato anterior, se houver
        if self.idx > 0:
            self.idx -= 1
            self.exibir_contato_atual()

    def proximo_contato(self):
        # Exibição do próximo contato, se houver
        if self.idx < len(self.df) - 1:
            self.idx += 1
            self.exibir_contato_atual()

    def buscar_contato(self):
        # Busca pelo contato com o nome informado e exibição do resultado
        nome = self.entry_nome.get()
        if nome:
            resultado = self.df.loc[self.df["nome"] == nome]
            if not resultado.empty:
                self.idx = resultado.index[0]
                self.exibir_contato_atual()

    def exibir_contato_atual(self):
        # Exibição dos dados do contato atual e atualização do label de informações
        if len(self.df) > 0:
            contato_atual = self.df.iloc[self.idx]
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, contato_atual["nome"])
            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, contato_atual["telefone"])
            self.label_info.config(text=f"Contato {self.idx+1} de {len(self.df)}")
        else:
            self.entry_nome.delete(0, tk.END)
            self.entry_telefone.delete(0, tk.END)
            self.label_info.config(text="Nenhum contato encontrado")

df = pd.DataFrame(columns=["nome", "telefone"])
app = ContatoApp(df)