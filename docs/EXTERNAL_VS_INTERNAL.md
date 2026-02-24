# 외부 환경 vs 회사 내부 환경

## 🔄 테스트 환경의 차이

| 항목 | 외부 환경 | 회사 내부 |
|------|---------|---------|
| **의존성 설치** | Public PyPI 사용 | 같음 |
| **JIRA 접근** | Mock/Dummy 데이터 | 실제 회사 JIRA 필요 |
| **인증** | 테스트용 토큰 | **개인 PAT 토큰 필수** |
| **테스트 실패** | 허용 (mock 부재) | ❌ 불가능 (API KEY 확인) |

---

## 📊 테스트 실패 패턴

### 외부 환경에서 실패하는 이유
```
❌ Mock JIRA 서버 없음
→ 15개 테스트가 Connection 오류로 실패 (예상된 동작)
```

### 회사 내부 환경에서 실패하는 이유
```
❌ .env에 JIRA_API_KEY 미설정
→ 같은 15개 테스트가 401 Unauthorized로 실패 (설정 문제)
```

---

## ✅ 회사 내부 환경 검증

**의존성 설치 성공:**
```bash
make sync  # ✅ 모든 패키지 설치됨
```

**API KEY 설정 확인:**
```bash
# 1. .env 파일이 존재하는가?
test -f .env && echo "✅ .env 파일 있음" || echo "❌ .env 파일 없음"

# 2. JIRA_API_KEY가 설정되었는가?
grep "JIRA_API_KEY=" .env | grep -v "^#"
```

**테스트 실행:**
```bash
make test  # API KEY 설정 후 실행하면 15개 모두 PASS
```

---

## 💬 FAQ

**Q: 외부와 회사 내부에서 같은 15개 실패가 나는데, 차이가 뭔가요?**
- **외부**: Mock 서버 없어서 Connection 실패 (정상)
- **회사**: API KEY 미설정으로 인증 실패 (조치 필요)

**Q: 테스트를 통과하려면?**
1. `.env` 파일 생성
2. 개인 JIRA PAT 토큰 발급
3. `JIRA_API_KEY=<토큰>` 추가
4. `make test` 다시 실행
