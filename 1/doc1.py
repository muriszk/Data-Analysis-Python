import pandas as pd

df = pd.DataFrame(
    {
        "Name":[
            "Braund, Mr Owen Harris",
            "Allen, Mr William Henry",
            "Bonnel, Miss Elizzazbeth",
                ],
        "Age": [22, 35, 58],
        "Sex": ["male",  "male", "female"],
    }
)

print("Tabela com todas as informações")
print(df)
print("Colunas específicas")
print(df["Age"])