from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta


app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_token(user_id: str) -> str:
    """JWT 토큰 생성"""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """토큰 검증"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")


# 인증 필요 엔드포인트
@app.post("/query")
async def query(request: QueryRequest, user_id: str = Depends(verify_token)):
    """인증된 사용자만 질의 가능"""
    return rag_service.query(request.question, request.k)


# API 키 방식
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")
VALID_API_KEYS = {"key1", "key2"}


def verify_api_key(api_key: str = Security(api_key_header)):
    """API 키 검증"""
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key


@app.post("/query-with-key")
async def query_with_key(request: QueryRequest, api_key: str = Depends(verify_api_key)):
    """API 키 인증"""
    return rag_service.query(request.question, request.k)
