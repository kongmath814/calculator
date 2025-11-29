import streamlit as st
import math

# 웹 앱 페이지 설정
st.set_page_config(page_title="다기능 계산기", layout="centered")

st.title("🔢 다기능 계산기 웹 앱")
st.markdown("Streamlit과 Python으로 구현된 사칙연산, 모듈러, 지수, 로그 연산 계산기입니다.")
st.markdown("---")

# 1. 연산 선택을 먼저 수행
st.header("1. 연산 선택")

# 연산 옵션 정의 (모두 한국어)
operation_options = {
    "선택하세요": {"symbol": None, "x_label": "첫 번째 숫자 (x)를 입력하세요:", "y_label": "두 번째 숫자 (y)를 입력하세요:"},
    "덧셈": {"symbol": "+", "x_label": "첫 번째 숫자 (더해지는 수)를 입력하세요:", "y_label": "두 번째 숫자 (더하는 수)를 입력하세요:"},
    "뺄셈": {"symbol": "-", "x_label": "첫 번째 숫자 (빼지는 수)를 입력하세요:", "y_label": "두 번째 숫자 (빼는 수)를 입력하세요:"},
    "곱셈": {"symbol": "*", "x_label": "첫 번째 숫자 (곱해지는 수)를 입력하세요:", "y_label": "두 번째 숫자 (곱하는 수)를 입력하세요:"},
    "나눗셈": {"symbol": "/", "x_label": "첫 번째 숫자 (나눠지는 수)를 입력하세요:", "y_label": "두 번째 숫자 (나누는 수, 0이 아닌 값)를 입력하세요:"},
    "모듈러 연산": {"symbol": "%", "x_label": "첫 번째 숫자 (나눠지는 수)를 입력하세요:", "y_label": "두 번째 숫자 (나누는 수, 0이 아닌 값)를 입력하세요:"},
    "지수 연산": {"symbol": "^", "x_label": "밑 (Base, x)을 입력하세요:", "y_label": "지수 (Exponent, y)를 입력하세요:"},
    "로그 연산": {"symbol": "log", "x_label": "진수 (x, 0보다 큰 값)를 입력하세요:", "y_label": "밑 (b, 0보다 크고 1이 아닌 값)을 입력하세요:"}
}

# st.session_state를 사용하여 선택된 연산을 저장
if 'selected_operation' not in st.session_state:
    st.session_state.selected_operation = "선택하세요"

selected_operation_name = st.selectbox(
    "수행할 연산을 선택하세요:",
    list(operation_options.keys()),
    key='operation_selectbox'
)

# 선택된 연산의 상세 정보를 가져옵니다.
current_op_details = operation_options[selected_operation_name]

# 2. 숫자 입력 (선택된 연산에 따라 레이블 변경)
st.header("2. 숫자 입력")
col1, col2 = st.columns(2)

# 첫 번째 숫자 입력 (x)
with col1:
    x_label = current_op_details["x_label"]
    num1 = st.number_input(x_label, value=0.0, format="%f", key="num1")

# 두 번째 숫자 입력 (y 또는 밑(b))
with col2:
    y_label = current_op_details["y_label"]
    
    # 로그 연산일 경우 최소값 및 주의 사항 설정
    if selected_operation_name == "로그 연산":
        num2 = st.number_input(y_label, value=10.0, min_value=0.0000001, format="%f", key="num2")
    else:
        num2 = st.number_input(y_label, value=0.0, format="%f", key="num2")

# 계산 로직을 수행하는 함수
def calculate(num1, num2, operation_name):
    """선택된 연산을 수행하고 결과를 반환합니다."""
    
    symbol = operation_options[operation_name]["symbol"]
    
    try:
        if operation_name == "덧셈":
            result = num1 + num2
            formula = f"{num1} + {num2}"
        elif operation_name == "뺄셈":
            result = num1 - num2
            formula = f"{num1} - {num2}"
        elif operation_name == "곱셈":
            result = num1 * num2
            formula = f"{num1} * {num2}"
        elif operation_name == "나눗셈":
            if num2 == 0:
                return "오류: 0으로 나눌 수 없습니다.", "나눗셈"
            result = num1 / num2
            formula = f"{num1} / {num2}"
        elif operation_name == "모듈러 연산":
            if num2 == 0:
                return "오류: 0으로 나눌 수 없습니다.", "모듈러 연산"
            result = num1 % num2
            formula = f"{num1} % {num2}"
        elif operation_name == "지수 연산":
            result = num1 ** num2
            formula = f"{num1}^{num2}"
        elif operation_name == "로그 연산":
            # 로그 정의: 진수(x) > 0, 밑(b) > 0, 밑(b) != 1
            if num1 <= 0 or num2 <= 0 or abs(num2 - 1.0) < 1e-9:
                return "오류: 로그 정의에 따라 진수(x) > 0, 밑(b) > 0, 밑(b) != 1 이어야 합니다.", "로그 연산"
            
            # math.log(x, base) 사용
            result = math.log(num1, num2)
            formula = f"log_{num2}({num1})"
        else:
            return None, None # 연산 선택 전
        
        return result, formula

    except Exception as e:
        return f"예상치 못한 오류 발생: {e}", operation_name


st.markdown("---")

# 3. 계산 버튼 및 결과 표시
if st.button("계산 실행"):
    if selected_operation_name == "선택하세요":
        st.warning("먼저 '수행할 연산을 선택하세요'.")
    else:
        result, formula = calculate(num1, num2, selected_operation_name)
        
        st.header("3. 계산 결과")

        if result is None:
            st.info("연산을 기다리는 중...")
        elif isinstance(result, str) and result.startswith("오류"):
            st.error(f"계산 실패: {result}")
        else:
            st.success(f"**수행된 연산 ({selected_operation_name}):** `{formula}`")
            st.balloons() # 계산 성공 시 풍선 효과 추가
            
            # 소수점 10자리까지 포맷팅하여 표시
            st.markdown(f"## **결과: `{result:.10f}`**")

# footer
st.markdown("---")
st.caption("참고: 계산 결과는 소수점 10자리까지 표시됩니다.")
