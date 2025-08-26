import streamlit as st

st.set_page_config(page_title="주택 청약 자격·가점 판별기", layout="centered")
st.title("주택 청약 자격·가점 판별기")
st.caption("규제지역(투기과열·청약과열, 분상제 적용) 기준의 표준 로직")

# 입력
st.subheader("기본 정보")
col1, col2 = st.columns(2)
with col1:
    is_head = st.selectbox("세대주 여부", ["예", "아니오"]) == "예"
    home_count = st.selectbox("세대 주택 보유수", ["0", "1", "2 이상"])
    past_point_win = st.selectbox("최근 2년 내 가점 당첨 이력", ["없음", "있음"]) == "있음"
    seoul_2y = st.selectbox("서울 2년 연속 거주 여부", ["예", "아니오"]) == "예"
with col2:
    dependents = st.number_input("부양가족 수(가점 산정값)", min_value=0, max_value=10, value=0, step=1)
    homeless_years = st.number_input("무주택 기간(년)", min_value=0, max_value=30, value=0, step=1)
    homeless_months_extra = st.number_input("무주택 기간(추가 개월)", min_value=0, max_value=11, value=0, step=1)
    total_homeless_months = homeless_years*12 + homeless_months_extra

st.subheader("청약통장")
col3, col4 = st.columns(2)
with col3:
    acct_months = st.number_input("본인 통장 가입기간(개월)", min_value=0, max_value=600, value=0, step=1)
    deposit_ok = st.selectbox("예치금 충족 여부", ["예", "아니오"]) == "예"
with col4:
    has_spouse = st.selectbox("배우자 여부", ["있음", "없음"]) == "있음"
    spouse_acct_months = st.number_input("배우자 통장 가입기간(개월)", min_value=0, max_value=600, value=0, step=1) if has_spouse else 0

st.subheader("특별공급 체크")
col5, col6 = st.columns(2)
with col5:
    sp_life_first = st.checkbox("생애최초 요건 충족(세대 전원 무주택 + 근로·사업 소득 등)")
    sp_newlywed = st.checkbox("신혼부부 요건 충족(혼인기간 요건 등)")
    sp_multi_children = st.checkbox("다자녀 요건 충족(미성년 3명 이상)")
with col6:
    sp_elder_parent = st.checkbox("노부모부양 요건 충족(만 65세 이상 장기 동거)")
    sp_institute = st.checkbox("기관추천 해당(장애·국가유공 등 추천서)")
    income_asset_ok = st.checkbox("소득·자산 기준 충족(필요 유형만)")

# 로직 함수
def points_homeless(months:int)->int:
    y = months/12
    if y < 1: return 2
    elif y < 2: return 4
    elif y < 3: return 6
    elif y < 4: return 8
    elif y < 5: return 10
    elif y < 6: return 12
    elif y < 7: return 14
    elif y < 8: return 16
    elif y < 9: return 18
    elif y < 10: return 20
    elif y < 11: return 22
    elif y < 12: return 24
    elif y < 13: return 26
    elif y < 14: return 28
    elif y < 15: return 30
    else: return 32

def points_dependents(n:int)->int:
    if n <= 0: return 5
    elif n
