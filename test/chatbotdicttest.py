
# 모듈 불러오기
from utils.process import Preprocess

sent = "내일 오전 10시에 탕수육 주문하고 싶어 ㅋㅋ"

# 전처리 객체 생성
p = Preprocess(userdic='../utils/user_dic.tsv')

# 형태소분석기 실행
pos = p.pos(sent)

# 품사 태그 없이 키워드 출력
keywords = p.get_keywords(pos, without_tag=False)
print(keywords)

# 품사 태그와 같이 키워드 출력
keywords2 = p.get_keywords(pos, without_tag=True)
print(keywords2)