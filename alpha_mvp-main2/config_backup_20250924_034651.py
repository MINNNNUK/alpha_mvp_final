"""
Supabase 설정 파일
"""
import os
from dotenv import load_dotenv

# .env 파일 로드 (로컬 개발용)
load_dotenv()

# Streamlit Cloud에서는 secrets를 사용, 로컬에서는 환경변수 사용
def get_supabase_config():
    # 로컬 개발 환경에서는 환경변수 사용
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    # 환경변수가 없으면 기본값 사용
    if not url or not key:
        url = "https://uulghcpqnwgkukfyiypb.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1bGdoY3Bxbndna3VreWZ5eXBiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUwNDQ4MjQsImV4cCI6MjA1MDYyMDgyNH0.Y4WU3jMl9cQqJqJqJqJqJqJqJqJqJqJqJqJqJqJqJq"
    
    return url, key

# Supabase 설정 가져오기
SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
