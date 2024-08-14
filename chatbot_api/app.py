from flask import Flask, request, jsonify, abort
import socket
import json

# 챗봇 엔진 서버 정보
host = "127.0.0.1"  # 챗봇 엔진 서버 IP
port = 5050         # 챗봇 엔진 port

# Flask 애플리케이션
app = Flask(__name__)

# 챗봇 엔진 서버와 통신
def get_answer_from_engine(bottype, query):
    try:
        mySocket = socket.socket()
        mySocket.connect((host, port))

        json_data = {'Query': query, 'BotType': bottype}
        message = json.dumps(json_data)
        mySocket.send(message.encode())

        data = mySocket.recv(2048).decode()
        ret_data = json.loads(data)

        mySocket.close()
        return ret_data
    except Exception as e:
        print(f"Socket Error: {e}")
        return {'error': '챗봇 엔진과의 통신 오류'}

@app.route('/hello', methods=['GET'])
def index():
    try:
        message = "안녕하세요, 챗봇 입니다 :D \n" \
                  "1.번호안내 2.장소안내\n" \
                  "사용예시 - (학과/트랙/기관명)번호 알려줘, (건물이름)위치 알려줘\n" \
                  "사용예시2 - 컴퓨터공학부 번호 알려줘, 상담실 위치 알려줘\n"
        json_data = {'message': message}
        return jsonify(json_data)

    except Exception as ex:
        print(f"Index Error: {ex}")
        abort(500)

@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    try:
        body = request.get_json()
        if not body or 'query' not in body:
            return jsonify({"error": "잘못된 요청 데이터"}), 400

        if bot_type == 'NORMAL':
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)
        elif bot_type == 'QUICK':
            try:
                with open("./static/json/quick_reply.json", "r", encoding='utf-8') as json_file:
                    data = json.load(json_file)
            except IOError as e:
                print(f"File Read Error: {e}")
                return jsonify({"error": "파일 읽기 오류"}), 500

            request_text = body.get('text')
            for item in data.get('question', []):
                if item.get('text') == request_text:
                    answer = item.get('answer', '답변이 없습니다.')
                    content = item.get('items', [{}])[0].get('content', '정보가 없습니다.')
                    return jsonify({"answer": answer, "content": content})

            return jsonify({"message": "해당 정보가 없습니다."})
        else:
            abort(404)
    except Exception as ex:
        print(f"Query Error: {ex}")
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
