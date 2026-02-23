# SSL Certificate Setup for Development

회사 내부 proxy를 통해 Python 패키지를 설치할 때 필요한 SSL 인증서 설정 가이드입니다.

## 문제

외부 환경에서 회사 내부 시스템(JFrog Artifactory 등)에 접근할 때 SSL 인증서 검증 오류 발생:
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

## 해결 방법

### 1. 회사 CA 인증서 다운로드

IT 팀에서 제공하는 CA 인증서 파일을 프로젝트 루트에 저장:
```bash
# 예: ca-certificates.crt 또는 company-ca.crt
```

### 2. 환경 변수 설정

Python 및 pip가 CA 인증서를 사용하도록 설정:

```bash
# .env 파일에 추가
export REQUESTS_CA_BUNDLE=/path/to/ca-certificates.crt
export CURL_CA_BUNDLE=/path/to/ca-certificates.crt
```

### 3. uv 패키지 매니저 설정

`pyproject.toml` 또는 `~/.config/uv/uv.toml`에 인증서 경로 추가:
```toml
[tool.uv]
index-url = "https://repo.samsungds.net/artifactory/api/pypi/pypi-remote/simple"
# CA 인증서는 환경 변수로 관리 (파일 경로에 저장하지 않음)
```

## 주의사항

- ⚠️ **ca-certificates.crt는 git에 포함되지 않음** (.gitignore 제외)
- ⚠️ **각 개발자가 로컬에서 설정해야 함** (공용 저장소에서 제외)
- ⚠️ **민감한 정보 취급** - 회사 내부에서만 사용

## 트러블슈팅

**문제**: `make sync-internal` 또는 `uv sync` 실패
```
error: Could not find a version that matches ...
```

**해결책**:
1. CA 인증서 경로 확인: `echo $REQUESTS_CA_BUNDLE`
2. 환경 변수 재설정: `source .env`
3. 회사 내부 네트워크 연결 확인 (VPN 필요할 수 있음)

## 참고

- 각 개발자마다 다른 인증서 파일명일 수 있음 (회사 IT 정책에 따름)
- 외부 환경에서는 공개 PyPI를 사용하면 인증서 불필요 (`make sync-external`)
