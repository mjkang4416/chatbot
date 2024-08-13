
import numpy as np
from numpy import dot
from numpy.linalg import norm
from safetensors import torch
from sentence_transformers import SentenceTransformer, util

import torch


class FindAnswer:
    def __init__(self, preprocess, df, embedding_data):
        # 챗봇 텍스트 전처리기
        self.p = preprocess

        # pre-trained SBERT
        self.model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

        # 질문 데이터프레임
        self.df = df

        # embedding_data
        self.embedding_data = embedding_data


    def search(self, query, intent):
        # 형태소 분석
        pos = self.p.pos(query)

        print(pos)

        # 불용어 제거
        keywords = self.p.get_keywords(pos, without_tag=True)
        query_pre = ""
        for k in keywords:
            query_pre += str(k)

        # 전처리된 질문 인코딩 및 텐서화
        query_encode = self.model.encode(query_pre)
        print(query_encode)
        query_tensor = torch.tensor(query_encode ,dtype=torch.float32)
        print(query_tensor)

        print(type(query_tensor))
        print(type(self.embedding_data))


        # 코사인 유사도를 통해 질문 데이터 선택
        cos_sim = util.cos_sim(query_tensor, self.embedding_data)
        print(cos_sim)
        best_sim_idx = int(np.argmax(cos_sim))
        print(best_sim_idx)
        selected_qes = self.df['질문(Query)'][best_sim_idx]
        query_intent = self.df['의도(Intent)'][best_sim_idx]

        if self.df['의도(Intent)'][best_sim_idx] == intent:
            # 선택된 질문 문장 인코딩
            selected_qes_encode = self.model.encode(selected_qes)

            # 유사도 점수 측정
            score = dot(query_tensor, selected_qes_encode) / (norm(query_tensor) * norm(selected_qes_encode))

            # 답변
            answer = self.df['답변(Answer)'][best_sim_idx]
            imageUrl = self. df['답변 이미지'][best_sim_idx]

            # 의도가 3번인 경우
            if intent == 3:
                answer = self.df['답변(Answer)'][best_sim_idx]
                imageUrl = None  # 이미지가 없는 경우

        else:
            score = 0
            answer = self.df['답변(Answer)'][best_sim_idx]
            imageUrl = self.df['답변 이미지'][best_sim_idx]

        return selected_qes, score, answer, imageUrl, query_intent
