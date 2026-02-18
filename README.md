# startup-plugins

Moonklabs의 Claude Code 플러그인 마켓플레이스입니다. 스타트업 창업자를 위한 AI 워크플로우 플러그인을 제공합니다.

## 플러그인 목록

| 플러그인 | 설명 |
|---|---|
| [startup-ceo](./startup-ceo/) | VC/AC 투자 유치 일일 루틴 — 딜소싱, 아웃리치, 파이프라인, IR 자료, 재무모델링, GTM 전략 |

## 설치

### 마켓플레이스 등록

```bash
# GitHub에서 직접 추가
claude plugins marketplace add moonklabs/startup-plugins
```

### 플러그인 설치

```bash
claude plugins install startup-ceo
```

Claude Code를 재시작하면 커맨드와 스킬이 활성화됩니다.

---

## startup-ceo

스타트업 창업자의 투자 유치 일상을 자동화하는 종합 Startup OS 플러그인입니다. 웹 검색만으로 단독 작동하며, CRM·이메일·문서 도구를 연결하면 더욱 강력해집니다.

### 커맨드

슬래시 커맨드로 명시적으로 실행하는 워크플로우입니다.

#### 일일 루틴

| 커맨드 | 설명 |
|---|---|
| `/daily-fundraise` | 일일 펀드레이징 브리핑 — 오늘의 우선순위, 딜소싱, 팔로업, 미팅 준비 |
| `/deal-sourcing` | VC/AC 새 투자자 타겟 발굴 — 웹 검색, thesis 매칭, 네트워크 매핑 |
| `/lead-dashboard` | 투자자 리드 리스트 대시보드 — 단계별 현황, 건강점수, 액션 제안 |

#### 아웃리치 & 파이프라인

| 커맨드 | 설명 |
|---|---|
| `/investor-outreach` | VC 리서치 + thesis 매칭 + 웜인트로 + 콜드 이메일 + 후속 시퀀스 |
| `/fundraise-pipeline` | 파이프라인 건강점수(100점) + 단계별 현황 + 리스크 플래그 |

#### IR & 미팅 준비

| 커맨드 | 설명 |
|---|---|
| `/investor-update` | 월간/분기 투자자 업데이트 — 핵심 지표, 하이라이트, 챌린지 |
| `/pitch-review` | 피치 덱 리뷰(100점) + 슬라이드별 평가 + 예상 VC 질문 |
| `/dd-prep` | DD/미팅 준비 — 투자자 배경, 예상 질문, 데이터룸 체크리스트 |
| `/create-ir-asset` | IR HTML 아티팩트 — Executive Summary, 원페이저, 투자 메모 |

#### 예측 & 분석

| 커맨드 | 설명 |
|---|---|
| `/fundraise-forecast` | 투자유치 예측 — 확약/파이프라인/가중예측, 3가지 시나리오, 런웨이 교차점 |
| `/business-case` | 투자자용 비즈니스 케이스 — 10섹션 구조화 문서 |
| `/market-opportunity` | TAM/SAM/SOM 시장 분석 — 3가지 방법론 교차 검증 |
| `/gtm-plan` | Go-to-Market 전략 — GTM 모션, ICP, 채널, 90일 실행 계획 |

### 스킬

컨텍스트에 따라 Claude가 자동으로 활성화하는 도메인 지식입니다.

#### 펀드레이징

| 스킬 | 설명 |
|---|---|
| `fundraising-process` | Pre-seed~Series B 라이프사이클, 단계별 벤치마크, 8주 타임라인 |
| `investor-research` | VC 펀드/파트너 7-query 웹검색, thesis 매칭, 접근전략 |
| `deal-sourcing` | VC, AC, 엔젤, CVC 소싱 방법론 — Thesis 매칭, 접근 경로 |
| `pitch-craft` | Sequoia-style 12슬라이드, 스토리텔링, VC 예상질문 30개 |
| `financial-modeling` | 3-시나리오 재무 모델링, SaaS·마켓플레이스·커머스 템플릿 |
| `term-sheet-knowledge` | 텀시트 주요조건, SAFE/전환사채, 캡테이블, 희석 계산 |
| `fundraise-comms` | 이메일 템플릿 — 웜인트로/콜드/팔로업/업데이트, Day5/10/21 케이던스 |

#### 사업 분석

| 스킬 | 설명 |
|---|---|
| `startup-metrics` | SaaS/마켓플레이스/컨슈머/B2B 메트릭스, 단계별 벤치마크 |
| `market-sizing` | TAM/SAM/SOM 3단계 프레임워크, Top-down/Bottom-up/Value Theory |
| `competitive-landscape` | Porter's 5 Forces, Blue Ocean, 포지셔닝 매트릭스, 배틀카드 |

#### GTM & 세일즈

| 스킬 | 설명 |
|---|---|
| `gtm-strategy` | GTM 모션(PLG/Sales-Led/Community-Led), PESO 모델, 콘텐츠 전략 |
| `pricing-strategy` | 가격 모델 비교, 밸류 메트릭, Good/Better/Best 패키징 |
| `sales-playbook` | MEDDPICC, 세일즈 단계, 핵심 지표, 팀 설계 |

### MCP 통합

`.mcp.json`에 사전 구성된 서버 외에도, 동일 카테고리의 MCP 서버라면 어떤 것이든 연결할 수 있습니다.

| 카테고리 | 기본 제공 (MCP 지원) | 추가 옵션 |
|---|---|---|
| CRM | HubSpot, Notion | Relate (한국 IR 특화, MCP 미지원 — 수동 운영) |
| 이메일·캘린더 | Microsoft 365 | Gmail, Google Calendar |
| 채팅 | Slack | Microsoft Teams |
| 데이터 보강 | OpenDART (상장사 한정, 커뮤니티 MCP) | THE VC, 혁신의숲, 넥스트유니콘 (웹 검색 기반) |
| 문서·스프레드시트 | Microsoft 365, Notion | Google Docs, Google Sheets |

자세한 내용은 [CONNECTORS.md](./startup-ceo/CONNECTORS.md)를 참조하세요.

## 라이선스

Apache 2.0
