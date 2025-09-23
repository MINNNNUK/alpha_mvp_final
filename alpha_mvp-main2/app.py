"""
정부지원사업 맞춤 추천 MVP
Streamlit Cloud 배포용 메인 애플리케이션
"""
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
from supabase import create_client
from config_cloud import SUPABASE_URL, SUPABASE_KEY

# 페이지 설정
st.set_page_config(
    page_title="정부지원사업 맞춤 추천 MVP",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def init_supabase():
    """Supabase 클라이언트 초기화"""
    try:
        if not SUPABASE_URL or not SUPABASE_KEY:
            st.error("❌ Supabase 설정이 없습니다. config_cloud.py 파일을 확인해주세요.")
            st.stop()
        
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"❌ Supabase 연결 실패: {e}")
        st.error("Supabase 설정을 확인하고 다시 시도해주세요.")
        st.stop()

def calculate_dday(application_period):
    """D-Day 계산"""
    if pd.isna(application_period) or not application_period:
        return None
    
    try:
        period_str = str(application_period).strip()
        if not period_str or period_str in ['', '세부사업별 상이', '-']:
            return None
        
        # YYYYMMDD 형식 처리
        if len(period_str) == 8 and period_str.isdigit():
            year = int(period_str[:4])
            month = int(period_str[4:6])
            day = int(period_str[6:8])
            end_date = datetime(year, month, day)
        elif '~' in period_str:
            end_date_str = period_str.split('~')[1].strip()
            date_formats = ['%Y-%m-%d', '%Y.%m.%d', '%m/%d/%Y', '%d/%m/%Y', '%Y%m%d']
            end_date = None
            for fmt in date_formats:
                try:
                    end_date = datetime.strptime(end_date_str, fmt)
                    break
                except ValueError:
                    continue
        else:
            date_formats = ['%Y-%m-%d', '%Y.%m.%d', '%m/%d/%Y', '%d/%m/%Y', '%Y%m%d']
            end_date = None
            for fmt in date_formats:
                try:
                    end_date = datetime.strptime(period_str, fmt)
                    break
                except ValueError:
                    continue
        
        if end_date:
            today = datetime.now()
            delta = end_date - today
            return delta.days
    except Exception:
        pass
    
    return None

def load_company_data():
    """회사 데이터 로드"""
    try:
        supabase = init_supabase()
        result = supabase.table('alpha_companies3').select('*').execute()
        df = pd.DataFrame(result.data)
        # 컬럼명 매핑 (기업명 -> 회사명)
        if '기업명' in df.columns:
            df = df.rename(columns={'기업명': '회사명'})
        return df
    except Exception as e:
        st.error(f"회사 데이터 로드 실패: {e}")
        return pd.DataFrame()

def load_recommendations(company_name):
    """추천 데이터 로드"""
    try:
        supabase = init_supabase()
        result = supabase.table('recommend_5').select('*').eq('회사명', company_name).execute()
        return pd.DataFrame(result.data)
    except Exception as e:
        st.error(f"추천 데이터 로드 실패: {e}")
        return pd.DataFrame()

def render_custom_recommendations(company_name: str):
    """맞춤 추천 탭"""
    st.subheader("🎯 맞춤 추천")
    
    # 추천 데이터 로드
    recommendations_df = load_recommendations(company_name)
    
    if recommendations_df.empty:
        st.info("해당 회사에 대한 추천 데이터가 없습니다.")
        return
    
    # 컬럼명 매핑
    column_mapping = {
        '공고명': 'announcement_title',
        '공고_기관': 'agency',
        '공고_지역': 'region',
        '공고_지원분야': 'support_field',
        '공고_신청기간': 'application_period',
        '공고_내용': 'announcement_content',
        '추천_이유': 'reason',
        '공고_URL': 'url',
        '추천_점수': 'score',
        '생성_시간': 'created_at'
    }
    
    recommendations_df = recommendations_df.rename(columns=column_mapping)
    
    # 필터링 옵션
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # 점수 필터 (0-1 범위를 0-100으로 변환)
        min_score = st.slider("최소 추천 점수", 0, 100, 30)
        min_score_normalized = min_score / 100  # 0-100을 0-1로 정규화
        filtered_df = recommendations_df[recommendations_df['score'] >= min_score_normalized]
    
    with col2:
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
    
    # 컬럼명 매핑
    column_mapping = {
        '공고명': 'announcement_title',
        '공고_기관': 'agency',
        '공고_지역': 'region',
        '공고_지원분야': 'support_field',
        '공고_신청기간': 'application_period',
        '공고_내용': 'announcement_content',
        '추천_이유': 'reason',
        '공고_URL': 'url',
        '추천_점수': 'score',
        '생성_시간': 'created_at'
    }
    
    recommendations_df = recommendations_df.rename(columns=column_mapping)
    
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
        st.info("해당 회사에 대한 공고 데이터가 없습니다.")
        return
    
    # 컬럼명 매핑
    column_mapping = {
        '공고명': 'announcement_title',
        '공고_기관': 'agency',
        '공고_지역': 'region',
        '공고_지원분야': 'support_field',
        '공고_신청기간': 'application_period',
        '공고_내용': 'announcement_content',
        '추천_이유': 'reason',
        '공고_URL': 'url',
        '추천_점수': 'score',
        '생성_시간': 'created_at'
    }
    
    recommendations_df = recommendations_df.rename(columns=column_mapping)
    
    # 로드맵 데이터 생성
    roadmap_data = []
    
    for idx, row in recommendations_df.iterrows():
        if pd.notna(row['application_period']):
            try:
                period_str = str(row['application_period']).strip()
                if not period_str or period_str in ['', '세부사업별 상이', '-']:
                    continue
                
                if len(period_str) == 8 and period_str.isdigit():
                    year = int(period_str[:4])
                    month = int(period_str[4:6])
                    day = int(period_str[6:8])
                    start_date = datetime(year, month, day)
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
    
    roadmap_df = pd.DataFrame(roadmap_data)
    
    # 월별 공고 수 현황
    st.subheader("📊 월별 공고 수 현황")
    monthly_counts = roadmap_df['month'].value_counts().sort_index()
    months_data = []
    for month in range(1, 13):
        count = monthly_counts.get(month, 0)
        months_data.append({'month': f'{month}월', 'count': count})
    months_df = pd.DataFrame(months_data)
    
    chart = alt.Chart(months_df).mark_bar(
        color='#1f77b4', cornerRadius=4
    ).encode(
        x=alt.X('month:O', sort=None, title='월'),
        y=alt.Y('count:Q', title='공고 수'),
        tooltip=['month', 'count']
    ).properties(width=600, height=300)
    
    st.altair_chart(chart, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 공고 수", len(roadmap_df))
    with col2:
        st.metric("활성 월 수", len(monthly_counts))
    with col3:
        max_month = monthly_counts.idxmax() if not monthly_counts.empty else 0
        st.metric("가장 많은 월", f"{max_month}월" if max_month > 0 else "없음")
    
    st.divider()
    
    # 월별 상세 로드맵
    st.subheader("📅 월별 상세 로드맵")
    
    # 월별로 그룹화하여 상위 3개씩 표시
    monthly_roadmap = roadmap_df.groupby('month').apply(lambda x: x.sort_values('score', ascending=False).head(3)).reset_index(drop=True)
    
    for month in range(1, 13):
        month_data = monthly_roadmap[monthly_roadmap['month'] == month]
        
        if not month_data.empty:
            st.subheader(f"📅 {month}월")
            
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
            st.info(f"📭 {month}월에 추천 공고가 없습니다.")

def main():
    """메인 함수"""
    # 헤더
    st.title("🏛️ 정부지원사업 맞춤 추천 MVP")
    st.markdown("정부지원사업과 초기 스타트업 자금조달을 위한 맞춤 추천 및 로드맵 생성 시스템")
    
    # 회사 선택
    companies_df = load_company_data()
    
    if companies_df.empty:
        st.error("회사 데이터를 불러올 수 없습니다.")
        return
    
    company_names = companies_df['회사명'].unique().tolist()
    company_name = st.selectbox("회사를 선택하세요", company_names)
    
    if not company_name:
        st.warning("회사를 선택해주세요.")
        return
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🎯 맞춤 추천", "🔔 신규 공고 알림", "🗓️ 12개월 로드맵"])
    
    with tab1:
        render_custom_recommendations(company_name)
    
    with tab2:
        render_new_announcement_alerts(company_name)
    
    with tab3:
        render_roadmap(company_name)

if __name__ == "__main__":
    main()
