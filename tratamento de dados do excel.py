import pandas as pd

dados = pd.read_excel('dados.xlsx',sheet_name='APURAÇÕES')

def gerar_relatorio (coluna_item,coluna_nota,validacao):
    
    #pegando os campos necessarios para o relatorio
    tabela = dados[['DATA',coluna_item,coluna_nota]]
    tabela=tabela.rename(columns={coluna_item:'AVALIADO ?',coluna_nota:'NOTA'})
    tabela['ITEM']=coluna_item

    #verificando a quantidade de avaliações feitas no mês
    quantidade_Avaliacao= tabela[['DATA','AVALIADO ?','ITEM']]
    quantidade_Avaliacao = quantidade_Avaliacao[quantidade_Avaliacao['AVALIADO ?']==validacao].groupby([pd.Grouper(key='DATA',freq='M'),'ITEM']).count()

    #verficando as avaliações dos itens
    validos = tabela[['DATA','AVALIADO ?','ITEM']]
    validos=validos.groupby([pd.Grouper(key='DATA',freq='M'),'ITEM']).count()

    relatorio = pd.merge(validos,quantidade_Avaliacao, on=['DATA','ITEM'])
    
    return relatorio

#Relatórios por item 
material_misturado = gerar_relatorio('1º - Materiais Misturados nas Posições?','Peso 1º       4','NÃO')
ruas_limpas = gerar_relatorio('2º - Ruas Limpas? (papéis, linhas ou strechs)','Peso 2º     3','SIM')
aramado = gerar_relatorio('3º - Aramados e Palets armaz. Em segurança?','Peso 3º         5','SIM')
materias_chao = gerar_relatorio('4º - Há materiais caidos no chão?','Peso 4º       3','NÃO')
lastro = gerar_relatorio('5º - Lastro sendo respeitado?','Peso 5º      3','SIM')
vazios = gerar_relatorio('6º - Sacos de Rafia ou Caixas vazios?','Peso 6º        2','NÃO')
aramado_fechado = gerar_relatorio('7º - Aramados fechados?','Peso 7º       5','SIM')

#Consolidando tudo em uma única tabela
apuracoes = pd.DataFrame()
apuracoes = pd.concat([material_misturado,ruas_limpas,aramado,materias_chao,lastro,vazios,aramado_fechado])

apuracoes.to_excel("acertividade das vozes.xlsx",index=True)