# -*- coding: utf-8 -*-
"""model_intent_test.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tIPeixy7hZhg3etMuyRDlOU-Yr-aOWob
"""

!pip install konlpy

# Google Drive 마운트
from google.colab import drive
drive.mount('/content/drive')

import sys
utils_path = '/content/drive/MyDrive/chatbot/utils'
if utils_path not in sys.path:
    sys.path.append(utils_path)


from process import Preprocess

# 경로 설정
model_path = '/content/drive/MyDrive/chatbot/models/intent'
if model_path not in sys.path:
    sys.path.append(model_path)


# 필요한 모듈 임포트
from intentmodel import IntentModel

p = Preprocess(word2index_dic='/content/drive/MyDrive/chatbot/train_tool/dict/chatbot_dict.bin',
               userdic='/content/drive/MyDrive/chatbot/utils/user_dic.tsv')

intent = IntentModel(model_name='/content/drive/MyDrive/chatbot/models/intent/intent_model.h5', preprocess=p)

query = "컴퓨터공학과 공지사항 링크줘 "
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "학자금 번호 알려줘 "
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "등록금 번호 알려줘 "
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "등록금"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "국제교류팀 번호 알려줘"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)


query = "국제교류"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)

query = "전과"
predict = intent.predict_class(query)
predict_label = intent.labels[predict]
print("="*30)
print(query)
print("의도 예측 클래스 : ", predict)
print("의도 예측 레이블 : ", predict_label)
print("="*30)