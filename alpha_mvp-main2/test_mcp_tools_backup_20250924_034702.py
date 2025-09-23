#!/usr/bin/env python3
"""
MCP Supabase 도구 테스트 스크립트
"""
from mcp_supabase_client import *
import json

def test_mcp_tools():
    """MCP 도구들을 테스트합니다."""
    print("🔧 MCP Supabase 도구 테스트 시작")
    print("=" * 50)
    
    # 1. 프로젝트 정보 조회
    print("\n1️⃣ 프로젝트 정보:")
    url = get_project_url()
    key = get_anon_key()
    print(f"   URL: {url}")
    print(f"   Key: {key[:20]}...")
    
    # 2. 테이블 목록 조회
    print("\n2️⃣ 테이블 목록:")
    tables = list_tables()
    for i, table in enumerate(tables, 1):
        print(f"   {i}. {table}")
    
    # 3. 마이그레이션 목록 조회
    print("\n3️⃣ 마이그레이션 목록:")
    migrations = list_migrations()
    if migrations:
        for migration in migrations:
            print(f"   - {migration}")
    else:
        print("   마이그레이션 정보 없음")
    
    # 4. 확장 프로그램 목록 조회
    print("\n4️⃣ 확장 프로그램 목록:")
    extensions = list_extensions()
    if extensions:
        for ext in extensions:
            print(f"   - {ext}")
    else:
        print("   확장 프로그램 정보 없음")
    
    # 5. 로그 조회 (API 서비스)
    print("\n5️⃣ API 로그 조회:")
    logs = get_logs('api')
    if logs:
        print(f"   {len(logs)}개의 로그 항목")
        for log in logs[:3]:  # 처음 3개만 표시
            print(f"   - {log}")
    else:
        print("   로그 정보 없음")
    
    # 6. 어드바이저 조회 (보안)
    print("\n6️⃣ 보안 어드바이저 조회:")
    security_advisors = get_advisors('security')
    if security_advisors:
        for advisor in security_advisors:
            print(f"   - {advisor}")
    else:
        print("   보안 어드바이저 정보 없음")
    
    # 7. TypeScript 타입 생성
    print("\n7️⃣ TypeScript 타입 생성:")
    types = generate_typescript_types()
    print("   TypeScript 타입이 생성되었습니다.")
    print(f"   총 {len(types.split('interface')) - 1}개의 인터페이스")
    
    # 8. Edge Functions 목록 조회
    print("\n8️⃣ Edge Functions 목록:")
    functions = list_edge_functions()
    if functions:
        for func in functions:
            print(f"   - {func}")
    else:
        print("   Edge Functions 없음")
    
    # 9. 브랜치 목록 조회
    print("\n9️⃣ 브랜치 목록:")
    branches = list_branches()
    if branches:
        for branch in branches:
            print(f"   - {branch}")
    else:
        print("   브랜치 정보 없음")
    
    print("\n✅ MCP 도구 테스트 완료!")
    print("=" * 50)

if __name__ == "__main__":
    test_mcp_tools()
