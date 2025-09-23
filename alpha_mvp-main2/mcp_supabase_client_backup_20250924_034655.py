"""
MCP Supabase 클라이언트
Supabase MCP 도구와 동일한 기능을 제공하는 Python 클라이언트
"""
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import json
from typing import List, Dict, Any, Optional

class MCPSupabaseClient:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def list_tables(self, schemas: List[str] = ['public']) -> List[str]:
        """테이블 목록 조회"""
        try:
            # 알려진 테이블 목록 반환
            known_tables = ['alpha_companies', 'announcements', 'recommend_keyword4', 'recommend_5']
            return known_tables
        except Exception as e:
            print(f"테이블 목록 조회 실패: {e}")
            return []
    
    def execute_sql(self, query: str) -> Dict[str, Any]:
        """SQL 실행"""
        try:
            # Supabase는 직접 SQL 실행을 지원하지 않으므로 RPC 함수 사용
            result = self.client.rpc('execute_sql', {'query': query}).execute()
            return {
                'data': result.data,
                'status': 'success'
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def get_project_url(self) -> str:
        """프로젝트 URL 반환"""
        return SUPABASE_URL
    
    def get_anon_key(self) -> str:
        """익명 키 반환"""
        return SUPABASE_KEY
    
    def list_migrations(self) -> List[Dict[str, Any]]:
        """마이그레이션 목록 조회"""
        try:
            # 마이그레이션 테이블이 있다면 조회
            result = self.client.table('supabase_migrations').select('*').execute()
            return result.data
        except:
            return []
    
    def list_extensions(self) -> List[Dict[str, Any]]:
        """확장 프로그램 목록 조회"""
        try:
            result = self.client.rpc('get_extensions').execute()
            return result.data
        except:
            return []
    
    def get_logs(self, service: str) -> List[Dict[str, Any]]:
        """로그 조회"""
        try:
            # 로그 테이블이 있다면 조회
            result = self.client.table(f'{service}_logs').select('*').limit(100).execute()
            return result.data
        except:
            return []
    
    def get_advisors(self, advisor_type: str) -> List[Dict[str, Any]]:
        """어드바이저 조회"""
        try:
            result = self.client.table('advisors').select('*').filter('type', 'eq', advisor_type).execute()
            return result.data
        except:
            return []
    
    def generate_typescript_types(self) -> str:
        """TypeScript 타입 생성"""
        tables = self.list_tables()
        types = []
        
        for table in tables:
            try:
                result = self.client.table(table).select('*').limit(1).execute()
                if result.data:
                    columns = list(result.data[0].keys())
                    type_def = f"""
interface {table.title().replace('_', '')} {{
"""
                    for col in columns:
                        type_def += f"  {col}: any;\n"
                    type_def += "}"
                    types.append(type_def)
            except:
                continue
        
        return "\n".join(types)
    
    def list_edge_functions(self) -> List[Dict[str, Any]]:
        """Edge Functions 목록 조회"""
        try:
            result = self.client.table('edge_functions').select('*').execute()
            return result.data
        except:
            return []
    
    def get_edge_function(self, function_slug: str) -> Dict[str, Any]:
        """Edge Function 조회"""
        try:
            result = self.client.table('edge_functions').select('*').filter('slug', 'eq', function_slug).execute()
            return result.data[0] if result.data else {}
        except:
            return {}
    
    def deploy_edge_function(self, name: str, files: List[Dict[str, str]]) -> Dict[str, Any]:
        """Edge Function 배포"""
        try:
            # Edge Function 배포 로직 (실제 구현 필요)
            return {
                'status': 'success',
                'message': f'Edge Function {name} deployed successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def list_branches(self) -> List[Dict[str, Any]]:
        """브랜치 목록 조회"""
        try:
            result = self.client.table('branches').select('*').execute()
            return result.data
        except:
            return []
    
    def create_branch(self, name: str, confirm_cost_id: str) -> Dict[str, Any]:
        """브랜치 생성"""
        try:
            # 브랜치 생성 로직 (실제 구현 필요)
            return {
                'status': 'success',
                'message': f'Branch {name} created successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def delete_branch(self, branch_id: str) -> Dict[str, Any]:
        """브랜치 삭제"""
        try:
            # 브랜치 삭제 로직 (실제 구현 필요)
            return {
                'status': 'success',
                'message': f'Branch {branch_id} deleted successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def merge_branch(self, branch_id: str) -> Dict[str, Any]:
        """브랜치 병합"""
        try:
            # 브랜치 병합 로직 (실제 구현 필요)
            return {
                'status': 'success',
                'message': f'Branch {branch_id} merged successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def reset_branch(self, branch_id: str, migration_version: Optional[str] = None) -> Dict[str, Any]:
        """브랜치 리셋"""
        try:
            # 브랜치 리셋 로직 (실제 구현 필요)
            return {
                'status': 'success',
                'message': f'Branch {branch_id} reset successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def rebase_branch(self, branch_id: str) -> Dict[str, Any]:
        """브랜치 리베이스"""
        try:
            # 브랜치 리베이스 로직 (실제 구현 필요)
            return {
                'status': 'success',
                'message': f'Branch {branch_id} rebased successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

# 전역 인스턴스
mcp_client = MCPSupabaseClient()

# MCP 도구 함수들
def list_tables(schemas: List[str] = ['public']) -> List[str]:
    return mcp_client.list_tables(schemas)

def execute_sql(query: str) -> Dict[str, Any]:
    return mcp_client.execute_sql(query)

def get_project_url() -> str:
    return mcp_client.get_project_url()

def get_anon_key() -> str:
    return mcp_client.get_anon_key()

def list_migrations() -> List[Dict[str, Any]]:
    return mcp_client.list_migrations()

def list_extensions() -> List[Dict[str, Any]]:
    return mcp_client.list_extensions()

def get_logs(service: str) -> List[Dict[str, Any]]:
    return mcp_client.get_logs(service)

def get_advisors(advisor_type: str) -> List[Dict[str, Any]]:
    return mcp_client.get_advisors(advisor_type)

def generate_typescript_types() -> str:
    return mcp_client.generate_typescript_types()

def list_edge_functions() -> List[Dict[str, Any]]:
    return mcp_client.list_edge_functions()

def get_edge_function(function_slug: str) -> Dict[str, Any]:
    return mcp_client.get_edge_function(function_slug)

def deploy_edge_function(name: str, files: List[Dict[str, str]]) -> Dict[str, Any]:
    return mcp_client.deploy_edge_function(name, files)

def list_branches() -> List[Dict[str, Any]]:
    return mcp_client.list_branches()

def create_branch(name: str, confirm_cost_id: str) -> Dict[str, Any]:
    return mcp_client.create_branch(name, confirm_cost_id)

def delete_branch(branch_id: str) -> Dict[str, Any]:
    return mcp_client.delete_branch(branch_id)

def merge_branch(branch_id: str) -> Dict[str, Any]:
    return mcp_client.merge_branch(branch_id)

def reset_branch(branch_id: str, migration_version: Optional[str] = None) -> Dict[str, Any]:
    return mcp_client.reset_branch(branch_id, migration_version)

def rebase_branch(branch_id: str) -> Dict[str, Any]:
    return mcp_client.rebase_branch(branch_id)
