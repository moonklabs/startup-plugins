# 커넥터

## 도구 참조 방식

플러그인 파일은 `~~category`를 해당 카테고리에서 사용자가 연결한 도구의 플레이스홀더로 사용합니다. 예를 들어 `~~CRM`은 Relate, HubSpot, Notion 또는 MCP 서버가 있는 다른 CRM을 의미할 수 있습니다.

플러그인은 **도구에 구애받지 않습니다** — 특정 제품이 아닌 카테고리(CRM, 이메일, 채팅 등)로 워크플로우를 설명합니다. `.mcp.json`에 특정 MCP 서버가 사전 구성되어 있지만, 해당 카테고리의 어떤 MCP 서버든 사용할 수 있습니다.

## 이 플러그인의 커넥터

| 카테고리 | 플레이스홀더 | 포함 서버 | 기타 옵션 |
|----------|-------------|-----------|-----------|
| CRM / 투자자 관리 | `~~CRM` | HubSpot, Notion | Relate (한국 IR 특화, MCP 미지원 — 수동 운영), Affinity, Attio, Airtable |
| 이메일 | `~~email` | Microsoft 365 | Gmail |
| 캘린더 | `~~calendar` | Microsoft 365 | Google Calendar |
| 채팅 | `~~chat` | Slack | Microsoft Teams |
| 지식 베이스 | `~~knowledge base` | Notion | Google Drive, Confluence |
| 데이터 보강 | `~~data enrichment` | — | THE VC, 혁신의숲, 넥스트유니콘 (MCP 미지원 — 웹 검색 기반), OpenDART (MCP 지원 — 상장사 한정) |
| 스프레드시트 | `~~spreadsheet` | Microsoft 365 | Google Sheets |
| 문서 | `~~docs` | Microsoft 365, Notion | Google Docs, Google Slides |
| 분석/BI | `~~analytics` | — | Mixpanel, Amplitude, ChartMogul |

## 한국 데이터 보강 도구 안내

한국 VC/스타트업 데이터를 제공하는 주요 서비스는 현재 공식 MCP 서버를 제공하지 않습니다. 활용 방식은 다음과 같습니다:

| 도구 | 특화 데이터 | 활용 방식 |
|------|------------|-----------|
| **THE VC** (thevc.kr) | 한국 투자 라운드, VC 포트폴리오, 투자 이력 | 웹 검색 기반 접근 |
| **혁신의숲** (innoforest.co.kr) | 스타트업 트래픽·매출·고용 성장 지표 | 웹 검색 기반 접근 |
| **넥스트유니콘** (nextunicorn.kr) | 스타트업-투자자 매칭, 투자자 DB | 웹 검색 기반 접근 |
| **OpenDART** (opendart.fss.or.kr) | 상장사 공시, 재무제표, 지분구조 | MCP 서버 가능 (오픈소스) |

### OpenDART MCP 설정 (선택사항)

상장사 공시 데이터가 필요한 경우 커뮤니티 MCP 서버를 설치할 수 있습니다:

```bash
# Smithery를 통한 설치 (예시)
# https://github.com/snaiws/DART-mcp-server 참고
```

OpenDART API 키는 [opendart.fss.or.kr](https://opendart.fss.or.kr)에서 무료로 발급받을 수 있습니다.

## CRM 선택 가이드

| 상황 | 추천 도구 |
|------|----------|
| 한국어 IR 파이프라인 특화, 수동 운영 | **Relate** (MCP 미지원) |
| MCP 자동화 연동 필요 | **HubSpot** 또는 **Notion** |
| 지식베이스 겸용 | **Notion** |
