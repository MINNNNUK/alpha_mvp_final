"""
Supabase 설정 관리
Streamlit Cloud 환경에 최적화된 설정
"""
import os
import streamlit as st

def get_supabase_config():
    """Supabase 설정 가져오기 (Streamlit Cloud 환경)"""
    # 환경변수에서 먼저 가져오기 (Streamlit Cloud에서 설정)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if url and key:
        return url, key
    
    try:
        # Streamlit Cloud의 secrets에서 가져오기
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return url, key
    except Exception as e:
        print(f"Streamlit secrets에서 설정을 가져올 수 없습니다: {e}")
        
        # 기본값 사용 (로컬 개발용)
        url = "https://uulghcpqnwgkukfyiypb.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1bGdoY3Bxbndna3VrZnlpeXBiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NzMxNTY5NywiZXhwIjoyMDcyODkxNjk3fQ.wCJi02hKCNiW-j9nhWyKq8J_WfRlBMi-8opFMfOnFvA"
        
        print("⚠️  Supabase 설정이 없습니다. 기본값을 사용합니다.")
        return url, key

# Supabase 설정 가져오기
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
