# total_TestSplit.py 
# csv 데이터 생성 -> 모델 생성 -> 모델 훈련 -> 학습모델 저장 -> 정확도 평가보고서 -> 스트림릿 화면
# train_test_split: 데이터 중 학습용(80%)은 훈련에만 사용, 평가용(20%)는 학습 완료 후 모델이 한 번도 본 적 없는 데이터로 최종 평가

import os, random, itertools, joblib
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split  # 새로 추가된 필수 모듈

# 웹 페이지 기본 설정
st.set_page_config(page_title="스팸 판별 AI", page_icon="📧", layout="wide")

st.title("📧 금융/스팸 메일 판별 AI 웹 앱")
st.markdown("데이터 개수를 설정하여 모델을 학습시키고, 임의의 문장이 스팸인지 직접 테스트해 보세요.")

# ==========================================
# [1단계 & 3단계] 데이터 생성, 학습 및 평가 보고서
# ==========================================
st.header("1️⃣ 데이터 생성 및 모델 학습")

# 사용자로부터 데이터 개수 입력 받기
col1, col2 = st.columns([1, 3])
with col1:
    total_count = st.number_input("생성할 데이터 총 개수", min_value=10, max_value=2000, value=300, step=10)

with col2:
    st.write("") # 버튼 위치를 맞추기 위한 여백
    st.write("")
    train_button = st.button("🚀 데이터 생성 및 학습 시작", use_container_width=True)

# 학습 버튼을 눌렀을 때 실행
if train_button:
    with st.spinner('데이터를 생성하고 모델을 학습하는 중입니다...'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)

        half_n = total_count // 2
        if total_count % 2 != 0:
            half_n = (total_count + 1) // 2
            st.info(f"50:50 비율을 위해 총 개수를 {half_n * 2}개로 조정합니다.")

        # 단어 풀 (기존 코드와 동일)
        spam_words1 = ["(광고)", "당첨!", "대출", "주식", "특가", "무료", "VIP", "긴급", "마지막 기회", "초특가"]
        spam_words2 = ["최저 금리", "무료 쿠폰", "급등 종목", "최대 80% 할인", "사은품 증정", "수익 보장", "무보증 대출", "포인트 지급", "전액 지원", "특별 이벤트"]
        spam_words3 = ["아래 링크를 클릭하세요.", "지금 바로 신청하세요.", "상담 받아보세요.", "다운로드 하세요.", "연락 바랍니다.", "확인해 보세요.", "절대 놓치지 마세요.", "서둘러 참여하세요.", "고객센터로 문의하세요.", "앱에서 확인하세요."]

        ham_words1 = ["오늘", "내일", "이번 주", "팀장님", "고객님", "대리님", "프로젝트", "회의", "점심", "다음 주"]
        ham_words2 = ["회의 시간", "요청하신 자료", "카드 명세서", "택배 배송", "결제 내역", "업무 보고서", "계약서 초안", "휴가 신청서", "미팅 준비", "일정 변경"]
        ham_words3 = ["확인 부탁드립니다.", "송부해 드립니다.", "도착 예정입니다.", "검토 바랍니다.", "언제 시간 되시나요?", "수정 완료했습니다.", "참고 부탁드립니다.", "다시 연락드리겠습니다.", "미리 감사드립니다.", "공지사항 확인 바랍니다."]

        spam_comb = list(itertools.product(spam_words1, spam_words2, spam_words3))
        ham_comb = list(itertools.product(ham_words1, ham_words2, ham_words3))

        spam_sentences = [f"{w1} {w2} {w3}" for w1, w2, w3 in spam_comb]
        ham_sentences = [f"{w1} {w2} {w3}" for w1, w2, w3 in ham_comb]

        content = random.sample(spam_sentences, half_n) + random.sample(ham_sentences, half_n)
        labels = [1] * half_n + [0] * half_n

        df = pd.DataFrame({"text": content, "label": labels}).sample(frac=1, random_state=42).reset_index(drop=True)
        
        csv_path = os.path.join(data_dir, f"spam_{total_count}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        # ==========================================
        # ✨ 핵심 변경: Train / Test 데이터 분할 (8:2 비율)
        # ==========================================
        X = df['text']
        y = df['label']
        
        # test_size=0.2 (20%를 평가용으로 빼둠), random_state (결과 재현을 위한 고정값)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 파이프라인 생성 및 학습 (80%의 X_train 데이터로만 학습!)
        model = Pipeline([('tfidf', TfidfVectorizer()), ('clf', MultinomialNB())])
        model.fit(X_train, y_train)
        
        st.session_state['model'] = model
        
        model_filename = os.path.join(data_dir, f'finance_spam_model_{total_count}.pkl')
        joblib.dump(model, model_filename)

        st.success(f"✅ 총 {len(df)}개 데이터 중 {len(X_train)}개로 학습, {len(X_test)}개로 평가 준비 완료!")

        st.divider()

        # ==========================================
        # ✨ 실무형 모델 평가 보고서 산출
        # ==========================================
        st.subheader("📊 신뢰도 높은 실무형 평가 보고서 (Test Data 기반)")
        st.caption(f"모델이 한 번도 본 적 없는 {len(X_test)}개의 테스트 데이터로 평가한 결과입니다.")
        
        # 하드코딩된 문장이 아닌, 분할해둔 20%의 테스트 데이터를 모델에 입력하여 예측
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        st.metric(label="모델 정확도 (Accuracy)", value=f"{accuracy * 100:.2f}%")

        col_rep, col_conf = st.columns(2)
        with col_rep:
            st.markdown("**상세 평가 보고서 (Classification Report)**")
            # y_test(실제 정답 20%)와 y_pred(AI가 예측한 정답 20%)를 비교
            report = classification_report(y_test, y_pred, target_names=['정상(HAM)', '스팸(SPAM)'])
            st.text(report) 
            
        with col_conf:
            st.markdown("**혼동 행렬 (Confusion Matrix)**")
            conf_matrix = confusion_matrix(y_test, y_pred)
            df_conf = pd.DataFrame(conf_matrix, columns=['예측_정상', '예측_스팸'], index=['실제_정상', '실제_스팸'])
            st.dataframe(df_conf, use_container_width=True)

st.divider()

# ==========================================
# [2단계] 사용자 인터랙티브 텍스트 테스트
# ==========================================
st.header("2️⃣ 문장 스팸 테스트")

example_sentences = [
    "직접 입력하기...",
    "안녕하세요 팀장님, 내일 점심 식사 가능하신가요?",
    "이번 주 금요일 오후 3시 회의 일정 공유드립니다.",
    "축하합니다! 1억 원 경품에 당첨되셨습니다. 지금 클릭!",
    "(광고) VIP 고객님 최저 금리 무보증 대출 상담 받아보세요.",
    "주식 급등 종목 지금 바로 확인해 보세요."
]

selected_example = st.selectbox("📌 예시 문장 빠른 선택:", example_sentences)

# '직접 입력하기...'가 아니면 선택한 문장을 텍스트 에어리어의 기본값으로 설정
default_text = "" if selected_example == "직접 입력하기..." else selected_example

# 사용자가 텍스트를 수정하거나 새로 입력할 수 있는 최종 입력창
user_input_text = st.text_area("✍️ 테스트할 문장을 입력하세요:", value=default_text, height=100)

if st.button("🔍 스팸 여부 분석하기", type="primary"):
    if 'model' not in st.session_state:
        st.warning("⚠️ 먼저 위에서 **데이터 생성 및 학습 시작** 버튼을 눌러 모델을 학습시켜주세요.")
    elif not user_input_text.strip():
        st.error("⚠️ 분석할 텍스트를 입력해주세요.")
    else:
        # 학습된 모델 가져오기
        loaded_model = st.session_state['model']
        
        # 추론
        pred = loaded_model.predict([user_input_text])[0]
        prob = loaded_model.predict_proba([user_input_text])[0]
        
        score = round(prob[pred] * 100, 2)
        
        # 결과 화면 출력
        st.subheader("💡 분석 결과")
        if pred == 1:
            st.error(f"🚨 **스팸(SPAM)** 메일로 분류되었습니다. (확신도: {score}%)")
        else:
            st.success(f"✅ **정상(HAM)** 메일로 분류되었습니다. (확신도: {score}%)")
        
        # 상세 확률 시각화
        st.progress(int(prob[1] * 100)) 
        st.caption(f"스팸일 확률: {prob[1]*100:.2f}% / 정상일 확률: {prob[0]*100:.2f}%")
