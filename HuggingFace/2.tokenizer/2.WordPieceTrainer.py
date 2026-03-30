# 2.WordPieceTrainer.py 파일 작성

# --- [필수 라이브러리 임포트] ---
# Tokenizer: 토크나이저의 파이프라인(전처리, 모델, 후처리 등)을 조립하고 관리하는 메인 클래스입니다.
from tokenizers import Tokenizer

# WordPiece: 토큰화 알고리즘으로 WordPiece 모델을 사용하기 위해 임포트합니다.
from tokenizers.models import WordPiece

# WordPieceTrainer: WordPiece 모델을 특정 텍스트 데이터셋에 맞춰 학습시키는 전용 학습기입니다.
from tokenizers.trainers import WordPieceTrainer

# Whitespace: 텍스트를 모델에 넣기 전, 띄어쓰기(공백)를 기준으로 1차 분리하는 전처리 도구입니다.
from tokenizers.pre_tokenizers import Whitespace

# os: 운영체제의 파일 시스템(경로 생성, 디렉토리 확인 등)에 접근하기 위해 사용하는 기본 모듈입니다.
import os

# --- [1. 토크나이저 초기화] ---
# WordPiece 모델을 기반으로 빈 토크나이저 객체를 생성합니다. 
# 사전에 없는 모르는 단어가 등장했을 때 처리할 기본 토큰을 "[UNK]"로 명시적으로 지정합니다.
tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))

# --- [2. PreTokenizer 설정] ---
# 본격적인 서브워드 분리 전에, 문장을 띄어쓰기(공백) 기준으로 먼저 나누도록 전처리기를 설정합니다.
tokenizer.pre_tokenizer = Whitespace()

# 현재 실행 중인 파이썬 스크립트 파일(wordPiece.py)의 절대 경로를 가져옵니다.
current_file_path = os.path.abspath(__file__)

# 현재 파일이 위치한 디렉토리(폴더)의 절대 경로를 추출합니다.
current_dir = os.path.dirname(current_file_path)

# 디렉토리 경로가 정상적으로 잡혔는지 콘솔에 출력하여 확인합니다.
print('current_dir=>', current_dir)

# 학습에 사용할 텍스트 파일(sample.txt)의 전체 경로를 운영체제에 맞게 조합하여 생성합니다.
txt_path = os.path.join(current_dir, "data", "sample.txt")

# --- [3. 학습 데이터 준비] ---
# 학습에 사용할 파일들의 경로를 리스트 형태로 준비합니다. (여러 파일 지정 가능)
training_files = [txt_path]

# --- [4. Trainer 설정] ---
# WordPieceTrainer를 인스턴스화하여 토크나이저가 데이터를 학습할 때 사용할 규칙과 하이퍼파라미터를 정의합니다.
trainer = WordPieceTrainer(
    vocab_size=2000,       # 모델이 구축할 전체 단어(토큰) 사전의 최대 크기를 2,000개로 제한합니다.
    min_frequency=2,       # 데이터 셋에서 최소 2번 이상 등장한 단어(또는 서브워드)만 사전에 등록합니다.
    special_tokens=[       # 모델 학습 및 추론 시 구조적/의미적 역할을 수행할 특수 토큰 배열을 정의합니다.
        "[PAD]",           # 배치 처리 시 문장 길이를 동일하게 맞추기 위해 채워넣는 패딩 토큰입니다.
        "[UNK]",           # 토큰 사전에 존재하지 않는 미등록 단어(Out-Of-Vocabulary)를 대체하는 토큰입니다.
        "[CLS]",           # 문장의 맨 앞에 위치하여 해당 문장 전체의 의미(Context)를 담는 분류용 토큰입니다.
        "[SEP]",           # 두 문장이 입력될 때, 문장과 문장 사이를 구분지어주는 구분자 토큰입니다.
        "[MASK]"           # 마스크드 언어 모델(MLM) 학습 시 단어를 가리고 모델이 맞추도록 할 때 쓰는 토큰입니다.
    ],
    continuing_subword_prefix="##" # WordPiece의 핵심 특징으로, 단어가 쪼개졌을 때 뒤에 붙는 조각임을 표시하는 접두사입니다.
)

# --- [5. 토크나이저 학습 실행] ---
# 준비된 데이터(training_files)와 설정된 학습기(trainer)를 사용하여 토크나이저를 실제로 학습시킵니다.
tokenizer.train(files=training_files, trainer=trainer)

# --- [6. 학습된 토크나이저 저장] ---
# current_dir(현재 파일이 있는 디렉토리 절대경로)와 파일명을 결합하여 명시적인 저장 경로 생성
save_path = os.path.join(current_dir, "data", "wordpiece_tokenizer.json")

# 지정된 절대경로에 토크나이저 JSON 파일을 저장
tokenizer.save(save_path)
print(f"토크나이저가 저장된 경로: {save_path}")

# --- [7. 학습된 토크나이저 불러오기] ---
# 절대경로를 사용하여 저장된 토크나이저를 다시 불러옴
new_tokenizer = Tokenizer.from_file(save_path)

# --- [8. 토큰화 테스트] ---
# 학습된 WordPiece 토크나이저가 한국어 문장을 어떻게 서브워드로 분리하는지 테스트하기 위해 텍스트를 입력합니다.
# output = new_tokenizer.encode("오늘은 날씨가 좋아서 산책하기 좋은 날입니다.")
output = new_tokenizer.encode("지금은 허깅페이스 중에서 토크나이저를 배우고 있습니다.")

# 입력된 문장이 최종적으로 어떤 글자 조각(서브워드, 예: '토큰', '##나이', '##저를')들로 나뉘었는지 텍스트 배열을 출력합니다.
print("토큰화 결과:", output.tokens)

# 분리된 각각의 글자 조각들이 단어 사전(Vocabulary)에서 몇 번 인덱스(고유 번호)에 매핑되어 있는지 정수 배열로 출력합니다.
print("토큰 ID:", output.ids)

'''
오늘은 날씨가 좋아서 산책하기 좋은 날입니다.

current_dir=> c:\workAI\work\HuggingFace\2.tokenizer
[00:00:00] Pre-processing files (0 Mo)    ██████████████████████████████████████████                100%[00:00:00] Tokenize words                 ██████████████████████████████████████████ 7        /        7
[00:00:00] Count pairs                    ██████████████████████████████████████████ 7        /        7
[00:00:00] Compute merges                 ██████████████████████████████████████████ 0        /        0
토큰화 결과: ['[UNK]', '날', '##씨', '##가', '좋', '##아', '##서', '[UNK]', '[UNK]', '[UNK]', '.']      
토큰 ID: [1, 8, 25, 26, 21, 27, 28, 1, 1, 1, 5]

'''

'''
지금은 허깅페이스 중에서 토크나이저를 배우고 있습니다.

current_dir=> c:\workAI\work\HuggingFace\2.tokenizer
[00:00:00] Pre-processing files (0 Mo)    ██████████████████████████████████████████                100%[00:00:00] Tokenize words                 ██████████████████████████████████████████ 7        /        7
[00:00:00] Count pairs                    ██████████████████████████████████████████ 7        /        7
[00:00:00] Compute merges                 ██████████████████████████████████████████ 0        /        0
토큰화 결과: ['[UNK]', '[UNK]', '[UNK]', '[UNK]', '[UNK]', '[UNK]', '.']
토큰 ID: [1, 1, 1, 1, 1, 1, 5]

'''
