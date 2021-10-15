from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics
import mysql.connector
def abrebanco():
    try:
        global conexao
        global comandosql

        conexao = mysql.connector.Connect(host='localhost', database='univap', user='root', password='')
        if conexao.is_connected():
            informacaobanco = conexao.get_server_info()
            print(f'Conectado ao servidor banco de dados - Versão {informacaobanco}')
            print('Conexão ok')

            comandosql = conexao.cursor()
            comandosql.execute('select database();')
            nomebanco = comandosql.fetchone()
            print(f'Banco de dados acessado = {nomebanco[0]}')
            print('=' * 80)
            return 1
        else:
            print('Conexão não realizada com banco')
            return 0
    except Exception as erro:
        print(f'Erro : {erro}')
        return 0
def inicio_e_menu():
    try:
        while True:
            
            escolha = input('Deseja entrar no módulo de alguma tabela? Digite "s" para prosseguir ou qualquer outra tecla para cancelar: ')
            if escolha != 's':
                print('OPERAÇÃO CANCELADA!')
                comandosql.close()
                conexao.close()
                break
            else:
                
                ans = True
                while ans:
                    print("""
                    1.Dados de um professor por ID
                    2.Dados de varios professores de acordo com a letra inicial
                    3.Nomes disciplinas apartir de curso
                    4.Nome professor mediante a curso
                    5.Carga horaria de um curso (Somente um ano letivo)
                    6.Sair
                    """)
                    ans=input("Oque você deseja fazer? ")
                    if ans=="1":
                      registro = int(input("\nDigite o Registro do professor"))
                      if registrosprofs(registro, ans) == 'a':
                         print('pdf criado com sucesso') 
                    
                    elif ans=="2":
                        registrochar = input('Digite uma sequência de caracteres do professor: ')
                        a = caractere(registrochar, ans)
                      
                    elif ans=="3":
                        disciplinascurso = int(input('Digite o número do curso vinculado a disciplina: '))
                        a = nomepelocurso(disciplinascurso, ans)
                    elif ans=="4":
                        profscurso=int(input('Digite o número do curso vinculado a disciplina: '))
                        a = profpelocurso(profscurso, ans)
                    elif ans=="5":
                        cargahorariapelocurso = int(input('Digite o curso desejado: '))
                        anoletivo = int(input('Digite o ano letivo desejado: '))
                        a = cargahoraria(cargahorariapelocurso, anoletivo, ans)
                    elif ans=="6":
                        ans = None
                          
                    else:
                       print("\n Nenhuma opção valida, tente novamente! ")
    
    except Exception as erro:
        print(f'Ocorreu erro: {erro}')
def gerarpdf(nomes, ans):
    nomearquivo = input('Informe o nome do arquivo PDF que deseja gerar: ') 
    pdf = canvas.Canvas(f'{nomearquivo}.pdf') 
    pdf.setTitle('Relatório de Professores')
    pdf.setFont("Helvetica-Oblique", 16) 
    pdf.drawString(10, 750, 'Relação de Professores:') 

    pdf.setFont("Helvetica-Oblique", 14)
    if ans == "1":
        pdf.drawString(10, 720, 'Registro | Nome professor |   Telefone      |     Idade    |      Salario ') 
        pdf.drawString(30, 700, f'{nomes[0]}       |        {nomes[1]}        |        {nomes[2]}      |       {nomes[3]}      |         {nomes[4]}')
    elif ans == "2":
        espaco = 30
        linha = 700
        pdf.drawString(10, 720, 'Registro | Nome professor |   Telefone      |     Idade    |      Salario ')
        for x in range(len(nomes)):
            espaco = 30
            for y in range(0, 5):
                pdf.drawString(espaco, linha, f'{    nomes[x][y]}  | ')
                espaco += 50
            linha -= 20
    elif ans == "3":
        espaco = 30
        linha = 700
        pdf.drawString(10, 720, 'disciplinas: ')
        for x in range(len(nomes)):
            espaco = 30
            pdf.drawString(espaco, linha, f'{    nomes[x]}   ')
            linha-=40
     
    elif ans == "4":
        espaco = 30
        linha = 700
        pdf.drawString(10, 720, 'Professores:')
        for x in range(len(nomes)):
            espaco = 30
            pdf.drawString(espaco, linha, f'{    nomes[x]}   ')
            linha-=40
    
    elif ans == "5":
        espaco = 30
        linha = 700
        pdf.drawString(10, 720, 'Carga horaria:')
        espaco = 30
        pdf.drawString(espaco, linha, f'{    nomes}  horas ')
        linha-=40    
    pdf.save()
    print(f'{nomearquivo} foi gerado com sucesso: ')
   
def registrosprofs(cod, ans):
    try:
        comandosql.execute(f'select *from professores;')
        todosr = comandosql.fetchall()
        verificar = 0
        if comandosql.rowcount > 0:
            for r in todosr:
                if cod == r[0]:
                    verificar = 1
                    break

        if verificar == 1:
            comandosql.execute(f'select *from professores where registro = {cod};')
            registro = comandosql.fetchone()
            a = gerarpdf(registro, ans)
            return 'a'
        else:
            return 'Não há professor com esse registro!'

    except Exception as erro:
        return '\nOcorreu um erro!'
        
def caractere(info, ans):
    try:
        info = info.capitalize()
        comandosql.execute(f'select *from professores;')
        todosr = comandosql.fetchall()
        nome = list()
        lista = list()
        verificar = 0
        if comandosql.rowcount > 0:
            for r in todosr:
                if info in r[1]:
                    verificar = 1
                    nome.append(r[1])
        if verificar == 1:
            for cont in range(0, len(nome)):
                comandosql.execute(f'select *from professores where nomeprof = "{nome[cont]}";')
                registro = comandosql.fetchone()
                lista.append(registro)
            a = gerarpdf(lista, ans)
            return lista
        else:
            return 'Não há professor que inicie com essa sequência de caracteres!'

    except Exception as erro:
        return '\nOcorreu um erro!'
        

def nomepelocurso(codcurso, ans):
    try:
        
    
        comandosql.execute(f'select curso from disciplinasxprofessores;')
        todosr = comandosql.fetchall()
        lista = list()
        verificar = 0
        if comandosql.rowcount > 0:
            for r in todosr:
                if codcurso == r[0]:
                    verificar = 1
               
        if verificar == 1:
            comandosql.execute(f'select nomedisc from disciplinasxprofessores inner join disciplinas on '
                                f'disciplinasxprofessores.coddisciplina = disciplinas.codigodisc where '
                                f'disciplinasxprofessores.curso = {codcurso};')
            registro = comandosql.fetchall()
            lista.append(registro[0][0])
            if comandosql.rowcount > 0:
                for r in registro:
                    if r[0] not in lista:
                        lista.append(r[0])
                    
                a = gerarpdf(lista, ans)
            

            return lista
        else:
            return 'Não há disciplinas vinculadas a este curso!'
    except Exception as erro:
        return '\nOcorreu um erro!'
def profpelocurso(codcurso, ans):
    try:
        comandosql.execute(f'select curso from disciplinasxprofessores;')
        todosr = comandosql.fetchall()
        lista = list()
        verificar = 0
        if comandosql.rowcount > 0:
            for r in todosr:
                if codcurso == r[0]:
                    verificar = 1
                    break

        if verificar == 1:
            comandosql.execute(f'select nomeprof from disciplinasxprofessores inner join professores on '
                               f'disciplinasxprofessores.codprofessor = professores.registro where '
                               f'disciplinasxprofessores.curso = {codcurso};')
            registro = comandosql.fetchall()
            lista.append(registro[0][0])
            if comandosql.rowcount > 0:
                for r in registro:
                    if r[0] not in lista:
                        lista.append(r[0])
                a = gerarpdf(lista, ans)
            return lista
        else:
            return 'Não há disciplinas vinculadas a este curso!'

    except Exception as erro:
        return '\nOcorreu um erro!'    
def cargahoraria(codcurso, anoletivo, ans):
    try:
        comandosql.execute(f'select curso, anoletivo from disciplinasxprofessores where curso = {codcurso} '
                           f'and anoletivo = {anoletivo};')
        todosr = comandosql.fetchall()
        soma = 0
        verificar = 0

        if comandosql.rowcount > 0:
            for r in todosr:
                if codcurso == r[0]:
                    verificar = 1

        if verificar == 1:
            comandosql.execute(f'select cargahoraria from disciplinasxprofessores where curso = {codcurso} '
                               f'and anoletivo = {anoletivo};')
            registro = comandosql.fetchall()
            if comandosql.rowcount > 0:
                for r in registro:
                    soma += r[0]
                a = gerarpdf(soma, ans)
            return soma

        else:
            return 'Não há registro com essas informações!'

    except Exception as erro:
        return '\nOcorreu um erro!'
    
if abrebanco() == 1:
    iniciar = inicio_e_menu()
    
    comandosql.close()
    conexao.close()

    
else:
    print('FIM DO PROGRAMA!!! Algum problema existente na conexão com banco de dados.')    
