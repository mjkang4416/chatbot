from flask import Flask, request, jsonify, abort, render_template
import socket
import json

# 챗봇 엔진 서버 정보
host = "127.0.0.1"      # 챗봇 엔진 서버 IP
port = 5050             # 챗봇 엔진 port

# Flask 애플리케이션
app = Flask(__name__)

# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query' : query,
        'BotType' : bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()

    return ret_data

@app.route('/hello', methods=['GET'])
def index():
    try:
        message = "안녕하세요, 챗봇 입니다 :D \n" \
                  "1.번호안내 2.장소안내\n" \
                  "사용예시 - (학과/트랙/기관명)번호 알려줘, (건물이름)위치 알려줘\n" \
                  "사용예시2 - 컴퓨터공학부 번호 알려줘, 상담실 위치 알려줘\n"
        json_data = {
            'message': message
        }
        message = json.dumps(json_data, ensure_ascii=False)
        message = json.loads(message)
        return jsonify(message)

    except Exception as ex:
        # 오류 발생 시 500 Error
        abort(500)


# 챗봇 엔진 query 전송 API
@app.route('/query/<bot_type>', methods=['GET', 'POST'])
def query(bot_type):
    body = request.get_json()
    try:
        if bot_type == 'NORMAL':
            # 일반 질의응답 API
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)
        elif bot_type == 'QUICK':
            with open("./static/json/quick_reply.json", "r", encoding='utf-8') as json_file:
                data = json.load(json_file)
                # 요청에서 'text' 값을 가져옴
            request_text = body.get('text')

            # 해당 'text'에 맞는 항목을 찾음
            for item in data['question']:
                if item['text'] == request_text:
                    if item['items']:
                        # 'answer'와 'content' 항목을 찾음
                        answer = item.get('answer', '답변이 없습니다.')
                        content = item['items'][0].get('content', '정보가 없습니다.')
                        return jsonify({"answer": answer, "content": content})

            # 'text'에 맞는 항목이 없는 경우
            return jsonify({"message": "해당 정보가 없습니다."})
        else:
            # 정의되지 않은 bot type인 경우 404 Error
            abort(404)

    except Exception as ex:
        # 오류 발생 시 500 Error
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)