# 정부지원사업 맞춤 추천 MVP

## 개요
정부지원사업과 초기 스타트업 자금조달을 위한 맞춤 추천 및 로드맵 생성 시스템입니다.

## 주요 기능
1. **맞춤 추천**: 회사 정보를 기반으로 한 정부지원사업 추천
2. **신규 공고 알림**: 최근 30일 내 신규 공고 알림
3. **12개월 로드맵**: 월별 지원 가능한 공고 현황 및 로드맵

## 🚀 Streamlit Cloud 배포

### 1. GitHub 저장소 생성
1. GitHub에서 새 저장소 생성
2. 저장소 이름: `government-support-mvp` (또는 원하는 이름)
3. Public 또는 Private 선택

### 2. 코드 업로드
```bash
git add .
git commit -m "Initial commit: Government Support MVP"
git branch -M main
git remote add origin https://github.com/yourusername/government-support-mvp.git
git push -u origin main
```

### 3. Streamlit Cloud 배포
1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. "New app" 클릭
3. GitHub 저장소 선택
4. 메인 파일 경로: `app.py`
5. "Deploy!" 클릭

### 4. 환경변수 설정 (Streamlit Cloud)
Streamlit Cloud의 "Secrets" 섹션에서 다음 설정 추가:
```toml
[supabase]
url = "https://uulghcpqnwgkukfyiypb.supabase.co"
key = "your_supabase_anon_key"
```

## 로컬 개발 환경

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/government-support-mvp.git
cd government-support-mvp
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
`.env` 파일을 생성하고 Supabase 설정을 추가하세요:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 5. 애플리케이션 실행
```bash
streamlit run app.py
```

## 테이블 연동
- **고객사 정보**: `alpha_companies3`
- **맞춤 추천**: `recommend_5`
- **신규 공고 알림**: `recommend_5`
- **로드맵**: `recommend_5`

## 기술 스택
- **Frontend**: Streamlit
- **Backend**: Supabase
- **Data Processing**: Pandas, NumPy
- **Visualization**: Altair
- **Deployment**: Streamlit Cloud

## 주요 개선사항
- ✅ **카드 기반 UI**: 각 공고를 독립적인 카드로 표시
- ✅ **점수 기반 색상 시스템**: 추천도에 따른 직관적인 색상 구분
- ✅ **D-Day 시각화**: 남은 기간을 색상으로 구분
- ✅ **신규 공고 강조**: 빨간 테두리로 신규 공고 표시
- ✅ **월별 시각화**: Altair를 사용한 공고 수 차트
- ✅ **Supabase 연결**: 데모 모드 완전 제거

## 개발자 정보
- 개발일: 2025년 9월 24일
- 버전: 1.0.0
- 배포: Streamlit Cloud
