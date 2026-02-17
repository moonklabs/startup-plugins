# Startup CEO 플러그인

Anthropic의 에이전트 데스크톱 애플리케이션인 [Cowork](https://claude.com/product/cowork)을 위해 설계된 스타트업 창업자 생산성 플러그인이며, Claude Code에서도 사용할 수 있습니다. VC/AC 투자 유치의 일일 루틴을 실행하고, 시장 분석, 재무 모델링, GTM 전략, 가격 전략, 경쟁 분석, 세일즈를 아우르는 종합 Startup OS 플러그인입니다.

**핵심 일일 워크플로우**: 아침 브리핑 → 딜소싱 → Lead Dashboard → 아웃리치 실행 → 미팅 준비/DD → IR 자료 제작

## 설치

```bash
claude plugins add startup-ceo
```

## 커맨드

슬래시 커맨드로 호출하는 명시적 워크플로우입니다:

### 일일 루틴 (3개)

| 커맨드 | 설명 |
|---|---|
| `/daily-fundraise` | 일일 펀드레이징 브리핑 — 오늘의 우선순위, 딜소싱, 팔로업, 미팅 준비를 한눈에 |
| `/deal-sourcing` | VC/AC 새 투자자 타겟 발굴 — 웹 검색, thesis 매칭, 네트워크 매핑 |
| `/lead-dashboard` | VC/AC 투자자 리드 리스트 대시보드 — 전체 현황, 단계별 분류, 액션 제안 |

### 아웃리치 & 파이프라인 (2개)

| 커맨드 | 설명 |
|---|---|
| `/investor-outreach` | VC 리서치 + thesis 매칭 + 웜인트로 + 콜드 이메일 + 후속 시퀀스 |
| `/fundraise-pipeline` | 투자자 파이프라인 건강점수 (100점) + 단계별 현황 + 리스크 플래그 + 커버리지 |

### IR & 미팅 준비 (4개)

| 커맨드 | 설명 |
|---|---|
| `/investor-update` | 월간/분기 투자자 업데이트 — 핵심 지표, 하이라이트, 챌린지, 도움 요청 |
| `/pitch-review` | 피치 덱 리뷰 (100점) + 슬라이드별 평가 + 예상 VC 질문 + 답변 |
| `/dd-prep` | DD/미팅 준비 — 투자자 배경, 예상 질문, 미팅 전략, 데이터룸 체크리스트 |
| `/create-ir-asset` | IR HTML 아티팩트 — Executive Summary, 원페이저, 데이터룸 랜딩, 투자 메모 |

### 예측 & 분석 (4개)

| 커맨드 | 설명 |
|---|---|
| `/fundraise-forecast` | 투자유치 예측 — 확약/파이프라인/가중예측, 최선/예상/최악 시나리오, 런웨이 교차점 |
| `/business-case` | 투자자용 비즈니스 케이스 — 10섹션 (시장, 솔루션, 경쟁, 재무, 팀, 트랙션, 리스크) |
| `/market-opportunity` | TAM/SAM/SOM 시장 분석 — 3가지 방법론 교차 검증, 투자자 프레젠테이션 형식 |
| `/gtm-plan` | Go-to-Market 전략 수립 — GTM 모션, ICP, 채널, 가격, 90일 실행 계획 |

모든 커맨드는 **단독**으로 작동하며(웹 검색, 사용자 입력), MCP 커넥터를 연결하면 **더욱 강력해집니다**.

## 스킬

관련 상황에서 Claude가 자동으로 활용하는 도메인 지식입니다:

### 펀드레이징 (7개)

| 스킬 | 설명 |
|---|---|
| `fundraising-process` | Pre-seed~Series B 라이프사이클, 단계별 벤치마크, 8주 타임라인, 준비 체크리스트 |
| `investor-research` | VC 펀드/파트너 7-query 웹검색, thesis 매칭, 접근전략 출력 템플릿 |
| `deal-sourcing` | VC, AC, 엔젤, CVC 투자자 소싱 방법론 — 데이터 소스, Thesis 매칭, 접근 경로 |
| `pitch-craft` | Sequoia-style 12슬라이드, 슬라이드별 가이드, 스토리텔링, VC 예상질문 30개 |
| `financial-modeling` | 3-시나리오 재무 모델링 (Base/Bull/Bear), SaaS·마켓플레이스·커머스 템플릿, 유닛이코노믹스 |
| `term-sheet-knowledge` | 텀시트 주요조건, SAFE/전환사채, 캡테이블, 희석 계산, Red Flags |
| `fundraise-comms` | 이메일 템플릿 (웜인트로/콜드/팔로업/업데이트), 월간 업데이트, Day5/10/21 케이던스 |

### 사업 분석 (3개)

| 스킬 | 설명 |
|---|---|
| `startup-metrics` | SaaS/마켓플레이스/컨슈머/B2B 메트릭스, 단계별 벤치마크, 투자자 보고 형식 |
| `market-sizing` | TAM/SAM/SOM 3단계 프레임워크, Top-down/Bottom-up/Value Theory 방법론 |
| `competitive-landscape` | Porter's 5 Forces, Blue Ocean 4-Actions, 포지셔닝 매트릭스, 배틀카드, Win/Loss |

### GTM & 세일즈 (3개)

| 스킬 | 설명 |
|---|---|
| `gtm-strategy` | GTM 모션 (PLG/Sales-Led/Community-Led/Content-Led/Founder-Led), PESO 모델, 콘텐츠 전략 |
| `pricing-strategy` | 가격 모델 비교, 밸류 메트릭, 가격 심리학, Good/Better/Best 패키징, 연간 vs 월간 |
| `sales-playbook` | MEDDPICC, 세일즈 단계, 핵심 지표, 단계별 전환율, 팀 설계 |

## 예시 워크플로우

### 아침 일일 루틴

```
/daily-fundraise
```

오늘의 우선순위, 투자자 미팅 목록, 후속연락 대상, 딜소싱 타겟, 런웨이 현황을 한눈에 확인합니다. ~~CRM, ~~calendar, ~~email이 연결되어 있으면 자동으로 데이터를 가져옵니다.

### 새로운 투자자 발굴

```
/deal-sourcing fintech series A
```

핀테크 Series A 투자자를 웹 검색으로 발굴하고, thesis 적합도를 평가(HIGH/MEDIUM/LOW)하며, 웜인트로 경로를 매핑합니다. ~~data enrichment (Crunchbase, PitchBook)가 연결되면 더욱 정확합니다.

### 투자자 리드 현황 파악

```
/lead-dashboard
```

전체 투자자 리드 리스트를 단계별로 정리하고, 건강점수(100점)를 계산하며, 정체/무응답 리스크를 플래그합니다. 주간 액션 플랜을 제안합니다.

### 맞춤형 아웃리치

```
/investor-outreach Sequoia Capital
```

Sequoia Capital을 리서치하고, thesis와의 적합도를 평가한 후, 웜인트로 블럽(포워딩 가능)과 콜드 이메일(AIDA 구조)을 생성합니다.

### 피치 덱 리뷰

```
/pitch-review
```

피치 덱을 업로드하면 슬라이드별로 G/Y/R 평가, 내러티브 흐름 분석, 누락 요소 지적, 예상 VC 질문 30개와 답변을 제공합니다.

### 시장 기회 분석

```
/market-opportunity
```

TAM/SAM/SOM을 3가지 방법론(Top-down, Bottom-up, Value Theory)으로 교차 검증하고, 투자자 프레젠테이션용 표와 차트를 생성합니다.

### GTM 전략 수립

```
/gtm-plan
```

제품과 타겟 시장에 최적화된 GTM 모션을 선정하고, ICP를 정의하며, 채널 우선순위, 가격 패키징, 90일 실행 계획을 수립합니다.

## 단독 사용 + 강화 모드

모든 커맨드와 스킬은 통합 도구 없이도 작동합니다:

| 가능한 작업 | 단독 사용 | 강화 연동 |
|-------------|-----------|-----------|
| 일일 브리핑 | 사용자가 파이프라인·미팅 입력 | ~~CRM, ~~calendar, ~~email (자동 수집) |
| 딜소싱 | 웹 검색 | ~~data enrichment (Crunchbase, PitchBook, Dealroom) |
| Lead 대시보드 | 사용자가 리드 리스트 입력 | ~~CRM (자동 파이프라인 데이터) |
| 투자자 아웃리치 | 웹 검색 + 사용자 맥락 | ~~CRM, ~~email (이력, 자동 전송) |
| 피치 리뷰 | 덱 파일 업로드 | ~~docs (Google Slides, Notion) |
| 재무 모델링 | 사용자가 가정 입력 | ~~spreadsheet (템플릿 자동 생성) |
| IR 자료 생성 | HTML 아티팩트 생성 | ~~docs (Notion, Google Drive 저장) |
| 투자자 업데이트 | 사용자가 지표 입력 | ~~analytics (Mixpanel, Amplitude), ~~CRM |

## MCP 통합

> 익숙하지 않은 플레이스홀더가 보이거나 연결된 도구를 확인하려면 [CONNECTORS.md](CONNECTORS.md)를 참조하세요.

도구를 연결하면 더 풍부한 경험을 제공합니다:

| 카테고리 | 예시 | 활성화되는 기능 |
|---|---|---|
| **CRM / 투자자 관리** | HubSpot, Notion, Affinity | 투자자 파이프라인, 미팅 이력, 커뮤니케이션 기록 |
| **데이터 보강** | Clay, ZoomInfo, Crunchbase, PitchBook | VC 펀드 데이터, 투자 이력, thesis, 포트폴리오 |
| **이메일** | Microsoft 365, Gmail | 아웃리치 자동화, 후속 연락 추적 |
| **캘린더** | Microsoft 365, Google Calendar | 투자자 미팅 일정, DD 세션 준비 |
| **문서** | Notion, Google Docs/Slides | 피치 덱, 데이터룸, IR 자료 |
| **스프레드시트** | Microsoft 365, Google Sheets | 재무 모델, 파이프라인 추적 |
| **분석/BI** | Mixpanel, Amplitude, ChartMogul | 핵심 지표, 성장 트렌드, 투자자 업데이트 |
| **채팅** | Slack, Teams | 팀 협업, 인트로 요청, 내부 논의 |

전체 지원 통합 목록은 [CONNECTORS.md](CONNECTORS.md)를 참조하세요.

## 라이선스

Apache 2.0
