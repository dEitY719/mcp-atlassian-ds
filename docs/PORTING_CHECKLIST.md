# 외부 오픈소스 → 회사 내부 이식 체크리스트

> 새로운 오픈소스 프로젝트를 회사 환경으로 이식할 때 사용하는 표준 프로세스

---

## Phase 1: 초기 분석

- [ ] 원본 저장소 클론 및 구조 분석
- [ ] 핵심 기능 파악 (MVP vs 고급 기능)
- [ ] 외부 의존성 확인 (API, 서비스 등)
- [ ] 라이선스 확인

---

## Phase 2: 회사 환경 적응

### 🔐 인증 및 보안
- [ ] 회사 프록시 설정 확인
- [ ] 회사 인증 방식 적용 (PAT, OAuth 등)
- [ ] 민감한 설정 값을 `.env` 분리
- [ ] `.env.example` 작성

### ⚙️ 의존성 관리
- [ ] 외부 PyPI와 회사 내부 PyPI 호환성 확인
- [ ] `pyproject.toml` 및 `pyproject.external.toml` 작성
- [ ] 외부/내부 테스트 환경 분리

### 📝 프로젝트 설정
- [ ] 임시 주석/메모 제거
- [ ] 프로젝트 구조 정렬
- [ ] 불필요한 파일 정리

---

## Phase 3: 테스트 및 검증

### 외부 환경 테스트
```bash
make sync-external
make test-external
```
- [ ] 의존성 설치 성공
- [ ] 테스트 실행 (실패 예상)

### 회사 내부 환경 테스트
```bash
make sync
make test
```
- [ ] 의존성 설치 성공
- [ ] API KEY 설정 (필수!)
- [ ] 테스트 통과 확인

---

## Phase 4: 문서화

### 필수 문서
- [ ] **QUICKSTART_INTERNAL.md** - 5분 내 시작 가이드
- [ ] **.env.example** - 환경 변수 설정 예제
- [ ] **EXTERNAL_VS_INTERNAL.md** - 환경 차이 설명

### 권장 문서
- [ ] 회사 내부 설정 가이드 (프록시, 인증 등)
- [ ] 테스트 실패 시 해결 방법

---

## 🎯 개발자 경험 개선 포인트

### 자주 생기는 문제들
1. **API KEY 미설정** → QUICKSTART_INTERNAL.md에 명시
2. **외부/내부 환경 혼동** → EXTERNAL_VS_INTERNAL.md로 설명
3. **설정 값 실수** → `.env.example` 제공
4. **테스트 실패 원인 불명** → 체크리스트 제공

---

## ✅ 완료 기준

- [x] 코드 정리 완료
- [x] 외부 환경 테스트 통과
- [x] 회사 내부 환경 테스트 통과 (API KEY 설정 후)
- [x] 개발자 가이드 작성 완료
- [x] 모든 주석/메모 정리 완료

---

## 💡 팀원을 위한 팁

1. **첫 사용자를 위해**: QUICKSTART_INTERNAL.md부터 읽으세요
2. **테스트 실패 시**: EXTERNAL_VS_INTERNAL.md의 FAQ 섹션 참고
3. **설정 방법**: `.env.example`을 복사해서 `.env` 생성
4. **질문 있을 때**: PORTING_CHECKLIST.md의 "개발자 경험 개선 포인트" 참고
