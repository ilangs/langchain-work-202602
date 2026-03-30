# 3.BPEvsWordPiece.py

# --- [필수 라이브러리 임포트] ---
from tokenizers import Tokenizer, models, trainers, pre_tokenizers  # 토크나이저 핵심 설계 도구
from tokenizers.pre_tokenizers import Whitespace                    # 공백 기반 사전 분리 도구
from tokenizers.trainers import BpeTrainer, WordPieceTrainer        # BPE 및 WordPiece 전용 학습기
import time                                                         # 코드 실행 시간 측정
import os                                                           # 파일 시스템 경로 설정

# 현재 실행 중인 파이썬 파일의 절대 경로를 가져옵니다.
current_file_path = os.path.abspath(__file__)

# 현재 파일이 위치한 디렉토리(폴더)의 절대 경로를 추출합니다.
current_dir = os.path.dirname(current_file_path)
print('current_dir=>', current_dir)  # 작업 경로 확인용 출력

# 실제 학습 데이터가 저장된 txt 파일의 전체 경로를 생성합니다.
txt_path = os.path.join(current_dir, "data", "sample.txt")

# --- [1. 학습 데이터 준비] ---
# 학습에 사용할 파일 경로들을 리스트 형태로 저장합니다.
training_files = [txt_path]

# --- [2. BPE 토크나이저 초기화 및 학습] ---
# BPE 모델 객체를 생성합니다.
bpe_tokenizer = Tokenizer(models.BPE())
# 학습 전, 공백(띄어쓰기)으로 단어를 먼저 나누도록 설정합니다.
bpe_tokenizer.pre_tokenizer = Whitespace()
# BPE 학습 규칙 설정 (사전 크기 2000, 최소 빈도 2, 특수 토큰 등록)
bpe_trainer = BpeTrainer(vocab_size=2000, min_frequency=2, special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"])

start_time = time.time()  # 학습 시작 시간 기록
bpe_tokenizer.train(files=training_files, trainer=bpe_trainer)  # BPE 학습 실행
bpe_time = time.time() - start_time  # 총 학습 시간 계산

# --- [3. WordPiece 토크나이저 초기화 및 학습] ---
# WordPiece 모델 생성 (모르는 단어는 [UNK]로 처리하도록 설정)
wp_tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
# 학습 전 전처리기 설정
wp_tokenizer.pre_tokenizer = Whitespace()
# WordPiece 학습 규칙 설정 (BPE와 동일한 조건으로 설정하여 비교)
wp_trainer = WordPieceTrainer(vocab_size=2000, min_frequency=2, special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"])

start_time = time.time()  # 학습 시작 시간 기록
wp_tokenizer.train(files=training_files, trainer=wp_trainer)  # WordPiece 학습 실행
wp_time = time.time() - start_time  # 총 학습 시간 계산

# --- [4. 동일 문장 토큰화 테스트] ---
test_sentence = "오늘은 날씨가 좋아서 놀러가기 좋은 날입니다."
bpe_output = bpe_tokenizer.encode(test_sentence)  # BPE로 문장 인코딩
wp_output = wp_tokenizer.encode(test_sentence)    # WordPiece로 문장 인코딩

# --- [5. 결과 비교 출력] ---
print("=== BPE 토크나이저 결과 ===")
print("토큰:", bpe_output.tokens)  # 분리된 단어 조각들 출력
print("토큰 ID:", bpe_output.ids)  # 각 조각의 고유 숫자 번호 출력
print("학습 시간:", round(bpe_time, 4), "초")

print("\n=== WordPiece 토크나이저 결과 ===")
print("토큰:", wp_output.tokens)  # 분리된 단어 조각들 출력 (WordPiece는 ## 접두어가 붙을 수 있음)
print("토큰 ID:", wp_output.ids)
print("학습 시간:", round(wp_time, 4), "초")

# --- [6. 어휘 크기 비교] ---
print("\nBPE 어휘 크기:", bpe_tokenizer.get_vocab_size())  # 최종 생성된 사전의 단어 개수 확인
print("WordPiece 어휘 크기:", wp_tokenizer.get_vocab_size())
