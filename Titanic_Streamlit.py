import streamlit as st
import pandas as pd
import numpy as np
# import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

# Streamlit App
st.cache_data.clear()
# Set up the title and description of the app
st.title("Titanic Data Analysis")
st.write("This application analyzes titanic data.")


titanic = pd.read_csv(r"C:/Users/umesh/Downloads/titanic dataset.csv", header = 0, dtype={'Age': np.float64})


st.subheader("Titanic Data :")
st.dataframe(titanic)

st.subheader("Performing Data Cleaning and Analysis :")

st.write(
    r''' 
    #### Survived :
    - 0 = Did not Survive (Died)
    - 1 = Survived

    #### Passenger’s class : 
    - 1 st
    - 2 nd
    - 3 rd
''')


st.subheader("Descriptive Statistics :")
st.dataframe(titanic.describe())


st.write("Name, Ticket, Fare, Cabin this columns can never decide survival of a person, hence we can safely delete it")

del titanic["Name"]
del titanic["Ticket"]
del titanic["Fare"]
del titanic["Cabin"]

st.dataframe(titanic)
st.write("Changing Value for 'Male', 'Female' string values to numeric values , male = 1 and female = 2")

def getNumber(str):
    if str=="male":
        return 1
    else:
        return 2
titanic["Gender"] = titanic["Sex"].apply(getNumber)
# delete Sex Column
del titanic["Sex"]
# Rename Gender - Sex
titanic.rename(columns = {'Gender':'Sex'}, inplace = True)

st.dataframe(titanic)

st.subheader("Null Values Counts :")
st.dataframe(titanic.isnull().sum())

st.markdown("Fill the null values of the Age column. Fill mean Survived age(mean age of the survived people) in the column where the person has survived and mean not Survived age (mean age of the people who have not survived) in the column where person has not survived")

meanS = titanic[titanic.Survived == 1].Age.mean()
# st.dataframe(meanS)

titanic["age"] = np.where(pd.isnull(titanic.Age) & titanic["Survived"] == 1, meanS, titanic["Age"])

meanNS = titanic[titanic.Survived==0].Age.mean()
# st.dataframe(meanNS)
titanic.age.fillna(meanNS, inplace = True)

del titanic['Age'] # delete Age column
titanic.rename(columns = {'age':'Age'}, inplace = True)

st.dataframe(titanic.head())

st.subheader("Null Values Counts :")
st.dataframe(titanic.isnull().sum())

st.markdown("We want to check if 'Embarked' column is is important for analysis or not, that is whether survival of the person depends on the Embarked column value or not")

# Finding the number of people who have survived 
# given that they have embarked or boarded from a particular port
survivedQ = titanic[titanic.Embarked == 'Q'][titanic.Survived == 1].shape[0]
survivedC = titanic[titanic.Embarked == 'C'][titanic.Survived == 1].shape[0]
survivedS = titanic[titanic.Embarked == 'S'][titanic.Survived == 1].shape[0]

survivedQ = titanic[titanic.Embarked == 'Q'][titanic.Survived == 0].shape[0]
survivedC = titanic[titanic.Embarked == 'C'][titanic.Survived == 0].shape[0]
survivedS = titanic[titanic.Embarked == 'S'][titanic.Survived == 0].shape[0]

titanic.dropna(inplace=True)

def getEmb(str):
    if str=="S":
        return 1
    elif str=='Q':
        return 2
    else:
        return 3
titanic["Embark"]=titanic["Embarked"].apply(getEmb)
del titanic['Embarked']
titanic.rename(columns={'Embark':'Embarked'}, inplace=True)

st.dataframe(titanic.head())

st.subheader("Null Values Counts :")
st.dataframe(titanic.isnull().sum())


import matplotlib.pyplot as plt
from matplotlib import style


#Drawing a pie chart for number of males and females aboard

males = (titanic['Sex'] == 1).sum() 
#Summing up all the values of column gender with a 
#condition for male and similary for females
females = (titanic['Sex'] == 2).sum()

st.subheader("Survived Peoples Pie Chart :")
st.write(f"Males : {males}")
st.write(f"Females : {females}")

p = [males, females]
plt.pie(p,    #giving array
    labels = ['Male', 'Female'], #Correspndingly giving labels
    colors = ['green', 'yellow'],   # Corresponding colors
    explode = (0.05, 0),    #How much the gap should me there between the pies
    startangle = 90)  #what start angle should be given
plt.axis('equal') 
# plt.show()

st.pyplot(plt)

st.subheader("Survived Males & Females Pie Chart :")

# More Precise Pie Chart
MaleS = titanic[titanic.Sex == 1][titanic.Survived == 1].shape[0]
MaleN = titanic[titanic.Sex == 1][titanic.Survived == 0].shape[0]
FemaleS = titanic[titanic.Sex == 2][titanic.Survived == 1].shape[0]
FemaleN = titanic[titanic.Sex == 2][titanic.Survived == 0].shape[0]

st.write(f"Survived Males : {MaleS}")
st.write(f"Not Survived Males : {MaleN}")
st.write(f"Survived Females : {FemaleS}")
st.write(f"Not Survived Females : {FemaleN}")

# Create new figure for the second pie chart
plt.figure()
chart = [MaleS, MaleN, FemaleS, FemaleN]
colors = ['lightskyblue', 'yellowgreen', 'Yellow', 'Orange']
labels = ["Survived Male", "Not Survived Male", "Survived Female", "Not Survived Female"]
explode = [0, 0.05, 0, 0.1]
plt.pie(chart, 
        labels = labels, 
        colors = colors, 
        explode = explode, 
        startangle = 100, 
        counterclock = False, 
        autopct = "%.2f%%")
plt.axis("equal")
# plt.show()
st.pyplot(plt)


# Count plot
# st.subheader("Titanic Survival Count :")

# plt.figure(figsize = (6, 8))
# sns.countplot(titanic, x = "Sex", hue = "Survived")

# # Set custom x-axis tick labels
# plt.xticks([0, 1], ['Male', 'Female'])

# # Change legend labels for Survived
# plt.legend(title='Status', labels=['Died', 'Survived'])
# plt.title('Titanic Survival Count by Gender')
# plt.xlabel('Sex')
# plt.ylabel('Passenger Count')
# st.pyplot(plt)
