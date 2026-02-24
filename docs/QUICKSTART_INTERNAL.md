# 회사 내부 환경 빠른 시작 가이드

## ⚡ 5분 내에 테스트 실행하기

### 1단계: API KEY 설정 (필수!)

```bash
# .env 파일 생성
cp .env.example .env

# 편집기에서 .env 열기
# 다음 항목을 회사 JIRA 정보로 채우기:
# - JIRA_URL: https://your-jira-instance.com
# - JIRA_API_KEY: 개인 PAT 토큰
```

**PAT 발급 방법:**
1. JIRA → 프로필 → 개인용 액세스 토큰 → 토큰 만들기
2. 토큰 이름 입력 → 자동 만료 해제 → 만들기 → 복사

### 2단계: 의존성 설치

```bash
make sync
```

### 3단계: 테스트 실행

```bash
make test
```

---

## 🚨 흔한 실패 원인

| 증상 | 원인 | 해결책 |
|------|------|--------|
| 15개 테스트 실패 | API KEY 미설정 | `.env` 파일에 `JIRA_API_KEY` 설정 |
| Connection 오류 | JIRA URL 오류 | `.env`에서 JIRA_URL 확인 |
| 401 Unauthorized | 토큰 만료/유효하지 않음 | 새로운 PAT 토큰 발급 |

---

## 📝 환경 변수 체크리스트

```bash
# 설정 확인 (민감정보는 출력 안 함)
grep -E "JIRA_URL|JIRA_API_KEY" .env
```

최소 필수 변수:
- ✅ `JIRA_URL`: 회사 JIRA 인스턴스 URL
- ✅ `JIRA_API_KEY`: 개인 PAT 토큰

---

## 💡 팁

- 토큰은 **절대 git에 커밋하지 말 것** (.env는 .gitignore에 등록됨)
- 팀원과 토큰 공유 금지 → 각자 개인 토큰 발급
- 테스트 실패 시 먼저 `.env` 파일부터 확인
