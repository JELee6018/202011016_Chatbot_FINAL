
# <레벤슈타인 거리를 기반으로한 챗봇 만들기>

# 1. 필요한 라이브러리를 불러오기
import pandas as pd 

# 2. SimpleChatBot 클래스 정의하기
class SimpleChatBot: 
    # 2-1. 인스턴스 초기화
    def __init__(self, filepath):   
        self.questions, self.answers = self.load_data(filepath)
    
    # 2-2. 학습할 데이터 불러오기    
    def load_data(self, filepath):  
        data = pd.read_csv(filepath)  # CSV 파일 읽어오기
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers   #__init__메서드의 self.questions와 self.answers 변수에 저장
    
    # 2-3. 레벤슈타인 거리 구하기(동적계획법 알고리즘)
    def levenshtein_distance(self, s1, s2):
        m = len(s1)   # s1 문자열의 길이를 저장
        n = len(s2)   # s2 문자열의 길이를 저장
        d = [[0 for j in range(n+1)] for i in range(m+1)]   # (m+1) x (n+1) 크기의 2차원 배열 생성
        for i in range(m+1):
            d[i][0] = i    # 첫 번째 열의 값을 초기화
        for j in range(n+1):
            d[0][j] = j    # 첫 번째 행의 값을 초기화
        for j in range(1, n+1):
            for i in range(1, m+1):
                if s1[i-1] == s2[j-1]:   
                    substitution_cost = 0
                else:
                    substitution_cost = 1
                d[i][j] = min(d[i-1][j] + 1,  # 문자 삽입
                              d[i][j-1] + 1,  # 문자 제거
                              d[i-1][j-1] + substitution_cost)  # 문자 변경
        return d[m][n]

    # 2-4. 가장 유사한 질문의 답변 구하기
    def find_best_answer(self, input_sentence):
        min_distance = float('inf')  # 변수 초기화
        best_response_index = None   # 변수 초기화
        for i, question in enumerate(self.questions):  # 각 질문에 대해
            distance = self.levenshtein_distance(input_sentence, question) # 레벤슈타인거리 구하기
            if distance < min_distance:  # 레벤슈타인거리가 최소값보다 작으면
                min_distance = distance  # 최소값 갱신
                best_response_index = i  # 가장 유사한 질문의 인덱스 갱신
        return self.answers[best_response_index]  # 가장 유사한 질문 반환

# 3. CSV 파일 경로 지정
filepath = 'ChatbotData.csv'

# 4. 챗봇 인스턴스를 생성
chatbot = SimpleChatBot(filepath)

# 5. 챗봇과 대화하기 
while True:
    input_text = input('You: ')
    if input_text.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_text)
    print('Chatbot:', response)
    