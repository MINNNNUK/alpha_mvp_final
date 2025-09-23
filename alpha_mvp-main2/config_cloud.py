"""
Supabase 설정 관리
Streamlit Cloud 환경에 최적화된 설정
"""
import os
import streamlit as st

def get_supabase_config():
    """Supabase 설정 가져오기 (Streamlit Cloud 환경)"""
    try:
        # Streamlit Cloud의 secrets에서 가져오기
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return url, key
    except Exception as e:
        print(f"Streamlit secrets에서 설정을 가져올 수 없습니다: {e}")
        
        # 환경변수에서 가져오기 (로컬 개발용)
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if url and key:
            return url, key
        
        # 기본값 사용 (실제 프로젝트에서는 환경변수 설정 필요)
        url = "https://uulghcpqnwgkukfyiypb.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1bGdoY3Bxbndna3VreWZ5eXBiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUwNDQ4MjQsImV4cCI6MjA1MDYyMDgyNH0.Y4WU3jMl9cQqJqJqJqJqJqJqJqJqJqJqJqJqJqJqJq"
        
        print("⚠️  Supabase 설정이 없습니다. 기본값을 사용합니다.")
        return url, key

# Supabase 설정 가져오기
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
