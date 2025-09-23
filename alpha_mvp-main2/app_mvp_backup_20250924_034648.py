import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
import altair as alt
from supabase import create_client, Client
import json
from config import get_supabase_config

# Supabase 설정 가져오기
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()

# Supabase 설정
@st.cache_resource
def init_supabase():
    """Supabase 클라이언트 초기화"""
    try:
        if not SUPABASE_URL or not SUPABASE_KEY:
            st.error("❌ Supabase 설정이 없습니다. config.py 파일을 확인해주세요.")
            st.stop()
        
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"❌ Supabase 연결 실패: {e}")
        st.error("Supabase 설정을 확인하고 다시 시도해주세요.")
        st.stop()

supabase: Client = init_supabase()

@st.cache_data(ttl=30)
def load_companies() -> pd.DataFrame:
    """회사 데이터 로드 (alpha_companies3 테이블 사용)"""
    try:
        if supabase is None:
            return pd.DataFrame()
        
        # alpha_companies3 테이블에서 기업 데이터 로드
        result = supabase.table('alpha_companies3').select('*').execute()
        df = pd.DataFrame(result.data)
        
        if df.empty:
            return df
        
        # 컬럼명을 표준화
        df = df.rename(columns={
            '기업명': 'company_name',
            '사업아이템 한 줄 소개': 'description',
            '주요 산업': 'industry',
            '특화분야': 'specialization',
            '소재지': 'location',
            '#매출': 'revenue',
            '#고용': 'employees',
            '#기술특허(등록)': 'patents',
            '#기업인증': 'certifications'
        })
        
        # ID 컬럼 추가 (No. 컬럼을 ID로 사용)
        df['id'] = df['No.']
        
        return df
    except Exception as e:
        st.error(f"회사 데이터 로드 실패: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def load_recommendations(company_name: str = None) -> pd.DataFrame:
    """추천 데이터 로드 (recommend_5 테이블 사용)"""
    try:
        if supabase is None:
            return pd.DataFrame()
        
        query = supabase.table('recommend_5').select('*')
        
        if company_name:
            query = query.eq('회사명', company_name)
        
        result = query.execute()
        df = pd.DataFrame(result.data)
        
        if df.empty:
            return df
        
        # 컬럼명을 표준화
        df = df.rename(columns={
            '회사명': 'company_name',
            '공고명': 'announcement_title',
            '공고_내용': 'announcement_content',
            '공고_지원분야': 'support_field',
            '공고_지역': 'region',
            '공고_기관': 'agency',
            '공고_신청기간': 'application_period',
            '공고_URL': 'url',
            '추천_점수': 'score',
            '추천_이유': 'reason',
            '생성_시간': 'created_at'
        })
        
        return df
    except Exception as e:
        st.error(f"추천 데이터 로드 실패: {e}")
        return pd.DataFrame()

def calculate_dday(due_date_str: str) -> Optional[int]:
    """D-Day 계산"""
    try:
        if not due_date_str or due_date_str == '-':
            return None
        
        # 다양한 날짜 형식 처리
        date_formats = [
            '%Y-%m-%d',
            '%Y.%m.%d',
            '%m/%d/%Y',
            '%d/%m/%Y'
        ]
        
        for fmt in date_formats:
            try:
                due_date = datetime.strptime(due_date_str, fmt).date()
                today = date.today()
                dday = (due_date - today).days
                return dday
            except ValueError:
                continue
        
        return None
    except:
        return None

def render_custom_recommendations(company_name: str):
    """맞춤 추천 탭"""
    st.subheader("🎯 맞춤 추천")
    
    # 추천 데이터 로드
    recommendations_df = load_recommendations(company_name)
    
    if recommendations_df.empty:
        st.info("해당 회사에 대한 추천 데이터가 없습니다.")
        return
    
    # 필터 옵션
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 점수 필터 (0-1 범위를 0-100으로 변환)
        min_score = st.slider("최소 추천 점수", 0, 100, 30)
        min_score_normalized = min_score / 100  # 0-100을 0-1로 정규화
        filtered_df = recommendations_df[recommendations_df['score'] >= min_score_normalized]
    
    with col2:
        # 지역 필터
        regions = ['전체'] + sorted(recommendations_df['region'].dropna().unique().tolist())
        selected_region = st.selectbox("지역", regions)
        if selected_region != '전체':
            filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    with col3:
        # 기관 필터
        agencies = ['전체'] + sorted(recommendations_df['agency'].dropna().unique().tolist())
        selected_agency = st.selectbox("지원기관", agencies)
        if selected_agency != '전체':
            filtered_df = filtered_df[filtered_df['agency'] == selected_agency]
    
    # 추천 결과 표시
    if not filtered_df.empty:
        st.success(f"📊 {len(filtered_df)}개의 맞춤 추천을 찾았습니다!")
        
        # 점수별 정렬
        filtered_df = filtered_df.sort_values('score', ascending=False)
        
        # 카드 형태로 표시
        for idx, row in filtered_df.iterrows():
            score_display = int(row['score'] * 100)  # 0-1을 0-100으로 변환
            
            # 카드 컨테이너
            with st.container():
                # 점수에 따른 색상 결정
                if score_display >= 80:
                    color = "🟢"
                elif score_display >= 60:
                    color = "🟡"
                else:
                    color = "🔴"
                
                # 메인 카드
                st.markdown(f"""
                <div style="
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                        <h3 style="margin: 0; color: #2c3e50; flex: 1;">{color} {row['announcement_title']}</h3>
                        <div style="text-align: right;">
                            <div style="font-size: 24px; font-weight: bold; color: #3498db;">{score_display}</div>
                            <div style="font-size: 12px; color: #7f8c8d;">점수</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 상세 정보를 2열로 표시
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # 기본 정보
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.markdown(f"**🏢 지원기관**\n{row['agency'] if pd.notna(row['agency']) else '정보 없음'}")
                        st.markdown(f"**📍 지역**\n{row['region'] if pd.notna(row['region']) else '정보 없음'}")
                    
                    with info_col2:
                        st.markdown(f"**🎯 지원분야**\n{row['support_field'] if pd.notna(row['support_field']) else '정보 없음'}")
                        st.markdown(f"**📅 신청기간**\n{row['application_period'] if pd.notna(row['application_period']) else '정보 없음'}")
                    
                    # 공고 내용 (있는 경우)
                    if pd.notna(row['announcement_content']) and row['announcement_content'].strip():
                        with st.expander("📄 공고 내용 보기", expanded=False):
                            st.write(row['announcement_content'])
                    
                    # 추천 이유 (있는 경우)
                    if pd.notna(row['reason']) and row['reason'].strip():
                        with st.expander("💡 추천 이유 보기", expanded=False):
                            st.write(row['reason'])
                
                with col2:
                    # D-Day 계산 및 표시
                    dday = calculate_dday(row['application_period'])
                    if dday is not None:
                        if dday > 0:
                            st.markdown(f"""
                            <div style="
                                background: #e8f5e8;
                                border: 1px solid #4caf50;
                                border-radius: 8px;
                                padding: 15px;
                                text-align: center;
                                margin-bottom: 10px;
                            ">
                                <div style="font-size: 18px; font-weight: bold; color: #2e7d32;">D-{dday}</div>
                                <div style="font-size: 12px; color: #4caf50;">일 남음</div>
                            </div>
                            """, unsafe_allow_html=True)
                        elif dday == 0:
                            st.markdown(f"""
                            <div style="
                                background: #fff3e0;
                                border: 1px solid #ff9800;
                                border-radius: 8px;
                                padding: 15px;
                                text-align: center;
                                margin-bottom: 10px;
                            ">
                                <div style="font-size: 18px; font-weight: bold; color: #f57c00;">오늘 마감!</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="
                                background: #ffebee;
                                border: 1px solid #f44336;
                                border-radius: 8px;
                                padding: 15px;
                                text-align: center;
                                margin-bottom: 10px;
                            ">
                                <div style="font-size: 18px; font-weight: bold; color: #d32f2f;">D+{abs(dday)}</div>
                                <div style="font-size: 12px; color: #f44336;">일 지남</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # 공고 보기 버튼
                    if pd.notna(row['url']) and row['url'].strip():
                        st.link_button("🔗 공고 보기", row['url'], use_container_width=True)
                    else:
                        st.info("🔗 링크 없음")
                
                # 구분선
                st.markdown("---")
    else:
        st.info("필터 조건에 맞는 추천이 없습니다.")

def render_new_announcement_alerts(company_name: str):
    """신규 공고 알림 탭"""
    st.subheader("🔔 신규 공고 알림")
    
    # 추천 데이터 로드
    recommendations_df = load_recommendations(company_name)
    
    if recommendations_df.empty:
        st.info("해당 회사에 대한 공고 데이터가 없습니다.")
        return
    
    # 최근 30일 내 생성된 공고 필터링
    if 'created_at' in recommendations_df.columns:
        recommendations_df['created_at'] = pd.to_datetime(recommendations_df['created_at'], errors='coerce')
        # timezone-aware datetime으로 변환
        cutoff_date = pd.Timestamp.now(tz='UTC') - timedelta(days=30)
        recent_df = recommendations_df[recommendations_df['created_at'] >= cutoff_date]
    else:
        recent_df = recommendations_df
    
    if recent_df.empty:
        st.info("최근 30일 내 신규 공고가 없습니다.")
        return
    
    st.success(f"📢 {len(recent_df)}개의 신규 공고를 발견했습니다!")
    
    # 신규 공고 목록 - 카드 형태로 표시
    for idx, row in recent_df.iterrows():
        score_display = int(row['score'] * 100)
        
        # 카드 컨테이너
        with st.container():
            # 신규 공고 표시
            st.markdown(f"""
            <div style="
                border: 2px solid #ff6b6b;
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
                background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
                box-shadow: 0 2px 4px rgba(255,107,107,0.2);
            ">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #2c3e50; flex: 1;">🆕 {row['announcement_title']}</h3>
                    <div style="text-align: right;">
                        <div style="font-size: 24px; font-weight: bold; color: #ff6b6b;">{score_display}</div>
                        <div style="font-size: 12px; color: #7f8c8d;">점수</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 상세 정보를 2열로 표시
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # 기본 정보
                info_col1, info_col2 = st.columns(2)
                
                with info_col1:
                    st.markdown(f"**🏢 지원기관**\n{row['agency'] if pd.notna(row['agency']) else '정보 없음'}")
                    st.markdown(f"**📍 지역**\n{row['region'] if pd.notna(row['region']) else '정보 없음'}")
                
                with info_col2:
                    st.markdown(f"**🎯 지원분야**\n{row['support_field'] if pd.notna(row['support_field']) else '정보 없음'}")
                    st.markdown(f"**📅 신청기간**\n{row['application_period'] if pd.notna(row['application_period']) else '정보 없음'}")
                
                # 공고 내용 (있는 경우)
                if pd.notna(row['announcement_content']) and row['announcement_content'].strip():
                    with st.expander("📄 공고 내용 보기", expanded=False):
                        st.write(row['announcement_content'])
            
            with col2:
                # D-Day 계산 및 표시
                dday = calculate_dday(row['application_period'])
                if dday is not None:
                    if dday > 0:
                        st.markdown(f"""
                        <div style="
                            background: #e8f5e8;
                            border: 1px solid #4caf50;
                            border-radius: 8px;
                            padding: 15px;
                            text-align: center;
                            margin-bottom: 10px;
                        ">
                            <div style="font-size: 18px; font-weight: bold; color: #2e7d32;">D-{dday}</div>
                            <div style="font-size: 12px; color: #4caf50;">일 남음</div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif dday == 0:
                        st.markdown(f"""
                        <div style="
                            background: #fff3e0;
                            border: 1px solid #ff9800;
                            border-radius: 8px;
                            padding: 15px;
                            text-align: center;
                            margin-bottom: 10px;
                        ">
                            <div style="font-size: 18px; font-weight: bold; color: #f57c00;">오늘 마감!</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="
                            background: #ffebee;
                            border: 1px solid #f44336;
                            border-radius: 8px;
                            padding: 15px;
                            text-align: center;
                            margin-bottom: 10px;
                        ">
                            <div style="font-size: 18px; font-weight: bold; color: #d32f2f;">D+{abs(dday)}</div>
                            <div style="font-size: 12px; color: #f44336;">일 지남</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # 공고 보기 버튼
                if pd.notna(row['url']) and row['url'].strip():
                    st.link_button("🔗 공고 보기", row['url'], use_container_width=True)
                else:
                    st.info("🔗 링크 없음")
            
            # 구분선
            st.markdown("---")

def render_roadmap(company_name: str):
    """로드맵 탭"""
    st.subheader("🗓️ 12개월 로드맵")
    
    # 추천 데이터 로드
    recommendations_df = load_recommendations(company_name)
    
    if recommendations_df.empty:
        st.info("해당 회사에 대한 로드맵 데이터가 없습니다.")
        return
    
    # 월별 로드맵 생성
    roadmap_data = []
    
    for idx, row in recommendations_df.iterrows():
        if pd.notna(row['application_period']):
            # 신청기간에서 시작 월 추출
            try:
                period_str = str(row['application_period']).strip()
                
                # 빈 문자열이나 '세부사업별 상이' 같은 텍스트는 건너뛰기
                if not period_str or period_str in ['', '세부사업별 상이', '-']:
                    continue
                
                # YYYYMMDD 형식 처리 (예: 20250801)
                if len(period_str) == 8 and period_str.isdigit():
                    year = int(period_str[:4])
                    month = int(period_str[4:6])
                    day = int(period_str[6:8])
                    start_date = datetime(year, month, day)
                # ~ 형식 처리 (예: 2025-08-01~2025-08-31)
                elif '~' in period_str:
                    start_date_str = period_str.split('~')[0].strip()
                    date_formats = ['%Y-%m-%d', '%Y.%m.%d', '%m/%d/%Y', '%d/%m/%Y', '%Y%m%d']
                    start_date = None
                    
                    for fmt in date_formats:
                        try:
                            start_date = datetime.strptime(start_date_str, fmt)
                            break
                        except ValueError:
                            continue
                else:
                    # 기타 형식 시도
                    date_formats = ['%Y-%m-%d', '%Y.%m.%d', '%m/%d/%Y', '%d/%m/%Y', '%Y%m%d']
                    start_date = None
                    
                    for fmt in date_formats:
                        try:
                            start_date = datetime.strptime(period_str, fmt)
                            break
                        except ValueError:
                            continue
                
                if start_date:
                    month = start_date.month
                    roadmap_data.append({
                        'month': month,
                        'title': row['announcement_title'],
                        'agency': row['agency'],
                        'score': row['score'],
                        'period': row['application_period'],
                        'url': row['url'],
                        'date': start_date
                    })
            except Exception as e:
                continue
    
    if not roadmap_data:
        st.info("로드맵을 생성할 수 있는 데이터가 없습니다.")
        return
    
    # 월별로 그룹화
    roadmap_df = pd.DataFrame(roadmap_data)
    monthly_roadmap = roadmap_df.groupby('month').apply(lambda x: x.sort_values('score', ascending=False).head(3)).reset_index(drop=True)
    
    # 월별 공고 수 시각화
    st.subheader("📊 월별 공고 수 현황")
    
    # 월별 공고 수 계산
    monthly_counts = roadmap_df['month'].value_counts().sort_index()
    
    # 1월부터 12월까지 모든 월 포함 (공고가 없는 월은 0으로)
    months_data = []
    for month in range(1, 13):
        count = monthly_counts.get(month, 0)
        months_data.append({
            'month': f'{month}월',
            'count': count
        })
    
    months_df = pd.DataFrame(months_data)
    
    # 막대 차트 생성
    chart = alt.Chart(months_df).mark_bar(
        color='#1f77b4',
        cornerRadius=4
    ).encode(
        x=alt.X('month:O', sort=None, title='월'),
        y=alt.Y('count:Q', title='공고 수'),
        tooltip=['month', 'count']
    ).properties(
        width=600,
        height=300
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # 통계 정보
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 공고 수", len(roadmap_df))
    with col2:
        st.metric("활성 월 수", len(monthly_counts))
    with col3:
        max_month = monthly_counts.idxmax() if not monthly_counts.empty else 0
        st.metric("가장 많은 월", f"{max_month}월" if max_month > 0 else "없음")
    
    st.divider()
    
    # 12개월 로드맵 표시
    st.subheader("📅 월별 상세 로드맵")
    months = ['1월', '2월', '3월', '4월', '5월', '6월', 
              '7월', '8월', '9월', '10월', '11월', '12월']
    
    cols = st.columns(4)
    
    for i, month in enumerate(months):
        with cols[i % 4]:
            st.subheader(f"📅 {month}")
            
            month_data = monthly_roadmap[monthly_roadmap['month'] == i + 1]
            
            if not month_data.empty:
                for _, item in month_data.iterrows():
                    with st.container():
                        score_display = int(item['score'] * 100)
                        st.write(f"**{item['title']}**")
                        st.write(f"🏢 기관: {item['agency']}")
                        st.write(f"⭐ 점수: {score_display}/100")
                        st.write(f"📅 기간: {item['period']}")
                        
                        if pd.notna(item['url']):
                            st.link_button("공고 보기", item['url'])
                        
                        st.divider()
            else:
                st.info("📭 해당 월에 추천 공고가 없습니다.")

def render_sidebar():
    """사이드바 렌더링"""
    st.sidebar.title("🏢 정부지원사업 맞춤 추천 시스템")
    
    # 회사 선택
    companies_df = load_companies()
    
    if companies_df.empty:
        st.sidebar.error("회사 데이터를 불러올 수 없습니다.")
        return
    
    st.sidebar.subheader("회사 선택")
    
    # 회사 목록 표시
    company_options = []
    for _, row in companies_df.iterrows():
        company_name = row.get('company_name', 'Unknown')
        description = row.get('description', '')
        company_options.append(f"{company_name} - {description}")
    
    selected_company = st.sidebar.selectbox(
        "회사를 선택하세요",
        company_options,
        key="company_selector"
    )
    
    if selected_company:
        # 선택된 회사 정보를 세션 상태에 저장
        company_name = selected_company.split(' - ')[0]
        company_info = companies_df[companies_df['company_name'] == company_name].iloc[0]
        st.session_state['selected_company'] = company_info.to_dict()
        st.session_state['selected_company_name'] = company_name

def main():
    """메인 함수"""
    st.set_page_config(
        page_title="정부지원사업 맞춤 추천 MVP",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🏛️ 정부지원사업 맞춤 추천 및 로드맵 생성 시스템")
    st.markdown("---")
    
    # 사이드바 렌더링
    render_sidebar()
    
    # 메인 컨텐츠
    if 'selected_company' in st.session_state:
        company = st.session_state['selected_company']
        company_name = st.session_state['selected_company_name']
        
        # 선택된 회사 헤더
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.subheader(f"🏢 {company_name}")
        with col2:
            st.metric("업종", company.get('industry', 'N/A'))
        with col3:
            st.metric("특화분야", company.get('specialization', 'N/A'))
        with col4:
            st.metric("지역", company.get('location', 'N/A'))
        
        # 탭 구성
        tab1, tab2, tab3 = st.tabs(["🎯 맞춤 추천", "🔔 신규 공고 알림", "🗓️ 12개월 로드맵"])
        
        with tab1:
            render_custom_recommendations(company_name)
        
        with tab2:
            render_new_announcement_alerts(company_name)
        
        with tab3:
            render_roadmap(company_name)
    else:
        st.info("👈 사이드바에서 회사를 선택해주세요.")

if __name__ == "__main__":
    main()
