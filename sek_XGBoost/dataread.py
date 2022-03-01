"""===============================================================
사전 준비
=========================================================="""

#%%

## example
# run DataRead
# df_train, df_test, df_items,df_item_categories, df_shops = DataRead('./data/')
# only works in notebook

##import library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
##데이터 불러오기, downsize  
# #path example: './data/kaggle1/', 같은 폴더 내 있으면 빈칸으로
def DataRead(path=''):
  import re
  import numpy as np
  import pandas as pd 
  import matplotlib.pyplot as plt
  
  global df_train, df_test, df_items,df_item_categories, df_shops
  
  df_train = pd.read_csv(path+'sales_train.csv')
  df_test = pd.read_csv(path+'test.csv')
  df_items = pd.read_csv(path+'items.csv')
  df_item_categories = pd.read_csv(path+'item_categories.csv')
  df_shops = pd.read_csv(path+'shops.csv')
  ##df_train
  # df_train>날짜 타입으로 변경
  df_train.date = pd.to_datetime(df_train.date, format='%d.%m.%Y')

  ##df_shops -> 시도명타입 추출
  f3= lambda x: x.split(' ')[0].strip()
  df_shops['city'] = df_shops.shop_name.apply(f3)

  f4= lambda x: x[x.find(' '):x.find('"')].strip()
  df_shops['type'] = df_shops.shop_name.apply(f4)
  # 중복 시도명 통합
  for i in range(len(df_shops)):
    if df_shops.iloc[i,2] == '!Якутск':
      df_shops.iloc[i,2] = 'Якутск'  

  ##df_item_categories
  # 대분류/소분류 컬럼 생성
  df_item_categories['main_cat'] = df_item_categories['item_category_name'].str.split(' - ').str[0].str.strip()
  df_item_categories['sub_cat'] = df_item_categories['item_category_name'].str.split(' - ').str[1].str.strip()
  #불필요 컬럼 제거
  df_item_categories=df_item_categories.drop('item_category_name',axis=1)
  #결측치 변환
  df_item_categories=df_item_categories.fillna(method='ffill', axis = 1)

  ## df_items
  #지저분한 이름 정리
  df_items['item_name'] = df_items['item_name'].apply(lambda x: item_name_correction(x))

  ##downcast df_train size
  for i in [df_train, df_test, df_items,df_item_categories, df_shops]:
    i = downcast_dtypes(i)
  return(df_train, df_test, df_items,df_item_categories, df_shops)
  # print('df_train, df_test, df_items,df_item_categories, df_shops')


def downcast_dtypes(df):
    float_cols = [c for c in df if df[c].dtype == "float64"]
    int_cols = [c for c in df if df[c].dtype in ["int64", "int32"]]
    df[float_cols] = df[float_cols].astype(np.float32)
    df[int_cols] = df[int_cols].astype(np.int16)
    return 

def item_name_correction(x):
    x = x.lower()
    x = x.partition('[')[0]
    x = x.partition('(')[0]
    x = re.sub('[^A-Za-z0-9А-Яа-я]+', ' ', x)
    x = x.replace('  ', ' ')
    x = x.strip()
    return x
