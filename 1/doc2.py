import pandas as pd

qtdColunas = int(input("Digite a quantidade de colunas: "))

colunas = []

for i in range(qtdColunas):
    coluna = str(input("Digite o nome da coluna[i]"))
    conteudo = str(str(input("Digite o valor da coluna [i]")))

    df = pd.DataFrame({
        f"{coluna}":[
            conteudo      
        ]
    })

print(df)