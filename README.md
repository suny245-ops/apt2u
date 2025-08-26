# 주택 청약 자격·가점 판별기 (규제지역 기준)

규제지역(투기과열·청약과열, 분상제 적용) 기준의 표준 로직으로 일반공급 1순위 판정, 가점(84점) 계산, 특별공급 적격성을 간단 판별하는 미니앱입니다.

## 파일 구조
.
├── app.py
├── cheongyak_core.py
├── cheongyak_jupyter_demo.py
├── requirements.txt
└── README.md

## 로컬 실행
pip install -r requirements.txt
streamlit run app.py

## Jupyter/콘솔 데모
python cheongyak_jupyter_demo.py

## 참고
본 앱의 규칙은 규제지역 기준으로 설계되었습니다. 실제 단지의 세부 요건은 해당 공고문이 최종 기준입니다.
