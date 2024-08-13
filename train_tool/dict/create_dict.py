
#
# 챗봇에서 사용하는 사전 파일 생성
#

import os
from tensorflow.keras import preprocessing
import pickle
import pandas as pd

# 정확한 경로를 확인하고 추가
module_path = '/content/drive/MyDrive/chatbot/utils'


# 모듈 불러오기
from utils.process import Preprocess

# 말뭉치 데이터 가져오기
movie_review = pd.read_csv('/content/drive/MyDrive/chatbot/train_tool/dict/영화리뷰.csv')

# 결측치 제거
movie_review.dropna(inplace=True)

# 말뭉치 데이터에서 문장만 추출
text1 = list(movie_review['document'])

# 말뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성
p = Preprocess()
dict = []
for c in text1:
    pos = p.pos(c)
    for k in pos:
        dict.append(k[0])


# 사전에 사용될 word2index 생성
# 사전의 첫번 째 인덱스에는 OOV 사용
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
tokenizer.fit_on_texts(dict)
word_index = tokenizer.word_index



# 사전 파일 생성
f = open("/content/drive/MyDrive/chatbot/train_tool/dict/chatbot_dict.bin", "wb")
try:
    pickle.dump(word_index, f)
except Exception as e:
    print(e)
finally:
    f.close()