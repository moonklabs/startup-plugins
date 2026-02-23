# 커넥터

## 도구 참조 방식

플러그인 파일은 `~~category`를 해당 카테고리에서 사용자가 연결한 도구의 플레이스홀더로 사용합니다. 예를 들어 `~~knowledge base`는 Notion, Google Drive, Confluence 중 연결된 도구를 의미합니다.

플러그인은 **도구에 구애받지 않습니다** — 특정 제품이 아닌 카테고리로 워크플로우를 설명합니다. `.mcp.json`에 특정 MCP 서버가 사전 구성되어 있지만, 해당 카테고리의 어떤 MCP 서버든 사용할 수 있습니다.

## 이 플러그인의 커넥터

| 카테고리 | 플레이스홀더 | 포함 서버 | 기타 옵션 |
|----------|-------------|-----------|-----------|
| 지식 베이스 | `~~knowledge base` | Notion | Google Drive, Confluence |
| 문서 | `~~docs` | Microsoft 365, Notion | Google Docs |
| 데이터 보강 | `~~data enrichment` | — | 기업마당, K-Startup (웹 검색 기반) |
| 스프레드시트 | `~~spreadsheet` | Microsoft 365 | Google Sheets |
| 채팅 | `~~chat` | Slack | Microsoft Teams |

## 한국 지원사업 데이터 소스

현재 공식 MCP 서버를 제공하는 지원사업 포털은 없습니다. 웹 검색을 통해 접근합니다.

| 포털 | URL | 특화 정보 |
|------|-----|----------|
| **기업마당** | bizinfo.go.kr | 정부 지원사업 통합 공고 |
| **K-Startup** | k-startup.go.kr | 창업 지원사업 전문 |
| **TIPS** | tips.go.kr | 기술창업 투자 프로그램 |
| **중소기업 통합공시** | smes.go.kr | 중소벤처기업부 공고 |
| **서울산업진흥원** | sba.seoul.kr | 서울 소재 기업 특화 |

## 지식베이스 연결 가이드

`~~knowledge base`(Notion 권장)에 회사 지식베이스를 구성하면:
- `/kb-init` 실행 시 자동으로 Notion 페이지 생성
- `/kb-update` 시 Notion 데이터베이스 자동 갱신
- `/apply-write` 시 Notion에서 최신 회사 정보 자동 로드

Notion 미연결 시 로컬 Markdown 파일(`.kb/`)로 대체 저장됩니다.
