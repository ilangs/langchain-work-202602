# 1.BpeTrainer.py 파일 작성
      
# --- [필수 라이브러리 임포트] ---
# Tokenizer: 토크나이저의 전체 파이프라인(전처리, 모델, 포스트 프로세싱 등)을 관리하는 메인 클래스
# models: BPE, WordPiece, Unigram 등 실제 토큰화 알고리즘을 선택하기 위한 모듈
# trainers: 선택한 알고리즘을 특정 데이터셋에 맞춰 학습시키는 학습기 모듈
# pre_tokenizers: 문장을 토큰화하기 전, 공백이나 구두점 등으로 미리 나누는 전처리 도구
from tokenizers import Tokenizer, models, trainers, pre_tokenizers

# Whitespace: 가장 기본적인 전처리기 중 하나로, 띄어쓰기(공백)를 기준으로 단어를 분리
from tokenizers.pre_tokenizers import Whitespace

# BpeTrainer: BPE(Byte-Pair Encoding) 알고리즘 전용 학습기로, 빈도수 기반으로 단어 조각 사전을 생성
from tokenizers.trainers import BpeTrainer

# os: 운영체제(OS)의 파일 시스템에 접근하여 경로 생성, 파일 읽기/쓰기 등을 처리하기 위해 사용
import os

# --- [1. 토크나이저 초기화] ---
# BPE(Byte-Pair Encoding) 모델을 기반으로 토크나이저 생성
tokenizer = Tokenizer(models.BPE())

# --- [2. PreTokenizer 설정] ---
# 공백(Whitespace) 기준으로 단어를 먼저 분리하도록 설정
tokenizer.pre_tokenizer = Whitespace()

# 현재 파이썬 파일의 절대경로
current_file_path = os.path.abspath(__file__)

# 현재 파일이 있는 디렉토리 절대경로
current_dir = os.path.dirname(current_file_path)
print('current_dir=>',current_dir) #current_dir=> c:\workAI\work\HuggingFace\2.tokenzier
txt_path = os.path.join(current_dir, "data", "sample.txt")

# --- [3. 학습 데이터 준비] ---
# 예시 텍스트 파일을 학습 데이터로 사용 (여러 문장 포함)
# training_files = ["sample.txt"]  # 미리 준비된 텍스트 파일
training_files = [txt_path]

# --- [4. Trainer 설정] ---
# BPETrainer를 사용하여 토크나이저 학습 규칙 정의
# BPE 알고리즘을 학습시킬 설정값(Trainer)을 정의
trainer = BpeTrainer(
    vocab_size=2000,     # 모델이 배울 전체 단어(토큰) 사전의 최대 크기를 2,000개로 제한
    min_frequency=2,     # 최소 2번 이상 등장한 단어 조합만 사전에 등록하여 노이즈를 방지
    special_tokens=[     # 학습 시 특별한 의미를 부여할 5가지 특수 토큰을 정의
        "[PAD]",         # 1. 문장 길이를 맞추기 위한 빈칸 채우기 (padding) 10글자->5글자+5padding
        "[UNK]",         # 2. 사전에 없는 모르는 단어 처리용 토큰
        "[CLS]",         # 3. 문장 전체의 의미를 담는 시작 지점 토큰
        "[SEP]",         # 4. 문장과 문장을 구분하는 구분자 토큰
        "[MASK]"         # 5. 모델 학습을 위해 단어를 가리는 마스크 토큰 (퀴즈형태로 물어봐서)
    ]
)

# --- [5. 토크나이저 학습 실행] ---
# 준비된 텍스트 파일을 기반으로 토크나이저 학습
tokenizer.train(files=training_files, trainer=trainer) # 매개변수명=전달할값
# = tokenizer.train(training_files, trainer)

# --- [6. 학습된 토크나이저 저장] ---
# current_dir(현재 파일이 있는 디렉토리 절대경로)와 파일명을 결합하여 명시적인 저장 경로 생성
save_path = os.path.join(current_dir, "data", "bpe_tokenizer.json")

# 지정된 절대경로에 토크나이저 JSON 파일을 저장
tokenizer.save(save_path)
print(f"토크나이저가 저장된 경로: {save_path}")

# --- [7. 학습된 토크나이저 불러오기] ---
# 절대경로를 사용하여 저장된 토크나이저를 다시 불러옴
new_tokenizer = Tokenizer.from_file(save_path)

# --- [8. 토큰화 테스트] ---
# 새로운 문장을 토큰화해보기
# output = new_tokenizer.encode("오늘은 날씨가 좋아서 산책하기 좋은 날입니다.")
output = new_tokenizer.encode("지금은 허깅페이스 중에서 토크나이저를 배우고 있습니다.")
print("토큰화 결과:", output.tokens)
print("토큰 ID:", output.ids)

'''
오늘 날씨가 너무 좋아서 기분이 상쾌합니다.

current_dir=> c:\workAI\work\HuggingFace\2.tokenizer
[00:00:00] Pre-processing files (0 Mo)    ████████████████████████████                100%
[00:00:00] Tokenize words                 ████████████████████████████ 7        /        7
[00:00:00] Count pairs                    ████████████████████████████ 7        /        7
[00:00:00] Compute merges                 ████████████████████████████ 0        /        0
토큰화 결과: ['오', '늘', '날', '씨', '가', '좋', '아', '서', '기', '좋', '날', '니', '다', '.']
토큰 ID: [19, 10, 8, 17, 6, 21, 18, 16, 7, 21, 8, 11, 12, 5]
'''

'''
지금은 허깅페이스 중에서 토크나이저를 배우고 있습니다.
=> 훈련시킨 문자열이 중복되어 나오는 빈도수에 따라 영향을 받을 수도 있다.
current_dir=> c:\workAI\work\HuggingFace\2.tokenizer
[00:00:00] Pre-processing files (0 Mo)    ████████████████████████████                100%
[00:00:00] Tokenize words                 ████████████████████████████ 7        /        7
[00:00:00] Count pairs                    ████████████████████████████ 7        /        7
[00:00:00] Compute merges                 ████████████████████████████ 0        /        0
토큰화 결과: ['이', '서', '이', '니', '다', '.']
토큰 ID: [20, 16, 20, 11, 12, 5]
'''
