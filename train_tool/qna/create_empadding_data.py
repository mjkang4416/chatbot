import pandas as pd
from tqdm import tqdm

tqdm.pandas()

import torch
from sentence_transformers import SentenceTransformer


# train_file = "/content/drive/MyDrive/chatbot/train_tool/qna/train_data.xlsx"
# model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

# df = pd.read_excel(train_file)
# df['embedding_vector'] = df['질문(Query)'].progress_map(lambda x : model.encode(x))
# df.to_excel("train_data_embedding.xlsx", index=False)

# embedding_data = torch.tensor(df['embedding_vector'].tolist())
# torch.save(embedding_data, 'embedding_data.pt')


class create_embedding_data:
    def __init__(self, preprocess, df):
        # 텍스트 전처리기
        self.p = preprocess

        # 질문 데이터프레임
        self.df = df

        # pre-trained SBERT
        self.model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

    def create_pt_file(self):
        # 질문 목록 리스트
        target_df = list(self.df['질문(Query)'])

        # 형태소 분석
        for i in range(len(target_df)):
            sentence = target_df[i]
            if isinstance(sentence, float):  # float 타입의 질문을 빈 문자열로 변환
                sentence = ""
            pos = self.p.pos(sentence)
            keywords = self.p.get_keywords(pos, without_tag=True)
            temp = " ".join(keywords)
            target_df[i] = temp
            # for k in keywords:
            #     temp += str(k)
            # target_df[i] = temp

        self.df['질문 전처리'] = target_df
        self.df['embedding_vector'] = self.df['질문 전처리'].progress_map(lambda x : self.model.encode(x))
        self.df.to_excel("./train_data_embedding.xlsx", index=False)
        embedding_data = torch.tensor(self.df['embedding_vector'].tolist())
        torch.save(embedding_data, 'embedding_data.pt')