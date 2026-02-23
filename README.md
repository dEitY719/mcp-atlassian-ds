# 🛠️ DS JIRA MCP (Beta)

> [English README](https://github.samsungds.net/hahn21-lee/mcp-dsjira/blob/main/README.en.md)

> LLM이 DS JIRA를 활용할 수 있도록 해주는 MCP(Model Context Protocol) 서버입니다.
> LLM은 해당 MCP를 활용해 JIRA 이슈를 검색, 생성, 업데이트할 수 있습니다.

이 프로젝트는 오픈소스 원본 레포지토리 [mcp-atlassian](https://github.com/sooperset/mcp-atlassian)를 기반으로
삼성 DS JIRA 환경에 맞추어 환경을 세팅하고, 일부 버그를 수정하였습니다.

## 📌 개요

LLM이 Jira와 상호작용할 수 있도록 하는 MCP 서버입니다.
MCP를 활용해 DS Jira 실시간 서버에 접근 가능합니다.

개인별 인증 정보를 활용합니다. 따라서, 공용 계정이 아닌 **개인별 Jira 계정**으로 Jira에 접근이 가능합니다.
이슈 수정, 댓글 추가 등 대부분의 JIRA 활용 동작을 MCP를 통해 수행할 수 있습니다.

### 🔐 인증 시스템

Jira MCP는 PAT(개인별 인증 토큰)을 활용한 인증 시스템을 사용하고 있습니다.
해당 시스템은 아래와 같은 장점이 있습니다.

- **사용자별 권한 적용** (접근 가능한 Jira Project 정보)
- **개인화된 서비스 제공** (나한테 할당된 Jira 이슈 확인, 내 계정으로 Jira Comment 작성하기 등)

## 🛠 사용 방법

아래 가이드에 따라 MCP 클라이언트 (Roo Code 등) 설정에서 이 서버를 등록한 후,
AI 어시스턴트에게 질문하면 됩니다.

### 🔑 Jira PAT 발급 방법

1. Jira 오른쪽 위 개인 프로필 이미지 클릭 → 프로파일 → 개인용 액세스 토큰 → 토큰 만들기
2. 토큰 이름 입력 (아무거나 상관 없습니다) → 자동 만료 해제 → 만들기
3. 생성된 토큰 복사

---

### 🧩 Roo Code MCP Config 설정

Roo Code MCP config 파일 (`mcp_settings.json`)을 아래와 같이 작성한 후,
**`<개인별 Jira PAT>` 부분만 본인의 것으로 변경**해 주세요. ex) "Authorization": "Token MTQ4MjIwMzc4ND~~~"

```json
{
    "mcpServers": {
        "jira": {
            "url": "http://mcp-servers--mcp-dsjira-prod.khprdpb01.apps.dks.samsungds.net/mcp/",
            "type": "streamable-http",
            "headers": {
                "Authorization": "Token <개인별 Jira PAT>"
            },
            "disabled": false,
            "alwaysAllow": [
                "jira_search",
                "jira_get_issue",
                "jira_get_all_projects",
                "jira_get_project_issues",
                "jira_get_worklog",
                "jira_get_transitions",
                "jira_search_fields",
                "jira_get_agile_boards",
                "jira_get_board_issues",
                "jira_get_sprints_from_board",
                "jira_get_sprint_issues",
                "jira_get_issue_link_types",
                "jira_get_user_profile"
            ]
        }
    }
}
```

> 참고) `alwaysAllow` 필드는 사용자의 승인 없이도 자동으로 실행할 도구들을 설정하는 필드입니다.
> 현재 Read-only Tool에 한해 `alwaysAllow` 설정되어 있습니다. 개인의 상황에 맞게 설정해주세요.

---

### 💬 사용 예시

MCP를 활용해 AI 어시스턴트에게 다음과 같은 요청을 할 수 있습니다:

```
- "ABC 프로젝트에서 일주일동안 업데이트된 이슈들 요약해줘"
- "PROJ-123 이슈의 상세 정보와 Epic Link 확인해"
- "새 이슈를 생성해줘: 프로젝트 DMSI, 유형 Task, 요약 'API 개선'"
- "ISSUE-456의 상태를 'In Progress'로 변경해"
- "BUG-123 이슈 changelog 조회해줘"
- "나한테 할당된 이슈들 요약해줘"
- "26' W4 스프린트의 모든 이슈 보여줘"
- "ABC-123 에 다음 내용으로 댓글 달아줘. '해당 이슈는 완료되어 close 하겠습니다.'"
```

---

## 📋 지원 기능

이 MCP 서버는 다음 JIRA 기능을 제공합니다.

### 🔍 검색 및 조회 (Read)

| Tool                          | 설명                      |
| ----------------------------- | ------------------------- |
| `jira_search`                 | 이슈 검색 (JQL 쿼리 지원) |
| `jira_get_issue`              | 특정 이슈 상세 조회       |
| `jira_get_all_projects`       | 모든 프로젝트 조회        |
| `jira_get_project_issues`     | 프로젝트별 이슈 목록 조회 |
| `jira_get_worklog`            | 작업 로그 조회            |
| `jira_get_transitions`        | 상태 전환 가능 목록 조회  |
| `jira_search_fields`          | 필드 검색                 |
| `jira_get_agile_boards`       | Agile 보드 조회           |
| `jira_get_board_issues`       | 보드 내 이슈 조회         |
| `jira_get_sprints_from_board` | 보드의 스프린트 조회      |
| `jira_get_sprint_issues`      | 스프린트 내 이슈 조회     |
| `jira_get_issue_link_types`   | 이슈 링크 유형 조회       |
| `jira_get_user_profile`       | 사용자 프로필 정보 조회   |

### ✏️ 이슈 관리 (Write)

| Tool                    | 설명                                 |
| ----------------------- | ------------------------------------ |
| `jira_create_issue`     | 새 이슈 생성                         |
| `jira_update_issue`     | 이슈 업데이트 (필드 수정, 상태 변경) |
| `jira_delete_issue`     | 이슈 삭제                            |
| `jira_add_comment`      | 댓글 추가                            |
| `jira_transition_issue` | 이슈 상태 전환                       |

### 🏃 스프린트 관리 (Write)

| Tool                 | 설명              |
| -------------------- | ----------------- |
| `jira_create_sprint` | 스프린트 생성     |
| `jira_update_sprint` | 스프린트 업데이트 |

---

## 🧩 DS JIRA 커스텀 필드

AI 어시스턴트는 DS JIRA 환경의 다음 커스텀 필드를 활용하여 이슈를 검색하고 관리할 수 있습니다:

| 필드 ID             | 필드명                 | 사용 예시                 |
| ------------------- | ---------------------- | ------------------------- |
| `customfield_10201` | Epic Link              | Epic에 연결된 이슈 검색   |
| `customfield_10203` | Epic Name              | Epic 이름으로 이슈 그룹화 |
| `customfield_11106` | Start date (WBSGantt)  | 프로젝트 시작 일정        |
| `customfield_11107` | Finish date (WBSGantt) | 프로젝트 종료 일정        |
| `customfield_15221` | Actual start date      | 실제 시작 일자            |
| `customfield_15222` | Actual finish date     | 실제 완료 일자            |
| `customfield_10660` | Type                   | 이슈 유형 (Milestone 등)  |
| `customfield_12905` | Milestone              | 마일스톤 정보             |
| `customfield_14804` | Target Project         | 대상 프로젝트             |
| `customfield_15316` | Chip Revision          | 칩 리비전 정보            |
| `customfield_15500` | 팀명                   | 소속 팀                   |
| `customfield_10733` | Co-workers             | 협업자 목록               |
| `customfield_11301` | Watcher List           | 관찰자 목록               |
| `customfield_11884` | CC List                | 수신자 목록               |
| `customfield_12351` | Group_CC               | 그룹 수신자               |
| `customfield_14826` | Input Data             | 입력 데이터               |
| `customfield_15239` | Closing Notes          | 마감 메모                 |

> ### 해당 필드들은 조회 / 검색시 필드 명을 명확하게 입력해주셔야 합니다.
>
> ### 해당 프로젝트에 특정 필드가 존재하지 않거나, 생성이 불가능한 경우 에러가 발생할 수 있습니다.

---

## 🧮 JQL 쿼리 예시

AI 어시스턴트에게 혼합된 JQL 쿼리를 요청할 수 있습니다:

```
- 특정 유형의 이슈: "issuetype = Epic AND project = PROJ"
- Epic 내 하위 이슈: "parent = PROJ-123"
- 상태별 검색: "status = 'In Progress' AND project = PROJ"
- 담당자별: "assignee = currentUser()"
- 최근 업데이트: "updated >= -7d AND project = PROJ"
- 버그만: "issuetype = Bug AND project = PROJ"
- 나에게 할당된 업무: "assignee = currentUser() AND status != Done"
- 중요도별: "priority = High AND project = PROJ"
```

---

## 💡 팁

1. **커스텀 필드 활용**: "Chip Revision이 'EVT1'인 이슈 5개만 찾아줘"라고 요청하면 `customfield_15316` 필드로 검색합니다.
2. **날짜 기반 검색**: "이번 달에 시작된 이슈" 또는 "마감일이 다가오는 이슈"로 요청할 수 있습니다.
3. **나한테 할당된 이슈 조회**: "나한테 할당된 이슈들 요약해줘"라고 요청하여 개인별 이슈 현황을 조회할 수 있습니다. (사용자가 입력한 PAT를 활용하여 사용자를 구별합니다.)
4. **본문에서 특정 정보 가져오기**: 이슈 설명, 댓글 등에서 내용을 추출하거나 요약할 수 있습니다.
5. **작업을 나누어서 요청하기**: 너무 많은 이슈를 한번에 조회하는 경우, Context가 넘치거나 MCP 측에서 오류가 발생할 수 있습니다. 작업을 작은 단위로 나누어서 요청해주세요.

---

## 🆘 지원

Bug 혹은 문의사항이 있는 경우 [Issues](https://github.samsungds.net/hahn21-lee/mcp-dsjira/issues) 탭에 남겨주시거나, 이한 (hahn21.lee) 에게 문의해주세요.
기술적인 문제는 아래 원본 repo [mcp-atlassian](https://github.com/sooperset/mcp-atlassian) 를 참고해주셔도 좋을 것 같습니다.

---

## 📚 참고

1. Jira는 조직별로 활용 형태나 규칙이 매우 상이합니다. 따라서 각 Jira 프로젝트의 Structure에 따라 동작하지 않는 도구가 존재할 수 있습니다.
2. 아직 베타버전이라 서비스가 안정적이지 않을 수 있습니다 😭. 문제가 발생할 경우 [Issues](https://github.samsungds.net/hahn21-lee/mcp-dsjira/issues) 탭에 남겨주시면 최대한 대응할 수 있도록 하겠습니다.
3. S.LSI Jira는 현재(2026/1/22 기준) v8.5.5로, PAT를 활용한 인증을 지원하지 않습니다. 따라서 개인별 인증을 필요로 하는 해당 MCP 사용이 불가능하며, 1/31 이후 버전이 10.3.7로 업그레이드되어 PAT를 활용한 인증이 가능해지면 검토를 거쳐 MCP 지원을 계획하고 있습니다.
