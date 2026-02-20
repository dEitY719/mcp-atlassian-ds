# Phase 8A': mcp-company 수작업 이식 작업 로그

## 작업 개요

**목표**: 회사 내부 Jira/Confluence 관련 코드(mcp-company) 를 외부 오픈소스(mcp-atlassian) 기반으로 변환 및 최적화

**기간**: 2026-02-20 ~
**방식**: 수작업 코드 분석 + AI 커밋 작성 (Conventional Commits 규칙 준수)
**상태**: 🔄 진행 중 (Phase 8A')

---

## 디렉토리 구조

```
/home/bwyoon/para/project/diff-mcp/
├── mcp-atlassian/          ← readonly (참고용, chmod 555)
│   └── [upstream 원본 코드]
└── mcp-company/            ← 현재 작업 중 (수정/삭제)
    ├── src/mcp_atlassian/  ← 이식 중인 코드
    ├── .env.example        ← 회사 설정 예제
    └── docs/               ← 작업 내용 문서화
        ├── INTERNAL_SETUP.md
        ├── PROXY_AND_AUTHENTICATION.md
        ├── AUTHENTICATION_PRIORITY.md
        ├── FEATURE_SCOPE.md
        ├── CONFLUENCE_MODULE_CHANGES.md
        ├── commit-msg-rules.sh
        └── PHASE8A_WORKLOG.md (이 파일)
```

---

## 작업 방식 (Daily Workflow)

### 1️⃣ 변경사항 확인 & 분석
```bash
git status                    # 변경된 파일 확인
git diff [file]              # 상세 내용 검토
```

### 2️⃣ 커밋 작성 (Conventional Commits)
- **Format**: `type(scope): description`
- **Types**: feat, fix, docs, style, refactor, perf, test, chore
- **Body**: 변경 이유 + 영향 + 설계 철학
- **Guide**: `docs/commit-msg-rules.sh` 참고

### 3️⃣ 필요시 문서 작성
- **위치**: `docs/` 아래
- **길이**: 짧고 핵심만 (개발자가 빠르게 읽을 수 있게)
- **대상**: 설정, 인증, API 변경 등 팀이 알아야 할 내용

### 4️⃣ 다음날 재개 시
1. `git log --oneline | head -20` → 진행 상황 파악
2. `PHASE8A_WORKLOG.md` 읽기 → 작업 맥락 이해
3. 관련 docs 파일 읽기 → 팀의 변경사항 파악
4. 새로운 변경사항부터 시작

---

## 지금까지의 작업 (2026-02-20)

### ✅ Commit History (총 16개)

```
1. 78f8f45 docs: add Conventional Commits rule definition and validation
2. 0161cf2 chore: simplify project structure (remove dev/CI config)
3. a360c67 refactor: remove advanced analytics and SLA tracking features
4. ecd548f docs: add .env.example for configuration onboarding
5. f3f42d0 chore: configure internal dependency management via JFrog Artifactory
6. 6048301 docs: add internal setup guide for Samsung DS environment
7. 3349dfe refactor: remove client certificate configuration from Confluence
8. 43f10d6 docs: add proxy and authentication architecture guide
9. fb23ff5 refactor: simplify Confluence authentication config
10. 8e215cf docs: add authentication priority guide for Jira/Confluence
11. 84c0880 refactor: remove page emoji and folder features from Confluence
12. 7c88d29 docs: add feature scope guide (what's included and what's not)
13. 81d8c73 refactor: remove emoji utility functions from Confluence utils
14. f157584 docs: add Confluence module changes migration guide
15. bd36c90 refactor: remove emoji and analytics features from Confluence v2 adapter
16. 9160978 docs: update Confluence changes guide to include v2 adapter removals
```

### 📊 코드 변경 통계

| 항목 | 내용 |
|------|------|
| **파일 삭제** | 31개 (dev/CI/doc 관련) |
| **코드 제거** | 476줄 (advanced features) |
| **문서 추가** | 6개 (.md 파일) |
| **환경설정** | JFrog Artifactory 설정 추가 |
| **API 변경** | emoji, folder, analytics 제거 |

### 🔑 주요 변경사항

#### 1. 프로젝트 구조 단순화
- DevContainer, GitHub Actions, Docker 제거
- README, CONTRIBUTING 제거 (내부 운영용 문서 유지)

#### 2. 의존성 정리
- advanced analytics/metrics/SLA 기능 제거 (~3,463줄)
- fastmcp, starlette 버전 다운그레이드 (내부 호환성)
- JFrog Artifactory 설정 (프록시 표준화)

#### 3. 인증 단순화
- 클라이언트 인증서 제거 (프록시 레벨에서 관리)
- OAuth 글로벌 우선순위 통합 (Cloud/Server 구분 제거)

#### 4. Confluence API 축소
- Page emoji 기능 제거 (v1/v2 모두)
- Folder 계층 제거 (Spaces 사용)
- Page views (analytics) 제거
- Content properties 관리 제거

#### 5. 문서화 (팀용)
- INTERNAL_SETUP.md → JFrog 설정 가이드
- PROXY_AND_AUTHENTICATION.md → 인증서 제거 설명
- AUTHENTICATION_PRIORITY.md → 우선순위 명확화
- FEATURE_SCOPE.md → 지원/미지원 기능
- CONFLUENCE_MODULE_CHANGES.md → Breaking changes 가이드
- commit-msg-rules.sh → 팀 커밋 규칙

---

## 설계 철학 (MVP 전략)

```
Core Operations > Advanced Features
Maintainability > Feature Completeness
Developer Experience > Flexibility
```

**지원**: 기본 CRUD (이슈 생성/검색/업데이트, 페이지 조회)
**제거**: 분석, 메트릭, 고급 네비게이션 (emoji), 계층(folder)

---

## 다음 작업 (예상)

- [ ] Jira 모듈 검토 (metrics, workflow, SLA 제거 여부)
- [ ] Models 정리 (사용하지 않는 필드 제거)
- [ ] 테스트 확인 (476줄 제거 후 테스트 상태)
- [ ] MCP 도구 검증 (변경사항 반영)
- [ ] 최종 문서화 (팀 온보딩 가이드)

---

## 참고 자료

### 핵심 문서
1. **commit-msg-rules.sh** - Conventional Commits 규칙 (필수)
2. **INTERNAL_SETUP.md** - JFrog 설정 (신규 개발자 필독)
3. **FEATURE_SCOPE.md** - 지원 기능 범위 (뭐가 안 되는지 알기)
4. **CONFLUENCE_MODULE_CHANGES.md** - API 변경 사항 (코드 수정 시 필독)

### 원본 비교
- mcp-atlassian (readonly): `chmod 555` 로 설정됨
- 원본 분석: `docs/PHASE8_ANALYSIS.md` 참고

---

## Tips for Tomorrow

1. **git log 활용**
   ```bash
   git log --oneline -20          # 최근 20개 커밋 확인
   git show [commit-hash]         # 특정 커밋 상세 보기
   git diff HEAD~5..HEAD          # 최근 5개 커밋의 변경사항
   ```

2. **빠른 방향 전환**
   - docs/ 파일을 먼저 읽고 맥락 파악
   - `git status`로 남은 작업 확인
   - 이전 커밋 메시지로 패턴 학습

3. **문제 발생 시**
   - mcp-atlassian (readonly) 와 비교
   - FEATURE_SCOPE.md 로 "이게 맞는 제거인지" 검증
   - 커밋 메시지와 docs 일관성 확인

---

**마지막 업데이트**: 2026-02-20
**총 진행시간**: ~3시간 (16개 커밋)
**다음 시작점**: `git log --oneline` 로 최신 상태 확인
