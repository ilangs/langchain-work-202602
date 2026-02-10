import os   # 운영체제 관련 기능(파일 존재 여부 확인, 디렉토리 생성 등)을 사용하기 위한 모듈

# 함수 정의: .env 파일을 읽어서 .toml 파일로 변환
def convert_env_to_toml(env_path=".env", toml_path=".streamlit/secrets.toml"):
    """
    매개변수 설명:
    env_path (str) : 변환할 원본 .env 파일 경로 (기본값=".env")
    toml_path (str): 변환된 결과를 저장할 .toml 파일 경로 (기본값=".streamlit/secrets.toml")
    """

    # 1. .env 파일이 존재하는지 확인
    if not os.path.exists(env_path):
        print(f"{env_path} 파일이 존재하지 않습니다.")  # 없으면 안내 메시지 출력
        return   # 함수 종료

    # 2. .streamlit 폴더 생성 (없으면 자동 생성)
    os.makedirs(os.path.dirname(toml_path), exist_ok=True)

    # 3. .env 파일 읽기
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()   # 모든 줄을 리스트로 가져옴

    toml_lines = []   # 변환된 내용을 담을 리스트 초기화

    # 4. .env 파일의 각 줄을 순회하며 변환
    for line in lines:
        line = line.strip()   # 앞뒤 공백 제거
        if not line or line.startswith("#"):  # 빈 줄이나 주석(#)은 무시
            continue
        if "=" in line:   # KEY=VALUE 형태만 처리
            key, value = line.split("=", 1)   # "=" 기준으로 앞뒤 분리 (최대 1번만 분리)
            key = key.strip()     # KEY 앞뒤 공백 제거
            value = value.strip() # VALUE 앞뒤 공백 제거
            # TOML은 값에 반드시 따옴표 필요
            toml_lines.append(f'{key} = "{value}"\n')

    # 5. 변환된 내용을 .toml 파일로 저장
    with open(toml_path, "w", encoding="utf-8") as f:
        f.writelines(toml_lines)

    # 6. 완료 메시지 출력
    print(f"★ 변환 완료: {toml_path}")

# 7. 스크립트를 직접 실행했을 때만 동작하도록 설정
if __name__ == "__main__":
    # 기본값: 현재 폴더의 .env → .streamlit/secrets.toml
    convert_env_to_toml(env_path=".env", toml_path=".streamlit/secrets.toml")
