from cheongyak_core import InputData, evaluate

# 예시 입력(원하는 값으로 수정)
data = InputData(
    is_head=True,
    home_count_label="0",
    past_point_win=False,
    seoul_2y=True,
    dependents=3,                # 부양가족수(가점 산정)
    homeless_months=120,         # 무주택 10년
    acct_months=60,              # 통장 60개월
    deposit_ok=True,
    has_spouse=True,
    spouse_acct_months=24,       # 배우자 24개월
    sp_life_first=True,
    sp_newlywed=False,
    sp_multi_children=False,
    sp_elder_parent=False,
    sp_institute=False,
    income_asset_ok=True
)

result = evaluate(data)

print("=== 일반공급 1순위 ===")
print(result["1순위"]["판정"], "-", result["1순위"]["사유"] or "사유 없음")

print("\n=== 가점 ===")
print("적용:", "가능" if result["가점"]["적용"] else "불가", "-", result["가점"]["사유"] or "사유 없음")
for k, v in result["가점"]["항목별"].items():
    print(f"{k}: {v}점")
print("총점:", result["가점"]["총점"], "/ 84")

print("\n=== 특별공급 ===")
print(", ".join(result["특별공급"]) if result["특별공급"] else "해당 없음")
