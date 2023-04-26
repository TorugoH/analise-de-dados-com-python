from datetime import datetime, timedelta
import pandas as pd
import requests
import json

# Define as datas de início e fim para as requisições
start_date = datetime(2022, 1, 1)
end_date = start_date + timedelta(days=30)

# Inicializa um dataframe vazio para armazenar os dados
all_data = pd.DataFrame()

# Loop para fazer as requisições e concatenar os dados
for i in range(14):

    # Formata as datas como strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    print('primeiro'+start_date_str)
    print('primeiro'+end_date_str)
    # Faz a requisição HTTP
    response = requests.post("https://api.pontomais.com.br/external_api/v1/reports/delays",
                            headers = {
                                  'Content-Type': 'application/json',
                                   'access-token':'seu token'
                         }
                        ,json= {
                            'report':{
                                'start_date':start_date_str,
                                'end_date':end_date_str,
                                'group_by':'',
                                'row_filters':"employee_name",
                                'columns':"date",
                                'format':'json'
                            }
                        }
    )
    jdata= json.loads(response.text.encode('utf-8'))
    data=pd.json_normalize(jdata)
    jdata1 = jdata['data']
    jdata1
    relatorio_atraso= pd.DataFrame()
    i=0
    for row in jdata1[0]:
            #print(i)    
          # print(row['data'])
          relatorio_atraso = relatorio_atraso.append(row['data'],ignore_index=True)
          i+=1 
    # Concatena os dados retornados para o dataframe
    all_data = pd.concat([all_data, relatorio_atraso], ignore_index=True)
    
    # Avança as datas para o próximo mês
    start_date = end_date
    end_date = start_date + timedelta(days=30)
    print(start_date)
    print(end_date)
  
all_data.to_excel('t5.xlsx')