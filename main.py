import streamlit as st
import math

# 웹 앱 페이지 설정
st.title("🔢 다기능 계산기 웹 앱")
st.markdown("---")

# 사용자 입력 위젯
st.header("입력")
col1, col2 = st.columns(2)

with col1:
    # 첫 번째 숫자 입력
    num1 = st.number_input("첫 번째 숫자 (x)를 입력하세요:", value=0.0, format="%f")

with col2:
    # 두 번째 숫자 입력 (로그 연산을 위해 0보다 큰 값만 허용)
    if st.session_state.get('operation') in ['로그 연산 (log_b x)']:
        num2 = st.number_input("밑 (b, 0보다 크고 1이 아닌 값)을 입력하세요:", value=10.0, min_value=0.0000001, format="%f")
    else:
        num2 = st.number_input("두 번째 숫자 (y)를 입력하세요:", value=0.0, format="%f")

# 연산 선택
operation_options = [
    "선택하세요",
    "덧셈 (+)",
    "뺄셈 (-)",
    "곱셈 (*)",
    "나눗셈 (/)",
    "모듈러 연산 (%)",
    "지수 연산 (x^y)",
    "로그 연산 (log_b x)"
]
operation = st.selectbox("수행할 연산을 선택하세요:", operation_options, key='operation')

# 계산 로직을 수행하는 함수
def calculate(num1, num2, operation):
    """선택된 연산을 수행하고 결과를 반환합니다."""
    
    # 지수 및 로그 연산을 위한 'math' 모듈의 함수들입니다.
    # 

[Image of scientific calculator functions]

    
    if operation == "덧셈 (+)":
        return num1 + num2, f"{num1} + {num2}"
    elif operation == "뺄셈 (-)":
        return num1 - num2, f"{num1} - {num2}"
    elif operation == "곱셈 (*)":
        return num1 * num2, f"{num1} * {num2}"
    elif operation == "나눗셈 (/)":
        if num2 == 0:
            return "오류: 0으로 나눌 수 없습니다.", "나눗셈"
        return num1 / num2, f"{num1} / {num2}"
    elif operation == "모듈러 연산 (%)":
        if num2 == 0:
            return "오류: 0으로 나눌 수 없습니다.", "모듈러 연산"
        return num1 % num2, f"{num1} % {num2}"
    elif operation == "지수 연산 (x^y)":
        return num1 ** num2, f"{num1}^{num2}"
    elif operation == "로그 연산 (log_b x)":
        if num1 <= 0 or num2 <= 0 or num2 == 1:
            return "오류: 로그 연산의 정의를 확인하세요. x > 0, b > 0, b != 1", "로그 연산"
        try:
            # math.log(x, base) 사용
            result = math.log(num1, num2)
            return result, f"log_{num2}({num1})"
        except ValueError as e:
            return f"오류: {e}", "로그 연산"
    else:
        return None, None

st.markdown("---")

# 계산 버튼
if st.button("계산하기"):
    if operation == "선택하세요":
        st.warning("먼저 수행할 연산을 선택하세요.")
    else:
        result, formula = calculate(num1, num2, operation)
        
        st.header("결과")
        if result is None:
            st.info("연산을 기다리는 중...")
        elif isinstance(result, str) and result.startswith("오류"):
            st.error(f"계산 실패: {result}")
        else:
            st.success(f"**수식:** `{formula}`")
            st.balloons() # 계산 성공 시 풍선 효과 추가
            
            # 소수점 10자리까지 포맷팅하여 표시
            st.markdown(f"## **결과: `{result:.10f}`**")

# 로그인을 위한 Streamlit 튜토리얼 영상이 포함된 검색 결과입니다.
Building A Calculator with Streamlit Components and HTML
