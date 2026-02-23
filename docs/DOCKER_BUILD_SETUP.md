# Docker Build Setup Guide

회사 내부 환경에서 Docker 이미지를 빌드할 때 필요한 설정입니다.

## 문제

외부 오픈소스를 Docker 이미지로 빌드할 때 발생하는 문제들:
- ❌ 회사 내부 proxy를 통과할 수 없음
- ❌ SSL/TLS 인증서 검증 오류
- ❌ 회사 내부 Docker registry에 접근 불가
- ❌ 환경별(dev, qa, prod) 설정 차이

## 해결 방법

### 1. 환경별 Dockerfile 구분

```
docker/
├── Dockerfile-dev   # 개발 환경 (빠른 빌드)
├── Dockerfile-qa    # QA 환경 (테스트)
└── Dockerfile-prod  # 운영 환경 (최적화)
```

**각 환경별 특징**:
- **dev**: 빠른 빌드, 디버깅 가능, 테스트 도구 포함
- **qa**: 운영과 동일, 로그 상세 기록
- **prod**: 최소화, 보안 강화, 성능 최적화

### 2. Proxy 설정 (필수!)

Dockerfile에 다음을 추가:
```dockerfile
ENV HTTP_PROXY=http://12.26.204.100:8080 \
    HTTPS_PROXY=http://12.26.204.100:8080 \
    NO_PROXY=localhost,127.0.0.1/24,...,.samsungds.net
```

**주의**:
- Proxy IP/Port는 회사별로 다름
- NO_PROXY 설정: 내부 네트워크는 proxy 우회
- 환경에 따라 다를 수 있음 (IT 팀 확인)

### 3. CA 인증서 설정 (필수!)

```dockerfile
ADD ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
```

**필요한 파일**:
- `ca-certificates.crt`: 회사의 CA 인증서
- 프로젝트 루트에 위치해야 함

### 4. Docker Registry 설정

```dockerfile
# FROM repo.samsungds.net/docker.io/python:3.10-alpine
FROM <회사-내부-registry>/python:3.10-alpine
```

**변경 필요**:
- `repo.samsungds.net` → 회사 내부 registry
- 공개 이미지도 회사 내부 registry 사용 (proxy 우회)

### 5. uv 의존성 설치

```dockerfile
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv lock

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
```

**uv 특징**:
- Python 패키지 매니저 (pip보다 빠름)
- 회사 proxy 자동 감지
- CA 인증서 자동 사용

### 6. 빌드 명령어

```bash
# Dev 환경
docker build -f docker/Dockerfile-dev -t mcp-atlassian:dev .

# QA 환경
docker build -f docker/Dockerfile-qa -t repo.samsungds.net/mcp-atlassian:qa .

# Prod 환경
docker build -f docker/Dockerfile-prod -t repo.samsungds.net/mcp-atlassian:latest .
```

## 주의사항

### ⚠️ 필수 파일 확인

빌드 전 확인:
```bash
ls -la ca-certificates.crt   # 존재해야 함
ls -la pyproject.toml        # 존재해야 함
ls -la uv.lock               # 존재해야 함 (또는 자동 생성)
```

### ⚠️ Proxy 설정 확인

```bash
# 현재 proxy 설정 확인
echo $HTTP_PROXY
echo $HTTPS_PROXY

# Dockerfile의 proxy와 일치해야 함
```

### ⚠️ 빌드 실패 원인

| 오류 | 원인 | 해결 |
|------|------|------|
| `Certificate verify failed` | CA 인증서 없음 | `ca-certificates.crt` 확인 |
| `Connection refused` | Proxy 미설정 | Dockerfile proxy 설정 확인 |
| `image not found` | Registry 오류 | Registry URL 확인 |
| `ModuleNotFoundError` | 의존성 설치 실패 | uv lock 재생성 |

## 회사별 커스터마이징

새 환경에서 빌드할 때 변경해야 할 항목:

- [ ] Proxy IP/Port (IT 팀 문의)
- [ ] NO_PROXY 범위 (회사 네트워크 범위)
- [ ] Docker Registry URL (DevOps 팀 문의)
- [ ] CA 인증서 파일 위치
- [ ] Base Image 버전 (Python 3.10 외 필요시)
- [ ] Timezone (TZ 설정)

## 참고

- **Proxy 문제**: IT 팀에 회사 proxy 정보 문의
- **CA 인증서**: IT 팀에서 제공 받음
- **Docker Registry**: DevOps 팀에 registry URL 문의
- **uv 공식문서**: https://docs.astral.sh/uv/
