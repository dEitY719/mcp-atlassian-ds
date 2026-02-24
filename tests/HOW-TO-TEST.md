# 🧪 테스트 실행 가이드

## 🚀 외부 PC (추천)

```bash
# 1단계: 의존성 설치
make sync-external

# 2단계: Jira 테스트만 실행
make test-external-jira
```

**이게 끝!** ✨

---

## 💻 내부 PC (회사)

```bash
# 1단계: 의존성 설치
make sync-internal

# 2단계: 테스트 실행
make test
```

---

## 📊 테스트 결과

```
✅ 통과: 753개 (Jira 관련)
❌ 실패: 6개 (조사 중)
⚠️  에러: 32개 (API 관련)
⏭️  스킵: 462개 (Confluence는 추후 개발)
```

---

## 💡 참고

- **Confluence 테스트 스킵**: 자동으로 처리됨
- **모든 테스트**: `make test-external` (외부) / `make test` (내부)
- **더 자세한 로그**: `-vv` 추가 → `pytest tests/ -vv --skip-confluence`

---

## ❓ 문제가 생기면

```bash
# 환경 초기화 후 재시도
make sync-external
make test-external-jira
```
