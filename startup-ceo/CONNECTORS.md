# 커넥터

## 도구 참조 방식

플러그인 파일은 `~~category`를 해당 카테고리에서 사용자가 연결한 도구의 플레이스홀더로 사용합니다. 예를 들어 `~~CRM`은 HubSpot, Notion, Affinity 또는 MCP 서버가 있는 다른 CRM을 의미할 수 있습니다.

플러그인은 **도구에 구애받지 않습니다** — 특정 제품이 아닌 카테고리(CRM, 이메일, 채팅 등)로 워크플로우를 설명합니다. `.mcp.json`에 특정 MCP 서버가 사전 구성되어 있지만, 해당 카테고리의 어떤 MCP 서버든 사용할 수 있습니다.

## 이 플러그인의 커넥터

| 카테고리 | 플레이스홀더 | 포함 서버 | 기타 옵션 |
|----------|-------------|-----------|-----------|
| CRM / 투자자 관리 | `~~CRM` | HubSpot, Notion | Affinity, Attio, Airtable, Close |
| 이메일 | `~~email` | Microsoft 365 | Gmail |
| 캘린더 | `~~calendar` | Microsoft 365 | Google Calendar |
| 채팅 | `~~chat` | Slack | Microsoft Teams |
| 지식 베이스 | `~~knowledge base` | Notion | Google Drive, Confluence |
| 데이터 보강 | `~~data enrichment` | Clay, ZoomInfo | Crunchbase, PitchBook, Dealroom |
| 스프레드시트 | `~~spreadsheet` | Microsoft 365 | Google Sheets |
| 문서 | `~~docs` | Microsoft 365, Notion | Google Docs, Google Slides |
| 분석/BI | `~~analytics` | — | Mixpanel, Amplitude, ChartMogul |
