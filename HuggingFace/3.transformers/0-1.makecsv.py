import csv
import random
import os

# 스팸 템플릿
spam_templates = [
    "[Web발신] (광고) {fund} 저금리 대출 안내 드립니다.",
    "고객님은 {adjective} 특별 승인 대상자입니다. 한도 조회하세요.",
    "최저 금리 {rate}% 보장! {speed} 입금 가능합니다.",
    "(광고) {fund} 지원 대출 신청 안내입니다.",
    "신용점수 상관없이 누구나 {amount}만원 승인! {action}"
]

# 정상 템플릿
normal_templates = [
    "[Web발신] {bank}카드 {date} {time} {money}원 결제 완료.",
    "고객님, 요청하신 {doc}이 이메일로 발송되었습니다.",
    "계좌 비밀번호가 {count}회 오류되었습니다. {place} 방문해 주세요.",
    "정기 예금 만기 안내 드립니다. {check} 내용을 확인하세요.",
    "{bank} 점검 안내: 오늘 밤 {hour}시부터 {duration}시간 동안 {status}됩니다."
]

# 랜덤 요소들
banks = ["신한", "KB국민", "우리", "하나", "NH농협", "카카오뱅크", "토스뱅크"]
funds = ["국민행복기금", "서민안정기금", "청년희망기금", "중소기업지원기금", "주택안정기금"]
rates = [2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
amounts = [1000, 2000, 3000, 5000, 7000, 10000]
dates = ["03/02", "04/15", "05/20", "06/01", "07/10", "08/25", "09/30"]
times = ["12:30", "09:15", "18:45", "22:00", "07:50", "14:20"]
moneys = [15000, 25000, 50000, 120000, 300000, 450000]
counts = [1, 2, 3, 4, 5]
hours = [10, 11, 12, 22, 23]
durations = [1, 2, 3, 4]
adjectives = ["비대면", "긴급", "우대", "특별", "한정"]
speed = ["당일 즉시", "빠른", "즉각"]
action = ["상담 클릭", "문의 바랍니다", "신청하세요"]
doc = ["통장 사본", "거래 내역서", "계약서"]
place = ["영업점", "지점", "본점"]
check = ["상세", "추가", "전체"]
status = ["중단", "점검", "일시 정지"]

# 데이터 생성 함수
def generate_sentence(template, label):
    return template.format(
        bank=random.choice(banks),
        fund=random.choice(funds),
        rate=random.choice(rates),
        amount=random.choice(amounts),
        date=random.choice(dates),
        time=random.choice(times),
        money=random.choice(moneys),
        count=random.choice(counts),
        hour=random.choice(hours),
        duration=random.choice(durations),
        adjective=random.choice(adjectives),
        speed=random.choice(speed),
        action=random.choice(action),
        doc=random.choice(doc),
        place=random.choice(place),
        check=random.choice(check),
        status=random.choice(status)
    ), label

# 중복 없는 데이터 생성
dataset = set()
while len(dataset) < 300:
    dataset.add(generate_sentence(random.choice(spam_templates), 1))
    dataset.add(generate_sentence(random.choice(normal_templates), 0))

dataset = list(dataset)
random.shuffle(dataset)

# CSV 저장
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, "data", "일반금융.csv")

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    writer.writerows(dataset)

print(f"✅ CSV 파일 저장 완료: {filename} (총 {len(dataset)}개 데이터)")
