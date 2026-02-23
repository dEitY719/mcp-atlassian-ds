# Company Customization Guide

외부 오픈소스(mcp-atlassian)를 회사 DS 환경에 맞게 적용할 때의 핵심 커스터마이징 사항입니다.

## 1. 인증 방식 (Authentication)

### 원본 오픈소스
- 다양한 인증 방식 지원 (OAuth, Basic Auth, PAT)
- 선택 가능하고 유연함

### 회사 환경 (mcp-company)
- **PAT(개인별 인증 토큰) 기반 인증만 지원**
- 사용자별 권한 적용 (개인 계정으로만 접근)
- MCP 설정에서 `Authorization: Token <PAT>` 형태로 사용

**이유**:
- 개인별 감사 추적(audit trail) 필요
- 공용 계정 사용 금지 정책
- 권한 관리의 명확성

---

## 2. 커스텀 필드 (Custom Fields)

### 원본 오픈소스
- 기본 JIRA 필드만 지원
- 커스텀 필드는 제네릭하게 처리

### 회사 환경 (DS JIRA)
```
customfield_10201  → Epic Link
customfield_10203  → Epic Name
customfield_11106  → Start date (WBSGantt)
customfield_11107  → Finish date (WBSGantt)
customfield_15221  → Actual start date
customfield_15222  → Actual finish date
customfield_10660  → Type
customfield_12905  → Milestone
customfield_14804  → Target Project
customfield_15316  → Chip Revision
customfield_15500  → 팀명
customfield_10733  → Co-workers
... (총 15개 필드)
```

**필드 ID 매핑 필요**:
- 각 회사별 Jira 환경에서 커스텀 필드 ID가 다름
- `src/mcp_atlassian/jira/fields.py` 에서 hardcode됨
- 새 회사 환경에 적용 시 **필드 ID를 재조사해야 함**

---

## 3. MCP 설정 (Configuration)

### 클라이언트 설정
```json
{
  "mcpServers": {
    "jira": {
      "url": "http://mcp-servers--mcp-dsjira-prod.khprdpb01.apps.dks.samsungds.net/mcp/",
      "type": "streamable-http",
      "headers": {
        "Authorization": "Token <개인별 Jira PAT>"
      }
    }
  }
}
```

**회사별 차이점**:
- MCP 서버 URL (내부 서버 주소)
- 운영 환경 (프로덕션, 스테이징 등)
- Header 기반 인증 (공개 PyPI에서는 제외됨)

---

## 4. 기능 제거/변경 사항

### MVP 범위 밖의 기능들

| 기능 | 이유 | 영향 |
|------|------|------|
| Client Certificate | Proxy가 담당 | SSL 설정 불필요 |
| Header-based Auth | PAT 기반으로 통일 | 간소화 |
| Analytics/Metrics | 불필요 | 코드 간소화 |
| Emoji Features | 회사 정책 | 제거됨 |
| Stateless Mode | 불필요 | CLI 단순화 |

---

## 5. 주의사항

### 새로운 회사에 적용할 때

1. **필드 ID 확인**
   ```bash
   # Jira REST API로 필드 조회
   curl -H "Authorization: Bearer <TOKEN>" \
     https://jira.company.com/rest/api/3/fields
   ```

2. **커스텀 필드 검증**
   - 모든 필드가 모든 프로젝트에 존재하지는 않음
   - 프로젝트별로 사용 가능한 필드 확인 필요

3. **인증 방식 확인**
   - 회사 Jira 버전 (v8.x, v10.x 등)
   - PAT 지원 여부
   - Proxy 설정 (SSL 검증)

4. **MCP 서버 주소**
   - 배포 환경에 따라 URL 변경 필요
   - 내부 네트워크 접근 가능 확인

---

## 6. 회사별 Jira 환경 차이

### 예시: Samsung DS vs 다른 팀/회사

| 항목 | Samsung DS | 가능한 다른 환경 |
|------|-----------|----------------|
| Jira 버전 | v10.3.7+ | v8.x, v9.x, 클라우드 |
| 인증 | PAT | OAuth, Basic Auth |
| 커스텀 필드 | 15개 (DS 특화) | 0~N개 (가변) |
| Epic 관리 | customfield_10201 | 다른 ID |
| 칩 정보 | customfield_15316 | 없음 (DS 특화) |

---

## 7. 적용 체크리스트

새 환경에 적용할 때:

- [ ] Jira 버전 확인
- [ ] 사용 가능한 인증 방식 확인 (PAT 지원?)
- [ ] 모든 커스텀 필드 ID 매핑
- [ ] MCP 서버 배포 주소 확인
- [ ] SSL 인증서 설정 (필요시)
- [ ] 테스트 계정으로 검증
- [ ] 문서 업데이트 (필드 ID, 서버 주소 등)

---

## 참고

- **원본**: https://github.com/sooperset/mcp-atlassian
- **회사 내부**: https://github.samsungds.net/hahn21-lee/mcp-dsjira
- **필드 ID 소스**: `src/mcp_atlassian/jira/fields.py`
