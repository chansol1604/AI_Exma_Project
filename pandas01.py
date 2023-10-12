# -*- coding: utf-8 -*-
"""pandas01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dfIA40FURr7MO51r_PclR1ybC08arn5W

# Pandas 실습
# DataFrame
"""

import pandas as pd
import numpy as np

df = pd.DataFrame([[15, '남', '영훈중'],
                  [17, '여', '성암중']],
                  index = ['서준', '도연'],
                  columns = ['나이', '성별', '학교'])     # 표 형태([[#데이터셋=[데이터],[데이터]],인덱스, 칼럼명)
df

print(df.index)
print(df.columns)

df = df.rename(columns = {'나이':'연령'})
df

df = df.rename(index = {'서준':'학생1', '도연':'학생2'})
df

df1 = df['연령']
print(type(df1))    # type = <class 'pandas.core.series.Series'>, (딕셔너리에 인덱스 추가한 것)
df1                 # column이 하나, 순서가 있음, 인덱싱 가능

df2 = df[['연령']]
print(type(df2))   # type = <class 'pandas.core.frame.DataFrame'>
df2                # column이 여러개

df

df.iloc[0,2]    # 표 형태이기에 2개의 값으로 찾아야 한다.

df.loc['학생1','연령']    # 인덱스, 칼럼을 이용해서 찾을 수도 있다. (순서 중요!)

df.loc['학생3'] = [18, '남', '신일중']    # 데이터 추가
df.loc['학생4'] = [14, '여', '풍문중']
df

# df.drop(['학생3'], inplace = True, axis = 'rows')   # 데이터 삭제
df2 = df.drop(['학생3'], inplace = True, axis = 'rows') # return 값이 없음
df.drop(['학생2'], inplace = False, axis = 'rows')    # inplace = False 사용 시 데이터 삭제 안됨
df1 = df.drop(['학생2'], inplace = False, axis = 'rows')  # 값을 줄때, 데이터를 삭제하고 넘겨주고 싶을 때 사용
print(df)
print(df1)
print(df2)
df

df['학년'] = 3  # 칼럼 추가
df

df['키'] = [175, 180, 185]
df

# df.drop(['학년'], inplace = True,  axis = 'columns') # 칼럼 제거
df2 = df.drop(['키'], inplace = False,  axis = True)   # axis 에 0,1 도 가능. True, False도 가능
df2

df =df[['성별', '학교', '연령', '키']]    # columns의 순서 변경
df

df.loc['학생1', '연령' : '키']    # columns 명으로 하면 뒤의 값까지 출력

df.iloc[0, 2:4]           # 숫자로 슬라이싱 할 때에는 +1을 해줘야 함

df.iloc[0, :3]

exam_data = {'이름' : ['경석','연주','선희'],
             '수학' : [90, 85, 70],
             '영어' : [98, 88, 78],
             '음악' : [90, 89, 88],
             '체육' : [88, 78, 69]}
df = pd.DataFrame(exam_data)
df.set_index('이름', inplace=True)    # 이름을 인덱스로 사용하겠다
df

df.shape

df.iloc[0,3] = 90
df

df.loc['경석','체육'] = 100
df

df.loc['경석',['영어','체육']] = 120, 130     # 120, 130 의 자료형은 튜플
df

df = df.transpose()     # 행과 열을 바꿔줌
df

df = df.T     # T = transpose()
df

df.loc['선희','음악'] = 89

ndf1 = df.set_index('음악')
ndf1

ndf1.loc[89]

ndf2 = df.set_index(['음악','수학'])      # 다중 인덱싱
ndf2

ndf2.loc[89, 70]

ndf2.iloc[1]

ndf3 = df.reset_index().set_index(['음악'])   # 인덱스로 설정된 값을 모르니 초기화하고 인덱스 설정
ndf3

ndf = df.reindex(['경석','연주','선희','덕유','영림'])    # 없는 인덱슬를 추가하면 NaN 값으로 채워줌
ndf

ndf = df.reindex(['경석','연주','선희','덕유','영림'],fill_value = 1)     # fill_value 사용시 그 값으로 NaN값 대체
ndf

ndf = df.sort_index()     # 인덱스를 기준으로 정렬, 오름차순
ndf

ndf = df.sort_index(ascending = False)    # ascending = True -> 오름차순, False -> 내림차순 , 기본값은 True
ndf

ndf = df.sort_values(by = '영어', ascending = False)
ndf

student1 = pd.Series({'국어' : 30, '영어' : 90})
student1

student2 = pd.Series({'국어' : float('NaN'), '영어' : 90})
student2

percentage = student1 / 100
percentage

percentage = student2 / 100       # NaN은 연산은 되지만 결과는 항상 NaN
percentage

student2 = pd.Series({'영어' : 50, '국어' : 40, '수학' : 80})
student2

student1 + student2     # 순서가 달라도 같은 키 값을 가진 것끼리 계산, 같은 키 값이 없을 경우 인덱스는 NaN으로 채워지고 결과값도 NaN으로 연산

student1.add(student2, fill_value = 1)    # NaN값을 채워서 더할 수도 있음

df

ndf = df + 100    # 모든 요소, 각각 연산
ndf

ndf -df

df

df.to_csv('./df_sample.csv')      # 값들을 ','로 구분해서 txt 파일로 저장

df = pd.read_csv('./df_sample.csv',index_col = '이름')      # 인덱스 지정
df

df = pd.read_csv('./df_sample.csv')      # 인덱스 지정하지 않으면 column 명이 없는 기본값 0,1,2,....
df

df.to_csv('./df_sample1.csv')

df= pd.read_csv('./df_sample1.csv')
df

df= pd.read_csv('./df_sample.csv')
df.to_csv('./df_sample.csv', index=False)   # 인덱스에 쓰레기 값이 들어가는 걸 막아줌

df= pd.read_csv('./df_sample.csv',index_col = '이름')
df

df.to_json('./df_sample.json')

ndf = pd.read_json('./df_sample.json')
ndf

df.to_excel('./df_sample.xlsx')

df2 = pd.read_excel('./df_sample.xlsx',index_col=0)
df2

tables = pd.read_html('https://www.w3schools.com/html/html_tables.asp')
print(type(tables))
print(len(tables))

tables[0]

tables[1]

df = pd.read_csv('./datasets/auto-mpg.csv',
names = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'name'])
df

df.head(10)

df.tail(10)

df.shape

df.info()

df.dtypes

df.horsepower.dtypes

df.name.dtypes

df.mpg.dtypes

df.describe()     # 숫자형 데이터만 출력

df.describe(include = 'all').T    # 모든 데이터 출력
#unique = 유니크한 값이 몇개, top = 빈도수가 가장 높은 것, freq = top이 몇 번 나왔냐 =>숫자형 자료형은 NaN으로 출력

df.count()

unique_value = df['name'].value_counts()        # name 칼럼 안에 있는 값들의 수를 세줌
print(type(unique_value))         # <class 'pandas.core.series.Series'>
unique_value

df.mean()

df.mpg.mean()

df.std()

df.corr()       # 상관계수, 상관관계가 크면 클수록 1에 가까워짐(범위 : 1 ~ -1)
# -1은 완벽한 반비례 관계
# 상관관계가 크면 가중치가 2배가 되는 것과 비슷하기 때문에 하나를 제거해야 한다.

mpg_to_kpl = 0.425144                 # 갤런 당 마일을 리터 당 킬로로 바꾸는 값
df['kpl'] = df['mpg'] * mpg_to_kpl
df.head(50)

df['kpl'] = df['kpl'].round(2)    # 2자리수까지 반올림
df.head()

df.info()

df['horsepower'].unique()     # 유니크한 값만 찍어줌

df['horsepower'].replace('?',np.nan, inplace = True)        # ?를 NaN 으로 치환
df.dropna(subset = ['horsepower'], axis = 0 , inplace = True) # horsepoer 중 NaN 값을 가지고 있는 row 삭제
df['horsepower'] = df['horsepower'].astype('float')
df.info()

df['origin'].unique()

df['origin'].replace({1 : 'USA', 2 : 'EU', 3 : 'JP'}, inplace = True)
print(df['origin'].unique())      # 많은 수 대로 정렬됨
print(df['origin'].head())
print(df['origin'].value_counts())

df['origin'] = df['origin'].astype('str')
print(df['origin'].dtypes)  # object
print(df['origin'])

df['origin'] = df['origin'].astype('category')
print(df['origin'].dtypes)  # category
print(df['origin'])         # str과 출력 값은 같음.

df.info()

count, bin_deviders = np.histogram(df['horsepower'], bins = 3)    # 3개 구간으로 나눠라
print(count)        # 나눠진 개수
print(bin_deviders)       # 기준을 나누는 점 4개를 반환(최소, 최대, 나누는 2개 기준점)

bin_names = ['저출력', '보통출력', '고출력']
df['hp_bin'] = pd.cut(x=df['horsepower'], bins = bin_deviders, labels = bin_names, include_lowest = True)
# include_lowest = 기준점에 해당하는 값을 어디에 포함할 것인지(기준 점 이상이냐 초과냐)
print(df[['horsepower', 'hp_bin']].head())

df.info()     # hp_bin 이 자동으로 category 형으로 바뀜

df1 = df[['horsepower', 'hp_bin', 'origin']]
df2 = pd.get_dummies(df1)     # 예제4에서 했던 것보다 간단하게 입력 데이터를 만들 수 있음
df2

from sklearn.preprocessing import StandardScaler        # 평균 0, 분산 1로 조정
from sklearn.preprocessing import Normalizer            # 자료의 평균과 표준편차에 맞춰 정규화
from sklearn.preprocessing import MinMaxScaler          # 최소값을 0 최대값을 1로 잡고 숫자들을 비율에 맞게 정규화

data = np.array([4, 5, 6, 7, 8])
min = 4
max = 8

scaled_data = data - min
print(scaled_data)

scaled_data = scaled_data / (max-min)
print(scaled_data)

minmax_scaler = MinMaxScaler()
data3 = minmax_scaler.fit_transform(data.reshape(-1,1))
print(data3)

data1 = np.array([4, 5, 6, 7, 8, 9])
data1.shape

data2 = np.array([[4, 5], [6, 7], [8, 9]])
data2.shape

reshaped_data = data1.reshape(3, 2)
reshaped_data1 = data1.reshape(2, 3)
reshaped_data2 = data1.reshape(-1, 1)     # 자료 하나하나를 1씩
print(reshaped_data)
print(reshaped_data1)
print(reshaped_data2)

df = pd.DataFrame({'c1' : ['a', 'a', 'b', 'a', 'b'],
                   'c2' : [1, 1, 1, 2, 2],
                   'c3' : [1, 1, 2, 2, 2]})
print(df)

df_dup = df.duplicated()    # 중복 확인, 전의 자료와 같은 것이 있는 지 검사
print(df_dup)

df_dup = df['c2'].duplicated()      # c2만 중복 확인
print(df_dup)

df2 = df.drop_duplicates()      # 중복되는 자료 제거
print(df2)

df2.info()    # Int64Index: 4 entries, 0 to 4, 제거를 시행했을 경우 인덱스가 빠질 수 있다.
              # 만약 삭제되지 않았다면 5 entries, 0 to 4

df2 = df.drop_duplicates(subset = ['c2', 'c3'])     # c2, c3 의 값만 중복 비교해서 제거 시행
print(df2)