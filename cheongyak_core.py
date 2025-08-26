from dataclasses import dataclass
from typing import Dict

@dataclass
class InputData:
    is_head: bool
    home_count_label: str    # "0" | "1" | "2 이상"
    past_point_win: bool
    seoul_2y: bool
    dependents: int
    homeless_months: int
    acct_months: int
    deposit_ok: bool
    has_spouse: bool
    spouse_acct_months: int
    sp_life_first: bool
    sp_newlywed: bool
    sp_multi_children: bool
    sp_elder_parent: bool
    sp_institute: bool
    income_asset_ok: bool

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
    if months <= 0: return 0
    elif months < 12: return 1
    elif months < 24: return 2
    else: return 3

def account_points_with_spouse(self_m:int, spouse_m:int)->int:
    base = base_points_account(self_m)
    bonus = spouse_bonus_points(spouse_m)
    return min(17, base + bonus)

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

def evaluate(data: InputData) -> Dict:
    rank_tag, rank_reason = first_rank_eligibility_regulated(
        data.acct_months, data.deposit_ok, data.seoul_2y, data.home_count_label
    )
    point_ok, point_reason = point_applicable(data.home_count_label, data.past_point_win)
    acc_pts = account_points_with_spouse(
        data.acct_months, data.spouse_acct_months if data.has_spouse else 0
    )
    pts = {
        "무주택기간": points_homeless(data.homeless_months),
        "부양가족": points_dependents(data.dependents),
        "청약통장": acc_pts
    }
    total_pts = sum(pts.values()) if point_ok else 0

    specials = []
    def need_income_ok(flag): return data.income_asset_ok if flag else True
    if data.sp_life_first and data.is_head and need_income_ok(True): specials.append("생애최초")
    if data.sp_newlywed and data.is_head and need_income_ok(True): specials.append("신혼부부")
    if data.sp_multi_children and data.is_head and need_income_ok(True): specials.append("다자녀")
    if data.sp_elder_parent and data.is_head and need_income_ok(False): specials.append("노부모부양")
    if data.sp_institute: specials.append("기관추천")

    return {
        "1순위": {"판정": rank_tag, "사유": rank_reason},
        "가점": {"적용": point_ok, "사유": point_reason, "항목별": pts, "총점": total_pts},
        "특별공급": specials
    }
