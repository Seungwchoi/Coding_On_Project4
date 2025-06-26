import pandas as pd

userList = {}

class User:
    def __init__(self, name, password):  # 생성자
        self.name = name
        self.password = password
        userList[self.name] = {'name': self.name, 'password': self.password}

# pandas DataFrame 변환
df = pd.DataFrame(userList.values())
print(df)
