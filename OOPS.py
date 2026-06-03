# class GreetingMachine:
#     def __init__(self,user_name):
#         self.name = user_name
#     def say_hello(self):
#         print(f"Hello {self.name}")
    
# machine_1 = GreetingMachine('Alice')
# machine_2 = GreetingMachine('Bob')

# print(machine_1.say_hello())
# print(machine_2.say_hello())

class Calculator:
    def __init__(self,number):
        self.number = number
    def add(self,y):
        x = self.number + y
        return x

    def multiply(self, y):
        a = self.number * y
        return a

calc = Calculator(5)
print(calc.add(3))
print(calc.multiply(5))

#############################
import pandas as pd

class Titanic:

    def __init__(self):
        self.model = None
        self.median_age = None
    
    def load_data(self,filepath):
        df = pd.read_csv(filepath)
        return df
    
    def calc_median_age(self,df):
        median = df['Age'].median()
        self.median_age = median
    
    def impute_age(self,df):
        new_df = df.copy()
        new_df['Age'] = new_df['Age'].fillna(self.median_age)
        return new_df

    def map_gender(self, df):   
        new_df = df.copy()
        new_df['Sex'] = new_df['Sex'].map({'male':0,'female':1})
        new_df['CryoSleep'] = new_df['CryoSleep'].map({'False':0, 'True': 1})
        new_df['VIP'] = new_df['VIP'].map({'False': 0, 'True': 1})
        return new_df
    
    def feature_eng(self, df):
        new_df = df.copy()
        dtype_dict = {c : type(c)} for c in df.columns
        columns = ['Cabin','HomePlanet','Destination']
        for c in columns:
            new_df = pd.get_dummies(new_df,columns=c, prefix=c)

    
