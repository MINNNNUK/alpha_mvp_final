#!/bin/bash

# 정부지원사업 맞춤 추천 MVP 백업 복원 스크립트
# 생성일: 2025-09-24 03:46:48

echo "🔄 정부지원사업 맞춤 추천 MVP 백업 복원을 시작합니다..."

# 백업 디렉토리 확인
BACKUP_DIR="/Users/minkim/git_test/kpmg-2025/alpha_mvp-main2"
TARGET_DIR="/Users/minkim/git_test/kpmg-2025/alpha_mvp-main"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ 백업 디렉토리를 찾을 수 없습니다: $BACKUP_DIR"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ 대상 디렉토리를 찾을 수 없습니다: $TARGET_DIR"
    exit 1
fi

echo "📁 백업 디렉토리: $BACKUP_DIR"
echo "📁 대상 디렉토리: $TARGET_DIR"

# 파일 복원
echo ""
echo "📋 파일 복원 중..."

# 1. 메인 MVP 애플리케이션
if [ -f "$BACKUP_DIR/app_mvp_backup_20250924_034648.py" ]; then
    cp "$BACKUP_DIR/app_mvp_backup_20250924_034648.py" "$TARGET_DIR/app_mvp.py"
    echo "✅ app_mvp.py 복원 완료"
else
    echo "⚠️  app_mvp_backup_20250924_034648.py 파일을 찾을 수 없습니다"
fi

# 2. Supabase 설정 파일
if [ -f "$BACKUP_DIR/config_backup_20250924_034651.py" ]; then
    cp "$BACKUP_DIR/config_backup_20250924_034651.py" "$TARGET_DIR/config.py"
    echo "✅ config.py 복원 완료"
else
    echo "⚠️  config_backup_20250924_034651.py 파일을 찾을 수 없습니다"
fi

# 3. MCP Supabase 클라이언트
if [ -f "$BACKUP_DIR/mcp_supabase_client_backup_20250924_034655.py" ]; then
    cp "$BACKUP_DIR/mcp_supabase_client_backup_20250924_034655.py" "$TARGET_DIR/mcp_supabase_client.py"
    echo "✅ mcp_supabase_client.py 복원 완료"
else
    echo "⚠️  mcp_supabase_client_backup_20250924_034655.py 파일을 찾을 수 없습니다"
fi

# 4. MCP 도구 테스트
if [ -f "$BACKUP_DIR/test_mcp_tools_backup_20250924_034702.py" ]; then
    cp "$BACKUP_DIR/test_mcp_tools_backup_20250924_034702.py" "$TARGET_DIR/test_mcp_tools.py"
    echo "✅ test_mcp_tools.py 복원 완료"
else
    echo "⚠️  test_mcp_tools_backup_20250924_034702.py 파일을 찾을 수 없습니다"
fi

# 5. MVP 문서
if [ -f "$BACKUP_DIR/README_MVP_backup_20250924_034707.md" ]; then
    cp "$BACKUP_DIR/README_MVP_backup_20250924_034707.md" "$TARGET_DIR/README_MVP.md"
    echo "✅ README_MVP.md 복원 완료"
else
    echo "⚠️  README_MVP_backup_20250924_034707.md 파일을 찾을 수 없습니다"
fi

echo ""
echo "🎉 백업 복원이 완료되었습니다!"
echo ""
echo "📋 복원된 파일들:"
echo "  - app_mvp.py (개선된 UI/UX가 적용된 메인 애플리케이션)"
echo "  - config.py (Supabase 연결 설정)"
echo "  - mcp_supabase_client.py (MCP 도구용 클라이언트)"
echo "  - test_mcp_tools.py (MCP 도구 테스트)"
echo "  - README_MVP.md (사용법 문서)"
echo ""
echo "🚀 실행 방법:"
echo "  cd $TARGET_DIR"
echo "  streamlit run app_mvp.py"
echo ""
echo "🌐 접속 URL: http://localhost:8501"
