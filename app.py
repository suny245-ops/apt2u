import streamlit as st

st.set_page_config(page_title="주택 청약 자격·가점 판별기", layout="centered")
st.title("주택 청약 자격·가점 판별기")
st.caption("규제지역(투기과열·청약과열, 분상제 적용) 기준 표준 로직")

# ===== 점수 로직 =====
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
    elif n == 1: return 10
    elif n == 2: return 15
    elif n == 3: return 20
    elif n == 4: return 25
    elif n == 5: return 30
    else: return 35

def base_points_account(months:int)->int:
    if months < 6: return 1
    elif months < 12: return 2
    elif months < 24: return 3
    elif months < 36: return 4
    elif months < 48: return 5
    elif months < 60: return 6
    elif months < 72: return 7
    elif months < 84: return 8
    elif months < 96: return 9
    elif months < 108: return 10
    elif months < 120: return 11
    elif months < 132: return 12
    elif months < 144: return 13
    elif months < 156: return 14
    elif months < 168: return 15
    elif months < 180: return 16
    else: return 17

def spouse_bonus_points(months:int)->int:
    # 단순 합산 보너스(최대 3점)
    if months <= 0: return 0
    elif months < 12: return 1
    elif months < 24: return 2
    else: return 3

def account_points_with_spouse(self_m:int, spouse_m:int)->int:
    return min(17, base_points_account(self_m) + spouse_bonus_points(spouse_m))

def first_rank_eligibility_regulated(acct_m:int, deposit_ok:bool, seoul_2y:bool, home_count_label:str):
    if home_count_label == "2 이상":
        return ("불가", "2주택 이상은 1순위 제외")
    if acct_m < 24 or not deposit_ok:
        return ("불가", "통장 24개월 미만 또는 예치금 미충족")
    tag = "해당지역 1순위" if seoul_2y else "기타지역 1순위"
    return (tag, "")

def point_applicable(home_count_label:str, past_point_win:bool):
    if home_count_label == "1":
        return (False, "1주택 세대 가점 불가")
    if home_count_label == "2 이상":
        return (False, "2주택 이상 1순위 제외")
    if past_point_win:
        return (False, "최근 2년 내 가점 당첨 이력")
    return (True, "")

# ===== 입력 폼 =====
with st.form("input_form"):
    st.subheader("기본 정보")
    col1, col2 = st.columns(2)
    with col1:
        is_head = st.selectbox("세대주 여부", ["예", "아니오"], index=0) == "예"
        home_count = st.selectbox("세대 주택 보유수", ["0", "1", "2 이상"], index=0)
        past_point_win = st.selectbox("최근 2년 내 가점 당첨 이력", ["없음", "있음"], index=0) == "있음"
        seoul_2y = st.selectbox("서울 2년 연속 거주 여부", ["예", "아니오"], index=0) == "예"
    with col2:
        dependents = st.number_input("부양가족 수(가점 산정값)", min_value=0, max_value=10, value=0, step=1)
        homeless_years = st.number_input("무주택 기간(년)", min_value=0, max_value=30, value=0, step=1)
        homeless_months_extra = st.number_input("무주택 기간(추가 개월)", min_value=0, max_value=11, value=0, step=1)
    total_homeless_months = int(homeless_years)*12 + int(homeless_months_extra)

    st.subheader("청약통장")
    col3, col4 = st.columns(2)
    with col3:
        acct_months = st.number_input("본인 통장 가입기간(개월)", min_value=0, max_value=600, value=0, step=1)
        deposit_ok = st.selectbox("예치금 충족 여부", ["예", "아니오"], index=0) == "예"
    with col4:
        has_spouse = st.selectbox("배우자 여부", ["있음", "없음"], index=1) == "있음"
        spouse_acct_months = st.number_input("배우자 통장 가입기간(개월)", min_value=0, max_value=600, value=0, step=1) if has_spouse else 0

    st.subheader("특별공급 체크")
    col5, col6 = st.columns(2)
    with col5:
        sp_life_first = st.checkbox("생애최초 요건 충족(세대 전원 무주택 + 근로·사업 소득 등)", value=False)
        sp_newlywed = st.checkbox("신혼부부 요건 충족(혼인기간 요건 등)", value=False)
        sp_multi_children = st.checkbox("다자녀 요건 충족(미성년 3명 이상)", value=False)
    with col6:
        sp_elder_parent = st.checkbox("노부모부양 요건 충족(만 65세 이상 장기 동거)", value=False)
        sp_institute = st.checkbox("기관추천 해당(장애·국가유공 등 추천서)", value=False)
        income_asset_ok = st.checkbox("소득·자산 기준 충족(필요 유형만)", value=False)

    submitted = st.form_submit_button("결과 보기")

# ===== 결과 =====
if submitted:
    # 1순위
    rank_tag, rank_reason = first_rank_eligibility_regulated(acct_months, deposit_ok, seoul_2y, home_count)

    # 가점 적용 가능 여부
    point_ok, point_reason = point_applicable(home_count, past_point_win)

    # 점수 계산
    acc_pts = account_points_with_spouse(int(acct_months), int(spouse_acct_months) if has_spouse else 0)
    pts = {
        "무주택기간": points_homeless(int(total_homeless_months)),
        "부양가족": points_dependents(int(dependents)),
        "청약통장": acc_pts
    }
    total_pts = sum(pts.values()) if point_ok else 0

    # 특별공급
    specials = []
    def need_income_ok(flag): return income_asset_ok if flag else True
    if sp_life_first and is_head and need_income_ok(True): specials.append("생애최초")
    if sp_newlywed and is_head and need_income_ok(True): specials.append("신혼부부")
    if sp_multi_children and is_head and need_income_ok(True): specials.append("다자녀")
    if sp_elder_parent and is_head and need_income_ok(False): specials.append("노부모부양")
    if sp_institute: specials.append("기관추천")

    st.subheader("일반공급 결과")
    colA, colB = st.columns(2)
    with colA:
        st.metric("1순위 판정", rank_tag)
        if rank_reason:
            st.write(f"사유: {rank_reason}")
    with colB:
        if point_ok:
            st.metric("가점 총점(84점 만점)", total_pts)
        else:
            st.metric("가점 적용", "불가")
            st.write(f"사유: {point_reason}")

    st.write("항목별 점수")
    st.table({"항목": list(pts.keys()), "점수": list(pts.values())})

    st.subheader("특별공급 결과")
    if specials:
        st.success(", ".join(specials) + " 가능")
    else:
        st.info("특별공급 해당 없음 또는 요건 미충족")

    st.divider()
    st.caption("주의: 실제 소득·자산·세부요건은 단지 공고문을 최종 기준으로 확인하세요.")
else:
    st.info("왼쪽/위의 입력을 채우고 ‘결과 보기’를 눌러주세요.")
