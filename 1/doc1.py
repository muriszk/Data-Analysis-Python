import pandas as pd

# Creating the entire table 
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

#Showing the table in diferent ways
print("Table with all informations")
print(df)
print("Especific Columns")
print(df["Age"])

# You can create a Series from scratch as well:
#ages1 = pd.Series([32, 45, 98], name="Age1")
#print(ages1)

# Show the maximum value
print("The maximum age:")
print(df["Age"].max())

# Show description of column
print(df.describe())