# startup-apply 플러그인 설계서

> 스타트업 지원사업 관리 플러그인 — 지식베이스 기반 사업계획서 자동화

## 목표

회사의 모든 지식베이스를 구조화하여 지원사업 사업계획서를 자동으로 작성/업데이트하고, HWP 파일로 출력한다. **일을 줄이는 것**이 최우선 목표.

## 핵심 전략

**접근 방식:** 지식베이스 우선 (Knowledge-base first)

```
지식베이스 구조화 (1단계)
  → 사업계획서 자동화 (2단계)
  → 소싱/적합도/리포트 (3단계)
  → HWP 파일 생성 MCP 서버 (4단계)
```

## 맥락

| 항목 | 내용 |
|------|------|
| 지식베이스 | Notion + 로컬 파일 (산발적, 정리 필요) |
| 과거 문서 | 지원사업 신청서/사업계획서 다수 보유 |
| 소싱 범위 | 정부/민간/지자체/대기업/해외 전부 |
| 출력 형식 | 완성된 HWPX 파일 직접 생성 (구형 HWP 입력도 변환 지원) |
| 대상 | 자체 사용 → 마켓플레이스 공개 |

---

## 1. 플러그인 구조

### 워크플로우 전체도

```
과거 문서 + Notion + 파일
        │
        ▼
┌──────────────────┐
│  /kb-init         │ ← 1회: 지식베이스 초기 구축
│  /kb-update       │ ← 수시: 정보 추가/갱신
└──────────────────┘
        │
        ▼
┌──────────────────────────────────────────────┐
│              지식베이스 (구조화된 회사 정보)        │
│  ├── company-profile (회사/팀/제품)              │
│  ├── financials (매출/KPI/재무)                  │
│  ├── tech (기술/특허/IP)                         │
│  ├── market (시장/경쟁사)                        │
│  └── history (과거 사업계획서 패턴)                │
└──────────────────────────────────────────────┘
        │
        ▼
┌────────────┬──────────────┬─────────────┐
│ /apply-find │ /apply-check  │ /apply-daily │
│ 지원사업소싱  │ 적합도조사     │ 데일리리포트  │
└────────────┴──────┬───────┴─────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │ /apply-write      │ ← 사업계획서 자동 작성
          │ /apply-update     │ ← 사업계획서 업데이트
          └──────────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │ /apply-export     │ ← HWP 파일 생성
          └──────────────────┘
```

### 디렉토리 구조

```
startup-apply/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json                    # Notion, HWP 생성 MCP 서버 등
├── commands/
│   ├── kb-init.md               # 지식베이스 초기 구축
│   ├── kb-update.md             # 지식베이스 갱신
│   ├── apply-find.md            # 지원사업 소싱
│   ├── apply-check.md           # 적합도 조사
│   ├── apply-daily.md           # 데일리 리포트
│   ├── apply-write.md           # 사업계획서 작성
│   ├── apply-update.md          # 사업계획서 업데이트
│   └── apply-export.md          # HWP 파일 생성
├── skills/
│   ├── kb-structure/            # 지식베이스 스키마 및 구조화 규칙
│   ├── bizplan-writing/         # 사업계획서 작성 도메인 지식
│   ├── gov-program-knowledge/   # 한국 지원사업 공고 체계 지식
│   └── hwp-format/              # HWP/HWPX 파일 형식 지식
├── agents/
│   ├── kb-extractor.md          # 문서에서 정보 추출
│   ├── program-sourcer.md       # 지원사업 웹 검색/소싱
│   ├── suitability-analyzer.md  # 적합도 분석
│   └── bizplan-writer.md        # 사업계획서 섹션별 작성
├── hwp_server/                  # HWP 생성 MCP 서버 (Python + Java)
│   ├── main.py
│   └── ...
├── CONNECTORS.md
└── README.md
```

### MCP 서버 연결

| 카테고리 | MCP 서버 | 용도 |
|---------|---------|------|
| `~~knowledge base` | Notion | 회사 지식베이스 읽기/쓰기 |
| `~~docs` | 로컬 파일 | 과거 문서(HWP/Word/PDF) 읽기 |
| `~~hwp-generator` | 자체 MCP 서버 (Python + Java) | HWPX 파일 생성, HWP→HWPX 변환 |
| `~~data enrichment` | 웹 검색 | 지원사업 공고 소싱 |

---

## 2. 지식베이스 구조화

### 지식베이스 스키마

`/kb-init` 실행 시 Notion에 다음 구조로 데이터베이스를 생성한다.

```
📁 [회사명] 지식베이스
├── 📄 company-profile
│   ├── 회사 개요 (법인명, 설립일, 대표자, 소재지, 업종코드)
│   ├── 미션/비전
│   ├── 팀 구성 (핵심 인력, 학력, 경력, 역할)
│   └── 연혁
│
├── 📄 product
│   ├── 제품/서비스 설명
│   ├── 핵심 기술 및 차별점
│   ├── 기술 스택
│   └── 특허/IP/인증
│
├── 📄 market
│   ├── TAM/SAM/SOM
│   ├── 목표 고객 (페르소나)
│   ├── 경쟁사 분석
│   └── 시장 트렌드
│
├── 📄 business-model
│   ├── 수익 모델
│   ├── 가격 정책
│   ├── 고객 획득 전략 (GTM)
│   └── 핵심 파트너/채널
│
├── 📄 financials
│   ├── 매출/MRR 추이
│   ├── 주요 KPI (MAU, 전환율, LTV, CAC 등)
│   ├── 재무제표 요약
│   └── 자금 사용 계획
│
├── 📄 track-record
│   ├── 수상/선정 이력
│   ├── 과거 지원사업 수행 실적
│   ├── 투자 유치 이력
│   └── 주요 고객/레퍼런스
│
└── 📄 past-plans (과거 문서 패턴)
    ├── 문체/톤 분석 결과
    ├── 섹션별 자주 쓰는 표현
    └── 공고별 작성 패턴
```

### `/kb-init` 커맨드 워크플로우

```
/kb-init 실행
    │
    ▼
"과거 사업계획서 파일을 올려주세요 (HWP, Word, PDF)"
    │
    ▼
┌─────────────────────────────────────────┐
│  kb-extractor 에이전트 (병렬 실행)        │
│  ├── 문서 A → 회사정보 추출               │
│  ├── 문서 B → 재무/KPI 추출              │
│  └── 문서 C → 시장/기술 추출              │
└─────────────────────────────────────────┘
    │
    ▼
추출 결과를 스키마에 매핑 → 사용자에게 검토 요청
    │
    ▼
"다음 항목이 비어 있습니다: [목록]. 지금 채우시겠습니까?"
    │
    ▼
Notion에 지식베이스 페이지 생성 (~~knowledge base)
    │
    ▼
"✅ 지식베이스 구축 완료 — 7개 카테고리 중 5개 완성, 2개 보완 필요"
```

- 사용자가 파일만 던지면 AI가 자동 분류/추출
- 빈 항목은 명확히 알려주고, `/kb-update`로 나중에 채울 수 있음
- Notion 미연결 시 로컬 Markdown 파일로 대체 저장

### `/kb-update` 커맨드

```
/kb-update financials            # 특정 카테고리 업데이트
/kb-update --from 파일.hwp       # 새 문서에서 자동 추출
/kb-update --check               # 미갱신 항목 점검
```

### kb-extractor 에이전트

```yaml
name: kb-extractor
tools: Read, Write, WebFetch
model: sonnet
```

- 과거 사업계획서에서 정보를 카테고리별로 자동 분류 추출
- HWP/Word/PDF 파일을 텍스트로 변환 후 파싱
- 중복/충돌 데이터 감지 시 사용자에게 질문

### kb-structure 스킬

자동 활성화 시 제공:
- 한국 지원사업에서 요구하는 표준 항목 체크리스트
- 카테고리별 작성 가이드 (예: "TAM/SAM/SOM은 출처와 산출 근거를 반드시 포함")
- 정보 완성도 점수 산출 기준

---

## 3. 사업계획서 작성 및 업데이트

### 사업계획서 표준 구조 ← 지식베이스 매핑

```
사업계획서 섹션                    ← 지식베이스 소스
─────────────────────────────────────────────────
1. 기업 개요                      ← company-profile
2. 대표자 및 팀 역량                ← company-profile.team
3. 창업 아이템 소개                 ← product
4. 기술 개발 내용                   ← product.tech + product.ip
5. 시장 분석                       ← market (TAM/SAM/SOM)
6. 경쟁사 분석 및 차별성             ← market.competitors + product
7. 사업화 전략 (BM/GTM)            ← business-model
8. 마케팅/판매 전략                  ← business-model.gtm
9. 재무 계획                       ← financials
10. 자금 소요 및 사용 계획           ← financials.funding
11. 추진 일정                       ← (공고별 생성)
12. 기대 효과                       ← market + business-model
13. 수행 실적                       ← track-record
```

### `/apply-write` 커맨드 워크플로우

```
/apply-write TIPS 2026년 상반기
    │
    ▼
1단계: 공고 분석
  - 웹 검색으로 해당 공고 요강 파악
  - 평가 항목, 배점, 페이지 제한, 양식 확인
  - 필수 기재 항목 체크리스트 생성
    │
    ▼
2단계: 지식베이스 매핑
  - 각 섹션에 필요한 KB 데이터 자동 매핑
  - 부족한 항목 식별
  → "시장 규모 데이터가 2024년입니다. 최신 자료로 업데이트할까요?"
    │
    ▼
3단계: 섹션별 작성 (bizplan-writer 에이전트)
  - 평가 배점이 높은 섹션부터 작성
  - 과거 문서의 문체/톤 반영
  - 섹션마다 사용자 검토 요청
    │
    ▼
4단계: 최종 조립
  - 전체 문서 일관성 검토 (용어, 수치 교차검증)
  - 페이지/글자수 제한 준수 확인
  - Markdown 최종본 출력
  → "/apply-export로 HWP 변환 가능합니다"
```

### `/apply-update` 커맨드

기존 사업계획서를 새 공고에 맞게 재활용한다.

```
/apply-update 기존계획서.hwp → 창업성장기술개발 2026
    │
    ▼
1. 기존 문서 파싱 → 섹션별 분리
2. 새 공고 요강과 비교
   - 추가 필요: [신규 섹션 목록]
   - 수정 필요: [변경 섹션 목록]
   - 재활용 가능: [그대로 쓸 섹션 목록]
3. 지식베이스에서 최신 데이터 반영
4. 변경 부분만 새로 작성
```

### bizplan-writer 에이전트

```yaml
name: bizplan-writer
tools: Read, Write, WebSearch
model: sonnet
```

- 지식베이스 데이터를 기반으로 섹션별 초안 작성
- 평가 배점에 맞춰 분량 배분
- 과거 사업계획서의 문체/표현 패턴 적용
- 수치 인용 시 반드시 출처 표기

### bizplan-writing 스킬

자동 활성화 시 제공:
- 한국 지원사업 사업계획서 평가위원 관점 작성 가이드
- 섹션별 킬러 표현 및 피해야 할 표현
- 정량 데이터 제시 원칙
- 공고 유형별 강조 포인트 (TIPS → 기술력, 예비창업패키지 → 사업화 가능성)

---

## 4. 지원사업 소싱 및 적합도 조사

### `/apply-find` 커맨드

```
/apply-find
/apply-find AI·SaaS
/apply-find --deadline 2026-04
```

program-sourcer 에이전트가 병렬 웹 검색으로 다음 소스를 탐색한다:

| 카테고리 | 소스 |
|---------|------|
| 정부 포털 | K-Startup, 기업마당, TIPS, 중기부/과기부/산업부 |
| 민간/AC | 주요 AC 프로그램, 대기업 오픈이노베이션 |
| 지자체 | 서울산업진흥원, 테크노파크, 창업지원센터 |
| 해외 | YC, Techstars 등 |

출력: 적합도 점수 순으로 정렬된 공고 리스트 (높은 적합도 / 검토 필요 / 마감 임박)

### `/apply-check` 커맨드

```
/apply-check TIPS
```

suitability-analyzer 에이전트가 지식베이스와 공고 요건을 대조하여 상세 분석:

| 분석 항목 | 내용 |
|----------|------|
| 충족 항목 | 업력, 기술 보유, 팀 구성 등 |
| 보완 필요 | 미충족이나 보완 가능한 항목 + `/kb-update` 안내 |
| 미충족 | 지원 불가 사유 |
| 작성 전략 | 평가 배점 기반 강조 포인트, 추천 운영사 |
| 준비 체크리스트 | 다음 액션 아이템 |

### program-sourcer 에이전트

```yaml
name: program-sourcer
tools: WebSearch, Read
model: sonnet
```

### suitability-analyzer 에이전트

```yaml
name: suitability-analyzer
tools: Read, WebSearch
model: sonnet
```

### 적합도 분석 프레임워크

```
지식베이스 항목        ←비교→    공고 지원 자격/평가 항목
──────────────────────────────────────────────
company-profile       →  기업 형태, 업력, 소재지 요건
product.tech          →  기술 혁신성, TRL 단계
market                →  시장 규모, 성장성
financials            →  매출 규모, 재무 건전성
track-record          →  과거 수행 실적, 수상 이력
business-model        →  사업화 가능성, 수익 모델
```

---

## 5. 데일리 리포트

### `/apply-daily` 커맨드

매일 아침 지원사업 현황을 한눈에 파악한다.

출력 구성:
1. **#1 우선순위** — 가장 긴급한 액션 (마감 임박 등)
2. **진행 현황** — 작성 중 / 검토 대기 / 제출 완료 / 결과 대기 건수
3. **마감 임박** — 7일 이내 마감 공고 (D-day, 작성률, 다음 액션)
4. **작성 중인 사업계획서** — 각 사업계획서 진행률 바 + 미완성 섹션
5. **제출 완료/결과 대기** — 제출일, 결과 발표일, 상태
6. **신규 공고 알림** — 적합도 높은 신규 공고
7. **지식베이스 상태** — 미갱신 카테고리 경고
8. **오늘의 체크리스트** — 우선순위별 할 일

### 파이프라인 추적 구조

Notion DB(또는 로컬 파일)에 다음 구조로 관리:

```
📁 지원사업 파이프라인
├── 공고명
├── 주관기관
├── 마감일
├── 상태: [소싱|분석|작성중|검토|제출|결과대기|선정|탈락]
├── 적합도 점수
├── 작성률 (%)
├── 사업계획서 파일 경로
└── 메모
```

에이전트 병렬 실행:
- `program-sourcer` → 신규 공고 중 적합도 높은 건 탐지
- `suitability-analyzer` → 마감 임박 공고의 준비 상태 점검

---

## 6. HWP 파일 생성

### 포맷 전략

HWPX(XML 기반 신형 포맷)를 기본으로 생성한다. 구형 .hwp 입력은 hwp2hwpx(Java)로 변환 후 처리한다.

### `/apply-export` 커맨드

```
/apply-export 창업성장기술개발                      # HWPX 생성
/apply-export 창업성장기술개발 --template 양식.hwpx  # 양식 기반
/apply-export 창업성장기술개발 --template 양식.hwp   # 구형 양식 자동 변환
/apply-export 창업성장기술개발 --format pdf          # PDF 출력
```

### 워크플로우

```
/apply-export 실행
    │
    ▼
1단계: 소스 확인 — Markdown 최종본 + 첨부 자료
    │
    ▼
2단계: 양식 분기
  ├── --template 양식.hwp → hwp2hwpx로 HWPX 변환 후 처리
  ├── --template 양식.hwpx → 빈 필드에 내용 삽입
  └── 양식 없음 → 표준 템플릿으로 신규 생성
    │
    ▼
3단계: HWPX 생성 (hwp-generator MCP 서버)
  - 제목/본문 스타일 매핑, 표 변환, 이미지 삽입
  - 페이지 번호, 머리말/꼬리말
  - 페이지/글자수 제한 검증
    │
    ▼
4단계: 검증 및 출력 → ./output/파일명.hwpx
```

### hwp-generator MCP 서버

`.mcp.json`에 사전 구성되는 로컬 MCP 서버.

```json
{
  "mcpServers": {
    "hwp-generator": {
      "command": "python",
      "args": ["hwp_server/main.py"]
    }
  }
}
```

#### MCP 도구

| 도구 | 기능 |
|------|------|
| `create_document` | 빈 HWPX 문서 생성 (용지, 여백, 기본 스타일) |
| `add_heading` | 제목 삽입 (수준 1~3) |
| `add_paragraph` | 본문 텍스트 삽입 (볼드, 이탤릭, 밑줄) |
| `add_table` | 표 삽입 (행/열, 병합, 셀 스타일) |
| `add_image` | 이미지 삽입 (크기, 위치) |
| `fill_template` | 기존 양식 HWPX의 빈 필드에 내용 삽입 |
| `set_page_setup` | 용지 크기, 여백, 머리말/꼬리말 |
| `convert_hwp_to_hwpx` | 구형 .hwp → .hwpx 변환 (Java 서브프로세스) |
| `export_file` | 최종 HWPX 파일 저장 |

#### 기술 스택

```
hwp-generator MCP 서버
├── Python (메인)
│   ├── lxml              # HWPX XML 처리
│   ├── Pillow            # 이미지 처리
│   └── mcp (python-sdk)  # MCP 프로토콜
│
└── Java (서브프로세스, HWP→HWPX 변환 시에만)
    ├── hwp2hwpx           # HWP → HWPX 변환
    ├── kr.dogfoot.hwplib  # HWP 파싱
    └── kr.dogfoot.hwpxlib # HWPX 생성
```

Java 런타임이 없는 환경에서는 변환 기능을 건너뛰고 HWPX만 지원하도록 graceful fallback.

### hwp-format 스킬

자동 활성화 시 제공:
- HWPX 파일 구조 (XML 스키마) 가이드
- 한국 정부 공문서 서식 표준 (글꼴: 함초롬바탕/돋움, 크기, 줄간격)
- 사업계획서 레이아웃 규칙
- 양식 파싱 시 빈 필드 탐지 패턴

### 한계 및 대안

| 상황 | 대응 |
|------|------|
| 구형 .hwp 양식 입력 | hwp2hwpx(Java)로 자동 변환 후 처리 |
| 복잡한 양식 (다단, 특수 레이아웃) | 파싱 실패 시 Markdown 초안 + 수동 복붙 안내로 폴백 |
| python-hwpx 미지원 기능 | LibreOffice headless 변환을 백업 경로로 제공 |

---

## 구현 단계 (예상)

| 단계 | 범위 | 산출물 |
|------|------|--------|
| 1단계 | 지식베이스 구조화 | `/kb-init`, `/kb-update`, kb-extractor 에이전트, kb-structure 스킬 |
| 2단계 | 사업계획서 자동화 | `/apply-write`, `/apply-update`, bizplan-writer 에이전트, bizplan-writing 스킬 |
| 3단계 | 소싱/적합도/리포트 | `/apply-find`, `/apply-check`, `/apply-daily`, program-sourcer, suitability-analyzer 에이전트 |
| 4단계 | HWP 파일 생성 | `/apply-export`, hwp-generator MCP 서버, hwp-format 스킬 |
