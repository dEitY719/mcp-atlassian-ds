# Next Steps - External Environment Testing

## 목표
외부 환경(공개 PyPI)에서 mcp-company 테스트 환경 동작 검증

---

## 월요일 (2026-02-23) 실행 계획

### Phase 1: 의존성 설치
```bash
cd /home/bwyoon/para/project/diff-mcp/mcp-company/
make sync-external
```

**목표:** 모든 패키지가 공개 PyPI에서 정상 설치되는지 확인

**예상 결과:**
- ✅ 가상 환경 생성
- ✅ 모든 의존성 설치 완료
- ✅ .venv 디렉토리 생성

**실패 시 조치:**
- requirements.external.txt 생성 필요 (수동으로)
- 또는 다른 설치 방법 검토

---

### Phase 2: 테스트 실행
```bash
make test-external
```

**목표:** pytest가 외부 환경에서 정상 동작하는지 확인

**예상 결과:**
- ✅ 테스트 수집 성공 (현재는 ModuleNotFoundError)
- ✅ 테스트 실행 성공
- ✅ 적절한 통과/실패 결과

**체크포인트:**
- [ ] 3 items 이상 collected
- [ ] 테스트 케이스 실행 시작
- [ ] 결과 리포트 생성

---

## 진행 중 발견 사항 기록

### 현재까지의 학습
1. **환경 분리 구조**
   - 내부: `pyproject.toml` (Artifactory)
   - 외부: `pyproject.external.toml` (공개 PyPI)

2. **빌드 시스템 이슈**
   - `uv-dynamic-versioning`은 Samsung DS Artifactory에서만 제공
   - 공개 PyPI에는 없음
   - build-system.requires 때문에 충돌

3. **해결책**
   - requirements.txt 기반 설치 준비
   - 원본 pyproject.toml은 보호됨

---

## 파일 참고
- `Makefile` - 환경별 명령어 정의
- `pyproject.external.toml` - 외부용 설정 (현재 미사용)
- `requirements.external.txt` - 다음에 생성 예정

---

## 월요일 이후 다음 단계

### Phase 3: 요구사항 충족 확인
- [ ] 외부 환경에서 모든 테스트 통과
- [ ] CI/CD 준비 (필요시)

### Phase 4: 문서 최종화
- [ ] EXTERNAL_ENVIRONMENT.md 작성
- [ ] 개발자 가이드 업데이트

---

## 참고
- 현재 commit: 4ac5048
- 총 33 commits 완료 (Phase 8A')
- 원본 코드는 100% 보호됨
