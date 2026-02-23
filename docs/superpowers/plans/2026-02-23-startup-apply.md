# startup-apply 플러그인 구현 계획

> **For Claude:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 지식베이스 기반 지원사업 사업계획서 자동 작성 플러그인을 구축한다.

**Architecture:** startup-fundraise 플러그인과 동일한 구조(commands/, skills/, agents/)를 따른다. 지식베이스 → 사업계획서 → 소싱/리포트 → HWP 생성 순서로 4단계에 걸쳐 구현한다. HWP 생성은 별도 Python MCP 서버(hwp_server/)로 분리한다.

**Tech Stack:** Claude Code Plugin (Markdown), Python MCP Server (lxml, mcp python-sdk), Java (hwp2hwpx, 선택적)

**Spec:** `docs/superpowers/specs/2026-02-23-startup-apply-design.md`

---

## Chunk 1: 플러그인 스캐폴드

플러그인의 뼈대를 만든다. plugin.json, .mcp.json, CONNECTORS.md, README.md 및 디렉토리 구조를 생성한다.

### Task 1: 플러그인 매니페스트 및 디렉토리 생성

**Files:**
- Create: `startup-apply/.claude-plugin/plugin.json`
- Create: `startup-apply/.mcp.json`
- Create: `startup-apply/CONNECTORS.md`
- Create: `startup-apply/README.md`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: 디렉토리 구조 생성**

```bash
mkdir -p startup-apply/.claude-plugin
mkdir -p startup-apply/commands
mkdir -p startup-apply/skills/kb-structure
mkdir -p startup-apply/skills/bizplan-writing
mkdir -p startup-apply/skills/gov-program-knowledge
mkdir -p startup-apply/skills/hwp-format
mkdir -p startup-apply/agents
```

- [ ] **Step 2: plugin.json 작성**

```json
{
  "name": "startup-apply",
  "version": "0.1.0",
  "description": "지원사업 사업계획서 자동 작성 — 지식베이스 구축, 공고 소싱, 적합도 분석, 데일리 리포트, HWP 출력. 웹 검색만으로 단독 작동하며, Notion·문서 도구 연결 시 더욱 강력해집니다.",
  "author": {
    "name": "Moonklabs"
  }
}
```

- [ ] **Step 3: .mcp.json 작성**

startup-fundraise의 패턴을 따른다. Notion(지식베이스), Slack(알림) 등 사전 구성.

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    },
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp"
    },
    "ms365": {
      "type": "http",
      "url": "https://microsoft365.mcp.claude.com/mcp"
    }
  }
}
```

- [ ] **Step 4: CONNECTORS.md 작성**

startup-fundraise/CONNECTORS.md의 구조를 따르되, 지원사업 맥락에 맞게 조정.

커넥터 테이블:

| 카테고리 | 플레이스홀더 | 포함 서버 | 기타 옵션 |
|----------|-------------|-----------|-----------|
| 지식 베이스 | `~~knowledge base` | Notion | Google Drive, Confluence |
| 문서 | `~~docs` | Microsoft 365, Notion | Google Docs |
| 데이터 보강 | `~~data enrichment` | — | 기업마당, K-Startup (웹 검색 기반) |
| 스프레드시트 | `~~spreadsheet` | Microsoft 365 | Google Sheets |
| 채팅 | `~~chat` | Slack | Microsoft Teams |

한국 지원사업 데이터 소스 안내 섹션 포함:
- 기업마당 (bizinfo.go.kr)
- K-Startup (k-startup.go.kr)
- TIPS (tips.go.kr)
- 각 지자체 지원사업 포털

- [ ] **Step 5: README.md 작성**

startup-fundraise/README.md의 구조를 따른다:
- 플러그인 한 줄 설명
- 주요 커맨드 목록 표
- 설치 방법
- 커넥터 안내 링크

- [ ] **Step 6: marketplace.json에 플러그인 추가**

`.claude-plugin/marketplace.json`의 plugins 배열에 항목 추가:

```json
{
  "name": "startup-apply",
  "source": "./startup-apply",
  "description": "지원사업 사업계획서 자동 작성 — 지식베이스 구축, 공고 소싱, 적합도 분석, 데일리 리포트, HWP 출력."
}
```

- [ ] **Step 7: Commit**

```bash
git add startup-apply/ .claude-plugin/marketplace.json
git commit -m "feat(startup-apply): 플러그인 스캐폴드 — plugin.json, .mcp.json, CONNECTORS, README"
```

---

## Chunk 2: 지식베이스 커맨드 + 스킬 + 에이전트

지식베이스 초기 구축과 갱신 기능을 구현한다.

### Task 2: kb-structure 스킬 작성

**Files:**
- Create: `startup-apply/skills/kb-structure/SKILL.md`

- [ ] **Step 1: SKILL.md 작성**

프런트매터:
```yaml
---
name: kb-structure
description: 지식베이스 구조화, 스키마 정의, 완성도 점검을 수행합니다. "지식베이스", "KB", "회사 정보 정리", "사업계획서 데이터", "knowledge base" 등의 맥락에서 자동 활성화됩니다.
---
```

본문에 포함할 내용:
- 지식베이스 7개 카테고리 스키마 (company-profile, product, market, business-model, financials, track-record, past-plans)
- 각 카테고리별 필수/선택 항목 상세
- 한국 지원사업에서 공통 요구하는 표준 항목 체크리스트
- 카테고리별 작성 가이드 (예: "TAM/SAM/SOM은 출처와 산출 근거를 반드시 포함")
- 정보 완성도 점수 산출 기준 (각 항목 가중치)
- Notion 스키마 vs 로컬 Markdown 대체 저장 구조

- [ ] **Step 2: Commit**

```bash
git add startup-apply/skills/kb-structure/
git commit -m "feat(startup-apply): kb-structure 스킬 — 지식베이스 스키마 및 구조화 규칙"
```

### Task 3: kb-extractor 에이전트 작성

**Files:**
- Create: `startup-apply/agents/kb-extractor.md`

- [ ] **Step 1: 에이전트 파일 작성**

프런트매터:
```yaml
---
name: kb-extractor
description: 과거 사업계획서, IR자료, 회사 문서에서 정보를 자동 추출하여 지식베이스 카테고리별로 분류합니다. "문서 추출", "정보 추출", "사업계획서 파싱", "KB 추출" 등의 요청 시 사용합니다.
tools: Read, Write, WebFetch
model: sonnet
---
```

본문에 포함할 내용:
- 작동 원칙: 문서를 받으면 7개 KB 카테고리에 매핑
- 실행 흐름:
  1. 문서 텍스트 추출 (HWP/Word/PDF → 텍스트)
  2. 섹션 식별 및 카테고리 매핑
  3. 정보 추출 (구조화된 데이터로 변환)
  4. 중복/충돌 감지 시 사용자 질문
- 출력 형식: 카테고리별 추출 결과 Markdown
- 병렬 실행: 여러 문서를 동시에 처리

- [ ] **Step 2: Commit**

```bash
git add startup-apply/agents/kb-extractor.md
git commit -m "feat(startup-apply): kb-extractor 에이전트 — 문서에서 KB 정보 자동 추출"
```

### Task 4: /kb-init 커맨드 작성

**Files:**
- Create: `startup-apply/commands/kb-init.md`

- [ ] **Step 1: 커맨드 파일 작성**

프런트매터:
```yaml
---
description: 회사 지식베이스를 초기 구축합니다 — 과거 문서 업로드 → 자동 추출 → 구조화 → Notion/로컬 저장
argument-hint: ""
---
```

본문 구조 (startup-fundraise/commands/daily-fundraise.md 패턴 참조):
1. 작동 방식 ASCII 박스 — 단독 사용 vs MCP 강화 모드
2. 사용법: `/kb-init`
3. 워크플로우:
   - "과거 사업계획서 파일을 올려주세요" 프롬프트
   - kb-extractor 에이전트 병렬 실행
   - 추출 결과 → 스키마 매핑 → 사용자 검토
   - 빈 항목 식별 → "지금 채우시겠습니까?"
   - Notion 저장 (또는 로컬 Markdown)
4. 강화 모드: `~~knowledge base`(Notion), `~~docs`(기존 문서 자동 탐색)
5. 출력 형식: 완성도 리포트
6. 에이전트 병렬 실행 다이어그램
7. 관련 스킬: kb-structure

- [ ] **Step 2: Commit**

```bash
git add startup-apply/commands/kb-init.md
git commit -m "feat(startup-apply): /kb-init 커맨드 — 지식베이스 초기 구축"
```

### Task 5: /kb-update 커맨드 작성

**Files:**
- Create: `startup-apply/commands/kb-update.md`

- [ ] **Step 1: 커맨드 파일 작성**

프런트매터:
```yaml
---
description: 지식베이스를 갱신합니다 — 카테고리별 업데이트, 새 문서 추출, 미갱신 항목 점검
argument-hint: "<카테고리|--from 파일|--check>"
---
```

본문 구조:
1. 작동 방식 ASCII 박스
2. 사용법:
   - `/kb-update financials` — 특정 카테고리 업데이트
   - `/kb-update --from 파일.hwp` — 새 문서에서 자동 추출
   - `/kb-update --check` — 미갱신 항목 점검
3. 워크플로우 (3가지 모드별)
4. 강화 모드: `~~knowledge base`, `~~docs`
5. 출력 형식: 변경 사항 diff + 완성도 업데이트
6. 관련 스킬: kb-structure

- [ ] **Step 2: Commit**

```bash
git add startup-apply/commands/kb-update.md
git commit -m "feat(startup-apply): /kb-update 커맨드 — 지식베이스 갱신"
```

---

## Chunk 3: 사업계획서 작성 커맨드 + 스킬 + 에이전트

### Task 6: bizplan-writing 스킬 작성

**Files:**
- Create: `startup-apply/skills/bizplan-writing/SKILL.md`

- [ ] **Step 1: SKILL.md 작성**

프런트매터:
```yaml
---
name: bizplan-writing
description: 한국 지원사업 사업계획서 작성 도메인 지식을 제공합니다. "사업계획서", "지원사업 작성", "bizplan", "사업계획서 평가", "작성 전략" 등의 맥락에서 자동 활성화됩니다.
---
```

본문에 포함할 내용:
- 사업계획서 표준 13개 섹션 구조 (기업개요 ~ 수행실적)
- 각 섹션 ← 지식베이스 카테고리 매핑 표
- 한국 지원사업 평가위원 관점 작성 가이드
- 섹션별 킬러 표현 및 피해야 할 표현
- 정량 데이터 제시 원칙 ("~할 예정" 대신 "~으로 검증됨")
- 공고 유형별 강조 포인트:
  - TIPS → 기술 혁신성 (40%)
  - 예비창업패키지 → 사업화 가능성
  - 창업성장기술개발 → 기술 개발 역량 + 시장성
  - AI 바우처 → AI 기술 적용 구체성
- 평가 배점에 따른 분량 배분 가이드
- 페이지/글자수 제한 관리 팁

- [ ] **Step 2: Commit**

```bash
git add startup-apply/skills/bizplan-writing/
git commit -m "feat(startup-apply): bizplan-writing 스킬 — 사업계획서 작성 도메인 지식"
```

### Task 7: bizplan-writer 에이전트 작성

**Files:**
- Create: `startup-apply/agents/bizplan-writer.md`

- [ ] **Step 1: 에이전트 파일 작성**

프런트매터:
```yaml
---
name: bizplan-writer
description: 지식베이스 데이터를 기반으로 사업계획서 섹션을 작성합니다. "사업계획서 섹션 작성", "사업계획서 초안", "bizplan draft" 등의 요청 시 사용합니다.
tools: Read, Write, WebSearch
model: sonnet
---
```

본문 구조 (investor-researcher.md 패턴 참조):
- 작동 원칙: 지식베이스 → 공고 요강 → 섹션별 초안
- 실행 흐름:
  1. 지식베이스에서 해당 섹션 데이터 로드
  2. 공고 평가 기준 확인
  3. 과거 문서 문체/표현 패턴 적용
  4. 초안 작성 (배점 비례 분량)
  5. 수치 교차검증
- 출력 형식: Markdown 섹션
- 병렬 실행: 독립적인 섹션 동시 작성 가능

- [ ] **Step 2: Commit**

```bash
git add startup-apply/agents/bizplan-writer.md
git commit -m "feat(startup-apply): bizplan-writer 에이전트 — 사업계획서 섹션별 작성"
```

### Task 8: /apply-write 커맨드 작성

**Files:**
- Create: `startup-apply/commands/apply-write.md`

- [ ] **Step 1: 커맨드 파일 작성**

프런트매터:
```yaml
---
description: 지원사업 사업계획서를 자동 작성합니다 — 공고 분석 → KB 매핑 → 섹션별 작성 → 최종 조립
argument-hint: "<공고명> [연도/회차]"
---
```

본문 구조:
1. 작동 방식 ASCII 박스
2. 사용법:
   - `/apply-write TIPS 2026년 상반기`
   - `/apply-write 창업성장기술개발`
   - `/apply-write TIPS --continue` (이어쓰기)
3. 4단계 워크플로우:
   - 1단계: 공고 분석 (웹 검색 → 요강/배점/양식 파악)
   - 2단계: 지식베이스 매핑 (부족 항목 식별)
   - 3단계: 섹션별 작성 (bizplan-writer 에이전트 병렬 실행)
   - 4단계: 최종 조립 (일관성 검토, 제한 준수)
4. 강화 모드: `~~knowledge base`, `~~data enrichment`, `~~docs`
5. 출력 형식: Markdown 사업계획서 + 진행률 리포트
6. 에이전트 실행 다이어그램
7. 관련 스킬: bizplan-writing, kb-structure

- [ ] **Step 2: Commit**

```bash
git add startup-apply/commands/apply-write.md
git commit -m "feat(startup-apply): /apply-write 커맨드 — 사업계획서 자동 작성"
```

### Task 9: /apply-update 커맨드 작성

**Files:**
- Create: `startup-apply/commands/apply-update.md`

- [ ] **Step 1: 커맨드 파일 작성**

프런트매터:
```yaml
---
description: 기존 사업계획서를 새 공고에 맞게 변환합니다 — 기존 문서 파싱 → 새 요강 비교 → 변경분만 재작성
argument-hint: "<기존파일> → <새 공고명>"
---
```

본문 구조:
1. 작동 방식 ASCII 박스
2. 사용법:
   - `/apply-update 기존계획서.hwp → 창업성장기술개발 2026`
   - `/apply-update 최근작성본.md → AI바우처`
3. 변환 프로세스:
   - 기존 문서 파싱 → 섹션별 분리
   - 새 공고 요강과 비교 (추가/수정/재활용 섹션 식별)
   - 지식베이스에서 최신 데이터 반영
   - 변경 부분만 새로 작성
4. 출력 형식: 변환 diff 리포트 + 새 Markdown 사업계획서
5. 관련 스킬: bizplan-writing

- [ ] **Step 2: Commit**

```bash
git add startup-apply/commands/apply-update.md
git commit -m "feat(startup-apply): /apply-update 커맨드 — 기존 사업계획서 재활용 변환"
```

---

## Chunk 4: 소싱 + 적합도 + 데일리 리포트

### Task 10: gov-program-knowledge 스킬 작성

**Files:**
- Create: `startup-apply/skills/gov-program-knowledge/SKILL.md`

- [ ] **Step 1: SKILL.md 작성**

프런트매터:
```yaml
---
name: gov-program-knowledge
description: 한국 정부/민간 지원사업 공고 체계, 평가 기준, 주요 프로그램 특성을 안내합니다. "지원사업", "정부 과제", "TIPS", "예비창업패키지", "창업성장기술개발", "공고 분석" 등의 맥락에서 자동 활성화됩니다.
---
```

본문에 포함할 내용:
- 한국 지원사업 생태계 개요 (주관기관별 분류)
- 주요 프로그램별 특성:
  - TIPS: 기술 혁신성 중심, 운영사 매칭, 최대 5억
  - 예비창업패키지: 예비 창업자, 사업화 가능성, 최대 1억
  - 초기창업패키지: 3년 이내, 최대 1억
  - 창업성장기술개발: 기술개발+사업화, 최대 3억
  - AI 바우처: AI 기술 적용, 최대 3억
  - 서울형 R&D: 서울 소재, 지자체 특화
- 평가 기준 공통 프레임워크 (기술성/시장성/사업화/팀역량 배점)
- 주요 소싱 포털 URL 목록
- 지원사업 캘린더 (월별 주요 공고 시기)
- 심사 프로세스 (서류 → 발표 → 선정) 가이드

- [ ] **Step 2: Commit**

```bash
git add startup-apply/skills/gov-program-knowledge/
git commit -m "feat(startup-apply): gov-program-knowledge 스킬 — 한국 지원사업 도메인 지식"
```

### Task 11: program-sourcer 에이전트 작성

**Files:**
- Create: `startup-apply/agents/program-sourcer.md`

- [ ] **Step 1: 에이전트 파일 작성**

프런트매터:
```yaml
---
name: program-sourcer
description: 지원사업 공고를 웹 검색으로 소싱하고 적합도 점수를 산출합니다. "지원사업 찾기", "공고 검색", "지원사업 소싱", "program sourcing" 등의 요청 시 사용합니다.
tools: WebSearch, Read
model: sonnet
---
```

본문 구조 (investor-researcher.md 패턴):
- 작동 원칙: 웹 검색 → 공고 수집 → 표준화 → 적합도 산출
- 검색 쿼리 전략:
  ```
  WebSearch: "기업마당 [업종] 지원사업 공고 2026"
  WebSearch: "K-Startup [키워드] 모집 공고"
  WebSearch: "TIPS 프로그램 [회차] 모집"
  WebSearch: "[지자체] 스타트업 지원사업 2026"
  WebSearch: "[대기업명] 오픈이노베이션 스타트업 모집"
  WebSearch: "site:bizinfo.go.kr [키워드] 공고"
  ```
- 공고 표준화 형식: 공고명, 주관기관, 마감일, 지원규모, 자격요건
- 적합도 점수 산출: 지식베이스 vs 공고 요건 매칭
- 출력: 적합도 순 정렬 표

- [ ] **Step 2: Commit**

```bash
git add startup-apply/agents/program-sourcer.md
git commit -m "feat(startup-apply): program-sourcer 에이전트 — 지원사업 웹 검색 소싱"
```

### Task 12: suitability-analyzer 에이전트 작성

**Files:**
- Create: `startup-apply/agents/suitability-analyzer.md`

- [ ] **Step 1: 에이전트 파일 작성**

프런트매터:
```yaml
---
name: suitability-analyzer
description: 특정 지원사업 공고에 대한 상세 적합도 분석을 수행합니다. "적합도 분석", "자격 요건 확인", "지원 가능성", "suitability" 등의 요청 시 사용합니다.
tools: Read, WebSearch
model: sonnet
---
```

본문 구조:
- 작동 원칙: 공고 요강 ↔ 지식베이스 대조 분석
- 분석 프레임워크 (6개 축):
  - company-profile → 기업 형태/업력/소재지
  - product.tech → 기술 혁신성/TRL
  - market → 시장 규모/성장성
  - financials → 매출/재무 건전성
  - track-record → 수행 실적/수상
  - business-model → 사업화 가능성
- 출력: 충족/보완필요/미충족 분류표 + 작성 전략 + 체크리스트

- [ ] **Step 2: Commit**

```bash
git add startup-apply/agents/suitability-analyzer.md
git commit -m "feat(startup-apply): suitability-analyzer 에이전트 — 적합도 상세 분석"
```

### Task 13: /apply-find 커맨드 작성

**Files:**
- Create: `startup-apply/commands/apply-find.md`

- [ ] **Step 1: 커맨드 파일 작성**

프런트매터:
```yaml
---
description: 지원사업 공고를 소싱합니다 — 정부/민간/지자체/해외 공고 검색 → 적합도 순 정렬
argument-hint: "[키워드] [--deadline YYYY-MM]"
---
```

본문 구조:
1. 작동 방식 ASCII 박스
2. 사용법: `/apply-find`, `/apply-find AI·SaaS`, `/apply-find --deadline 2026-04`
3. 워크플로우: program-sourcer 에이전트 → 적합도 자동 산출 → 결과 정렬
4. 출력 형식: 높은 적합도(80%+) / 검토 필요(60-79%) / 마감 임박 표
5. 강화 모드: `~~data enrichment`
6. 에이전트 실행 다이어그램
7. 관련 스킬: gov-program-knowledge

- [ ] **Step 2: Commit**

```bash
git add startup-apply/commands/apply-find.md
git commit -m "feat(startup-apply): /apply-find 커맨드 — 지원사업 소싱"
```

### Task 14: /apply-check 커맨드 작성

**Files:**
- Create: `startup-apply/commands/apply-check.md`

- [ ] **Step 1: 커맨드 파일 작성**

프런트매터:
```yaml
---
description: 특정 지원사업 공고의 상세 적합도를 분석합니다 — 자격요건 대조, 보완 항목, 작성 전략 제안
argument-hint: "<공고명>"
---
```

본문 구조:
1. 작동 방식 ASCII 박스
2. 사용법: `/apply-check TIPS`, `/apply-check 창업성장기술개발`
3. 워크플로우: 공고 요강 검색 → suitability-analyzer 에이전트 → 결과 출력
4. 출력 형식: 종합 적합도 % + 충족/보완/미충족 표 + 작성 전략 + 체크리스트
5. 관련 스킬: gov-program-knowledge, kb-structure

- [ ] **Step 2: Commit**

```bash
git add startup-apply/commands/apply-check.md
git commit -m "feat(startup-apply): /apply-check 커맨드 — 적합도 상세 분석"
```

### Task 15: /apply-daily 커맨드 작성

**Files:**
- Create: `startup-apply/commands/apply-daily.md`

- [ ] **Step 1: 커맨드 파일 작성**

프런트매터:
```yaml
---
description: 지원사업 데일리 리포트 — 마감 임박, 작성 진행률, 신규 공고, 지식베이스 상태를 한눈에
argument-hint: ""
---
```

본문 구조 (daily-fundraise.md 패턴 참조):
1. 작동 방식 ASCII 박스
2. 사용법: `/apply-daily`
3. 필요한 정보: 진행 중인 지원사업 현황 (수동 입력 or ~~knowledge base)
4. 출력 형식 (8개 섹션):
   - #1 우선순위
   - 진행 현황 (작성중/검토/제출/결과대기)
   - 마감 임박 (D-7 이내)
   - 작성 중인 사업계획서 (진행률 바)
   - 제출 완료/결과 대기
   - 신규 공고 알림
   - 지식베이스 상태 (미갱신 경고)
   - 오늘의 체크리스트
5. 파이프라인 추적 구조 (Notion DB/로컬 파일)
6. 에이전트 병렬 실행: program-sourcer, suitability-analyzer
7. 우선순위 프레임워크:
   - 마감 임박 35%
   - 작성률 낮음 30%
   - KB 미갱신 20%
   - 신규 공고 15%
8. 관련 커맨드 링크

- [ ] **Step 2: Commit**

```bash
git add startup-apply/commands/apply-daily.md
git commit -m "feat(startup-apply): /apply-daily 커맨드 — 지원사업 데일리 리포트"
```

---

## Chunk 5: HWP 생성 — 스킬 + 커맨드

HWP MCP 서버는 별도 구현 계획으로 분리한다. 이 청크에서는 스킬과 커맨드(MCP 서버 호출 인터페이스)만 작성한다.

### Task 16: hwp-format 스킬 작성

**Files:**
- Create: `startup-apply/skills/hwp-format/SKILL.md`

- [ ] **Step 1: SKILL.md 작성**

프런트매터:
```yaml
---
name: hwp-format
description: HWP/HWPX 파일 형식 및 한국 공문서 서식 규칙을 안내합니다. "HWP", "HWPX", "한글 파일", "문서 내보내기", "파일 변환" 등의 맥락에서 자동 활성화됩니다.
---
```

본문에 포함할 내용:
- HWPX 파일 구조 (ZIP + XML) 설명
- HWP vs HWPX 차이 및 호환성
- 한국 정부 공문서 서식 표준:
  - 글꼴: 함초롬바탕 (본문), 함초롬돋움 (제목)
  - 크기: 제목 16pt, 소제목 13pt, 본문 11pt
  - 줄간격: 160~180%
  - 여백: 상 20mm, 하 15mm, 좌우 20mm
- 사업계획서 레이아웃 규칙 (표지, 목차, 본문, 부록)
- hwp2hwpx(Java) 변환 안내
- 양식 파싱 시 빈 필드 탐지 패턴
- MCP 서버 도구 참조 가이드

- [ ] **Step 2: Commit**

```bash
git add startup-apply/skills/hwp-format/
git commit -m "feat(startup-apply): hwp-format 스킬 — HWP/HWPX 파일 형식 도메인 지식"
```

### Task 17: /apply-export 커맨드 작성

**Files:**
- Create: `startup-apply/commands/apply-export.md`

- [ ] **Step 1: 커맨드 파일 작성**

프런트매터:
```yaml
---
description: 사업계획서를 HWP 파일로 내보냅니다 — Markdown → HWPX 변환, 양식 기반 작성, PDF 출력
argument-hint: "<공고명> [--template 양식파일] [--format hwpx|pdf]"
---
```

본문 구조:
1. 작동 방식 ASCII 박스
2. 사용법:
   - `/apply-export 창업성장기술개발` — HWPX 생성
   - `/apply-export TIPS --template 양식.hwpx` — 양식 기반
   - `/apply-export TIPS --template 양식.hwp` — 구형 양식 자동 변환
   - `/apply-export TIPS --format pdf` — PDF 출력
3. 워크플로우:
   - 소스 확인 (Markdown 최종본)
   - 양식 분기 (.hwp 자동 변환 / .hwpx 필드 삽입 / 신규 생성)
   - HWPX 생성 (hwp-generator MCP 서버 도구 호출)
   - 검증 및 출력
4. MCP 도구 참조 표:
   - `create_document`, `add_heading`, `add_paragraph`, `add_table`
   - `add_image`, `fill_template`, `set_page_setup`
   - `convert_hwp_to_hwpx`, `export_file`
5. 한계 및 폴백:
   - 복잡한 양식 → Markdown + 수동 복붙 안내
   - Java 런타임 없음 → HWPX만 지원 안내
6. 관련 스킬: hwp-format

- [ ] **Step 2: Commit**

```bash
git add startup-apply/commands/apply-export.md
git commit -m "feat(startup-apply): /apply-export 커맨드 — HWP 파일 생성"
```

### Task 18: 최종 커밋 및 검증

- [ ] **Step 1: 전체 파일 구조 확인**

```bash
find startup-apply -type f | sort
```

기대하는 파일 목록:
```
startup-apply/.claude-plugin/plugin.json
startup-apply/.mcp.json
startup-apply/CONNECTORS.md
startup-apply/README.md
startup-apply/agents/bizplan-writer.md
startup-apply/agents/kb-extractor.md
startup-apply/agents/program-sourcer.md
startup-apply/agents/suitability-analyzer.md
startup-apply/commands/apply-check.md
startup-apply/commands/apply-daily.md
startup-apply/commands/apply-export.md
startup-apply/commands/apply-find.md
startup-apply/commands/apply-update.md
startup-apply/commands/apply-write.md
startup-apply/commands/kb-init.md
startup-apply/commands/kb-update.md
startup-apply/skills/bizplan-writing/SKILL.md
startup-apply/skills/gov-program-knowledge/SKILL.md
startup-apply/skills/hwp-format/SKILL.md
startup-apply/skills/kb-structure/SKILL.md
```

- [ ] **Step 2: marketplace.json 검증**

marketplace.json에 startup-apply 항목이 포함되어 있는지 확인.

- [ ] **Step 3: 플러그인 설치 테스트**

```bash
# 개발용 마켓플레이스에서 플러그인 확인
# Claude Code 재시작 후 /kb-init, /apply-daily 등 커맨드 노출 확인
```

---

## 후속 계획 (별도 구현)

HWP MCP 서버(`hwp_server/`)는 별도의 설계 → 구현 사이클이 필요하다:

1. **hwp_server 설계**: Python MCP 서버 구조, HWPX XML 생성 로직, hwp2hwpx Java 통합
2. **hwp_server TDD 구현**: MCP 도구별 테스트 → 구현 → 통합 테스트
3. **플러그인 통합**: `.mcp.json`에 hwp-generator 로컬 서버 추가, `/apply-export` 실제 연동

이는 현재 플러그인(커맨드/스킬/에이전트)이 완성된 후 진행한다.
