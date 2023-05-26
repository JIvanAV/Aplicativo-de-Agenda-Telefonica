import pandas as pd                                                                                         #importar o pandas - biblioteca para o uso da planilha
import os                                                                                                   #importar os - biblioteca para procurar arquivos
from tkinter import *                                                                                       #Tkinter - biblioteca para criar a interface
import tkinter as tk                                                                                        #Tkinter - biblioteca para criar a interface
CAMINHOARQUIVO = 'contatos.csv'                                                                             #Caminho do arquivo (nome)
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
if os.path.isfile(CAMINHOARQUIVO): contatos = pd.read_csv(CAMINHOARQUIVO)                                   #cria um framedata caso não exista o arquivo
else: df = pd.DataFrame(columns=['Nome', 'Telefone'])                                                       #caso exista o arquivo, utiliza ele
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def criar_contato(df,nome,telefone):
    novo_contato = pd.DataFrame({'Nome': [nome], 'Telefone': [telefone]})                                   #cadastrar no contatos.csv o contato
    df = pd.concat([df, novo_contato], ignore_index=True)                                                   #concatenar o novo contato a lista antiga
    salvar_contatos(df)                                                                                     #salvar o arquivo
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def ler_contatos(df):
    try: pd.read_csv(CAMINHOARQUIVO)                                                                        #tentar ler o arquivo contatos.csv
    except FileNotFoundError:                                                                               #caso dê erro
        resultado = "Arquivo de contatos não encontrado."                                                   #aviso de erro
        return resultado                                                                                    #retorna o resultado com mensagem de erro          #remove os contatos nan e organiza alfabeticamente

    resultado = ""                                                                                          #str que irá receber os contatos
    i = 0                                                                                                   #contador
    for row in df.itertuples(index=False, name=None):
        nome = row[0]                                                                                       #lista para receber os nomes
        telefone = row[1]                                                                                   #lista para receber os telefone

        if len(str(telefone)) == 8:
            telefone = telefone[:4] + "-" + telefone[4:]                                                    #deixar números xxxxxxxx em xxxx-xxxx

        elif len(str(telefone)) == 9:
            telefone = telefone[0] + "." + telefone[1:5] + "-" + telefone[5:]                               #deixar números xxxxxxxxx em x.xxxx-xxxx

        elif len(str(telefone)) == 11:
            telefone = "(" + telefone[0:2] + ")" + telefone[3] + "." + telefone[3:7] + "-" + telefone[7:]   #deixar números xxxxxxxxxxx em (xx)x.xxxx-xxxx

        elif len(str(telefone)) == 12:
            telefone = "(" + telefone[0:3] + ")" + telefone[4] + "." + telefone[4:8] + "-" + telefone[8:]   #deixar números xxxxxxxxxxxx em (xxx)x.xxxx-xxxx

        telefone = f"===> {telefone} | ID: {i}"                                                             #colocar uma seta e o ID
        i+= 1                                                                                               #adicionar 1 ao contador

        resultado += f"{nome}\n{telefone} \n\n"                                                             #adicionar ao resultado

    return f"{resultado}"                                                                                   #retornar o resultado
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def pesquisar_contato(df,termo_pesquisa):
    resultados = df.loc[df['Nome'].str.contains(termo_pesquisa, case=False)]                                #procura no arquivo contatos.csv o contato com nome aproximado

    if resultados.empty: resultado = "Nenhum contato encontrado"                                            #resultado n existe
    else:
        resultadoLista = resultados.values.tolist()                                                         #resultado completo

        i = 0                                                                                               #contador
        resultado = ""                                                                                      #variavel string vazia

        for i in range(1,len(resultadoLista)):
            nome = resultadoLista[i][0]                                                                     #lista para receber os nomes
            telefone = resultadoLista[i][1]                                                                 #lista para receber os telefone

            if len(str(telefone)) == 8:
                telefone = telefone[:4] + "-" + telefone[4:]                                                #deixar números xxxxxxxx em xxxx-xxxx

            elif len(str(telefone)) == 9: 
                telefone = telefone[0] + "." + telefone[1:5] + "-" + telefone[5:]                           #deixar números xxxxxxxxx em x.xxxx-xxxx

            elif len(str(telefone)) == 11:
                telefone = "("+telefone[0:2] +")" + telefone[3] + "." + telefone[3:7] + "-" + telefone[7:]  #deixar números xxxxxxxxxxx em (xx)x.xxxx-xxxx

            elif len(str(telefone)) == 12:
                telefone = "("+telefone[0:3] +")" + telefone[4] + "." + telefone[4:8] + "-" + telefone[8:]  #deixar números xxxxxxxxxxxx em (xxx)x.xxxx-xxxx

            telefone = f"===> {telefone}"                                                                   #colocar uma seta e o ID
            i+= 1                                                                                           #adicionar 1 ao contador
            resultado += f"{nome}\n{telefone} \n\n"                                                         #adicionar ao resultado

    return f"{resultado}"                                                                                   #retornar o resultado
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def deletar_contato(nome):
    indice = contatos.loc[contatos['Nome'] == nome].index[0]                                                #pega o indice do contato
    contatos.drop(indice, inplace=True)                                                                     #apaga o contato
    salvar_contatos(contatos)                                                                               #salva
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def consultarID(df,nome):
    linhas = df.loc[df['Nome'] == nome].index                                                               #pega todos os nomes

    if len(linhas) > 0:                                                                                     #se a quantidade de linhas for maior que zero
        linha = linhas[0]                                                                                   #pega o id
        txt = f"ID: {linha}"                                                                                #insere o ID no texto
    else:
        txt = ""                                                                                            #texto vazio
    return txt                                                                                              #retorna o texto
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def salvar_contatos(df):
    df.to_csv(CAMINHOARQUIVO, index=False)                                                                  #salva os contatos em contato.csv
    return                                                                                                  #retorna aviso
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def buscar_indice(contatos, nome):
    indice = contatos.Index[contatos['Nome'] == nome].tolist()                                              #pega o indice do nome
    if not indice:                                                                                          #se não encontrar o indice
        aviso = (f"Contato {nome} não encontrado.")                                                         #printa que não encontrou o contato
        return aviso                                                                                        #encerra a função retornando valor vazio
    return indice[0]                                                                                        #encerra a função retornando o indice
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
def att_contato(df,id,nome,tel):
    id = int (id)                                                                                           #transformar id em inteiro

    if nome == "":nome = df.loc[id, 'Nome']                                                                 #se o nome estiver vazio, pegue o antigo
    elif tel == "":tel = df.loc[id, 'Telefone']                                                             #se o telefone estiver vazio, pegue o antigo

    elif nome == "" and tel == "": return                                                                   #se ambos estiverem vazios, retorne

    if id in df.index:                                                                                      #se o id estiver na planilha
        df.loc[id] = [nome,tel]                                                                             #substitui o nome e telefone

    salvar_contatos(df)                                                                                     #salvar os contatos

    return ler_contatos(df)                                                                                 #retornar leitura dos contatos
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
class TextoScrollbar(tk.Frame):
    def focus_entry(self,event):
        event.widget.focus_set()                                                                            #funcionalidade para focar no input que ser clicado
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
    def button_clicked_new(self):
        nome =self.barnewName.get()                                                                         #pegar o resultado da barra de nome
        telefone = self.barnewTel.get()                                                                     #pegar o resultado da barra de telefone

        if nome == "" or telefone == "":                                                                    #se um dos dois estiver vazio
            pass                                                                                            #não faça nada

        else:
            criar_contato(self.df,nome,telefone)                                                            #crie o contato
            self.text.delete('1.0', tk.END)                                                                 #apagar o conteudo antigo
            self.text.insert("1.0",ler_contatos(self.df))                                                   #atualiza a tela para mostrar o novo contato criado
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=# 
    def button_clicked_save(self):
        salvar_contatos(self.df)                                                                            #salvar os contatos
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
    def button_clicked_search(self):
        if self.barSearch.get() == "":                                                                      #se a entrada for vazia
            self.text.delete('1.0', tk.END)                                                                 #apagar o texto anterior
            self.text.insert("1.0",ler_contatos(self.df))                                                   #voltar ao inicial

        else:                                                                                               #se tiver digitado algo
            self.text.delete('1.0', tk.END)                                                                 #apagar o texto anterior
            self.text.insert("1.0",pesquisar_contato(self.df,self.barSearch.get()))                         #usar a função pesquisar com o conteúdo digitado
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
    def button_clicked_delete(self):
        nome = self.deleteSearch.get()                                                                      #pegar o nome colocado na barra
        deletar_contato(nome)                                                                               #deleta o contato

        self.text.delete('1.0', tk.END)                                                                     #apagar o texto anterior
        self.text.insert("1.0",ler_contatos(self.df))                                                       #voltar ao inicial
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
    def button_clicked_send_att(self):
        id = self.barAttID.get()                                                                            #pergar o id (linha)
        if not id.isnumeric(): return                                                                       #se id não for numérico, retornar

        novoNome = self.barAttNomeNovo.get()                                                                #pegar novo nome
        novoTel = self.barAttTelNovo.get()                                                                  #pegar novo telefone

        self.text.delete('1.0', tk.END)                                                                     #apagar o conteudo antigo
        self.text.insert("1.0",att_contato(self.df,id,novoNome,novoTel))                                    #atualiza a tela para mostrar o novo contato criado
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
    def button_clicked_att(self):
        id = self.barAttID.get()                                                                            #pergar o id (linha)
        if not id.isnumeric(): return                                                                       #se id não for numérico, retornar
        
        else:
            id = int(id)                                                                                    #transformar id em int

            if id < 0 or id > self.df.shape[0] - 1: return                                                  #se id for um número negativo ou superior ao número de linhas do arquivo, retornar

            else:                                                                                           #tudo ok, executar os comandos abaixo
                linha = self.df.iloc[id]                                                                    #pegar o valor da linha (id)
                nome = linha['Nome']                                                                        #pegar o nome
                telefone = linha['Telefone']                                                                #pegar o telefone
                
                self.labelNomeAntigo.config(text=f"Nome Antigo: {nome}")                                    #cria o texto do nome novo
                self.labelTeleAntigo.config(text=f"Telefo. Antigo: {telefone}")                             #cria o texto do telefone novo
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
    def button_clicked_ID(self):
        nome = self.barlocateID.get()                                                                       #pega o nome colocado na barra
        id = consultarID(self.df,nome)                                                                      #consulta o ID

        if id != "":                                                                                        #se o id não for vazio 
            self.labelID = tk.Label(text=id)                                                                #cria o texto do ID
            self.labelID.place(relx="0.34",rely="0.65")                                                     #coloca o texto do ID na tela

        return id
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
    def __init__(self, master=None):
        self.df = pd.read_csv(CAMINHOARQUIVO, usecols=['Nome', 'Telefone'])                                 #le o arquivo

        super().__init__(master)                                                                            #iniciar método construtor
        self.master = master                                                                                #cria o tk
        self.master.title("Agenda")                                                                         #nome da janela
        self.master.geometry("750x750")                                                                     #tamanho da janela
        self.master.config(bg="lightgrey")                                                                  #cor da janela
        self.pack()                                                                                         #inicia o tk
        
        self.text_frame = tk.Frame(self)                                                                    #Cria um frame para o texto
        self.text_frame.pack(fill="both", expand=True)                                                      #preenche a tela com o espaço para texto

        self.scrollbar = tk.Scrollbar(self.text_frame)                                                      #cria um scrollbar para navegar pelo texto
        self.scrollbar.pack(side="right", fill="y")                                                         #define a posição do scrollbar
        
        self.text = tk.Text(self.text_frame, yscrollcommand=self.scrollbar.set)                             #cria um widget de texto para exibir os contatos
        self.text.pack(fill="both", expand=True)                                                            #preenche a tela com os contatos

        self.scrollbar.config(command=self.text.yview)                                                      #conecta o scrollbar ao widget de texto

        self.save = Button(master,text= "Salvar")                                                           #criar botão de salvar
        self.save.place(relx="0.06",rely="0.55")                                                            #colocar o botão de salvar                           <=== (0.06,0.55) 
        self.save.config(command=self.button_clicked_save)                                                  #chamar funcionalidade de botão (save)

        self.buttomSearch = Button(master,text= "Pesquisar")                                                #criar botão de pesquisar
        self.buttomSearch.place(relx="0.06",rely="0.6")                                                     #colocar o botão de pesquisar                        <=== (0.06,0.6)
        self.barSearch = Entry(master,text="Pesquisar")                                                     #criar barra de pesquisar
        self.barSearch.place(relx="0.15",rely="0.604")                                                      #colocar barra de pesquisar                          <=== (0.15,0.604)
        self.buttomSearch.config(command=self.button_clicked_search)                                        #chamar funcionalidade de botão (search)

        self.new = Button(master,text= "Novo Contato")                                                      #criar botão de novo
        self.new.place(relx="0.06",rely="0.75")                                                             #colocar o botão de novo                             <=== (0.6,0.75)
        self.barnewName = Entry(master,text="Name")                                                         #criar barra de nome
        self.barnewName.place(relx="0.185",rely="0.755")                                                    #colocar barra de nome                               <=== (0.185,0.755)
        self.barnewTel = Entry(master,text="Telefone")                                                      #criar barra de telefone
        self.barnewTel.place(relx="0.185",rely="0.79")                                                      #colocar barra de telefone                           <=== (0.185,0.79)
        self.new.config(command=self.button_clicked_new)                                                    #chamar funcionalidade de botão (new)

        self.locateID = Button(master,text= "Consultar ID")                                                 #criar botão de ID
        self.locateID.place(relx="0.06",rely="0.65")                                                        #colocar o botão de localizar ID                     <=== (0.06,0.65)
        self.barlocateID = Entry(master,text="locateID")                                                    #criar barra de nome
        self.barlocateID.place(relx="0.17",rely="0.655")                                                    #colocar barra de nome                               <=== (0.17,0.655)
        self.locateID.config(command=self.button_clicked_ID)                                                #chamar funcionalidade de botão (ID)

        self.delete = Button(master,text= "Excluir Contato")                                                #criar botão de deletar
        self.delete.place(relx="0.12",rely="0.55")                                                          #colocar o botão de deletar                          <=== (0.12,0.55)
        self.deleteSearch = Entry(master,text="Delete")                                                     #criar barra de detelar
        self.deleteSearch.place(relx="0.25",rely="0.555",width=50)                                          #colocar barra de deletar                            <=== (0.25,0.55)
        self.delete.config(command=self.button_clicked_delete)                                              #chamar funcionalidade de botão (delete)

        self.att = Button(master,text= "Atualizar Contato")                                                 #criar botão de atualizar
        self.att.place(relx="0.5",rely="0.552")                                                             #colocar o botão de pesquisar                        <=== (0.5,0.552)
        self.barAttID = Entry(master,text="Atualizar")                                                      #criar barra de atualizar(id)
        self.barAttID.place(relx="0.645",rely="0.555")                                                      #colocar barra de atualizar(id)                      <=== (0.66,0.555)
        self.att.config(command=self.button_clicked_att)                                                    #chamar funcionalidade de botão (att)
        self.labelID = tk.Label(text="(Inserir ID)")                                                        #cria o texto de pedir ID
        self.labelID.place(relx="0.82",rely="0.555")                                                        #coloca o texto do ID na tela

        self.labelNomeNovo = tk.Label(text=f"Nome Novo:")                                                   #cria o texto do nome antigo
        self.labelNomeNovo.place(relx="0.5",rely="0.67")                                                    #coloca o texto do nome antigo na tela
        self.labelTeleNovo = tk.Label(text=f"Telefo. Novo:")                                                #cria o texto do nome antigo
        self.labelTeleNovo.place(relx="0.5",rely="0.7")                                                     #coloca o texto do nome antigo na tela
        self.labelNomeAntigo = tk.Label(text=f"Nome Antigo: ___")                                           #cria o texto do nome antigo
        self.labelNomeAntigo.place(relx="0.5",rely="0.59")                                                  #coloca o texto do nome antigo na tela
        self.labelTeleAntigo = tk.Label(text=f"Telefo. Antigo: ___")                                        #cria o texto do nome antigo
        self.labelTeleAntigo.place(relx="0.5",rely="0.62")                                                  #coloca o texto do nome antigo na tela
        self.barAttNomeNovo = Entry(text="Bara Att Nome Novo")                                              #criar barra de atualizar nome novo(id)
        self.barAttNomeNovo.place(relx="0.61",rely="0.67")                                                  #colocar barra de atualizar nome novo(id) 
        self.barAttTelNovo = Entry(text="Bara Att TelNovo")                                                 #criar barra de atualizar telefone novo(id)
        self.barAttTelNovo.place(relx="0.61",rely="0.7")                                                    #colocar barra de atualizar telefone novo(id) 
        self.sendAtt = Button(text= "Enviar")                                                               #criar botão de enviar
        self.sendAtt.place(relx="0.5",rely="0.74")                                                          #colocar o botão de enviar  
        self.sendAtt.config(command=self.button_clicked_send_att)                                           #caso botão de enviar seja clicado

        self.text.insert("1.0",ler_contatos(self.df))                                                       #define o texto a ser exibido com base na função ler_contatos

        self.text.configure()                                                                               #atualiza a tela - OBS: state="disabled" desabilita a edição
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
root = Tk()                                                                                                 #cria uma variável para instaciar a classe TK()
TextoScrollbar(root)                                                                                        #passar a variável como parâmetro do método construtor da classse
root.mainloop()                                                                                             #exibe na tela
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
