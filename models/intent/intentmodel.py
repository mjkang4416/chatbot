
import sys
import tensorflow as tf
from config.globalparams import MAX_SEQ_LEN

# from tensorflow.keras.models import load_model

from tensorflow import keras


from tensorflow.keras import preprocessing

# 의도 분류 모델 모듈
class IntentModel:
    def __init__(self, model_name, preprocess):

        # 의도 클래스별 레이블블
        self.labels = {0: "장소", 1: "번호", 2: "공지", 3: "정보", 4: "기타"}

        # 의도 분류 모델 불러오기
        self.model = keras.models.load_model(model_name)
        # self.model = load_model(model_name)

        # 챗봇 텍스트 전처리기
        self.p = preprocess

    # 의도 클래스 예측
    def predict_class(self, query, globalparams=None):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 단어 시퀀스 벡터 크기
        config_path = '../../config'
        if config_path not in sys.path:
          sys.path.append(config_path)


        # 패딩처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]