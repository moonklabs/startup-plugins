---
description: Go-to-Market 전략을 수립합니다 — GTM 모션, ICP, 채널, 가격, 90일 실행 계획
argument-hint: "<제품 또는 시장>"
---

# /gtm-plan

> 익숙하지 않은 플레이스홀더가 보이거나 연결된 도구를 확인하려면 [CONNECTORS.md](../CONNECTORS.md)를 참조하세요.

Go-to-Market (GTM) 전략 수립 커맨드입니다. 제품과 시장에 최적화된 GTM 모션 선정, ICP 정의, 채널 우선순위, 가격 패키징, 90일 실행 계획을 포함한 종합 GTM 전략을 생성합니다.

## 사용법

```bash
/gtm-plan                      # 대화형으로 정보 수집
/gtm-plan "B2B SaaS CRM"       # 제품 지정
/gtm-plan "중소기업 회계"       # 시장 지정
```

## 작동 방식

```
┌─────────────────────────────────────────────────────────────────┐
│                      GTM PLAN GENERATOR                          │
├─────────────────────────────────────────────────────────────────┤
│  기본 기능 (단독 작동)                                            │
│  ✓ 5가지 GTM 모션 중 최적 조합 선정                               │
│  ✓ ICP (Ideal Customer Profile) 3-5개 세그먼트 정의             │
│  ✓ PESO 채널 전략 (Paid/Earned/Shared/Owned)                   │
│  ✓ 가격 패키징 권장 (Good/Better/Best)                           │
│  ✓ 90일 실행 로드맵 (Week 1-4/5-8/9-12)                         │
│  ✓ KPI 및 성공 지표 설정                                          │
├─────────────────────────────────────────────────────────────────┤
│  강화 모드 (도구 연결 시)                                         │
│  + ~~analytics: 기존 채널 성과 데이터 분석                        │
│  + ~~CRM: ICP별 Win Rate 및 CAC 검증                            │
│  + ~~knowledge base: 기존 GTM 자료 참조                         │
└─────────────────────────────────────────────────────────────────┘
```

## 필요한 정보

### 1단계: 제품/시장 입력

**제품 정보**:
- 제품/서비스 설명 (한 줄)
- 카테고리 (SaaS, 마켓플레이스, 컨슈머, B2B)
- 주요 기능 (Top 3)
- 핵심 가치 제안

**시장 정보**:
- 타겟 고객 (B2B/B2C, 산업, 규모)
- 지역 (한국, 미국, 글로벌)
- 시장 성숙도 (신생, 성장, 성숙)

**현재 단계**:
- 투자 라운드 (Pre-seed, Seed, Series A/B)
- 팀 규모
- 현재 트랙션 (고객 수, MRR/GMV)

**기존 GTM 활동** (있다면):
- 현재 채널 (웹사이트, SNS, 광고)
- 고객 획득 방식
- CAC, Conversion Rate

### 2단계: 관련 스킬 자동 활성화

문서 생성 중 다음 스킬 백그라운드 활용:

| 분석 영역 | 활성화 스킬 | 목적 |
|-----------|-------------|------|
| GTM 모션 | **gtm-strategy** | 5가지 모션 평가 및 선정 |
| 가격 전략 | **pricing-strategy** | 가격 모델 및 패키징 |
| 경쟁 분석 | **competitive-landscape** | 경쟁사 GTM 분석 |
| 세일즈 | **sales-playbook** | Sales-Led 프로세스 |

## 출력 형식

### GTM 전략 문서

```markdown
# [제품명] Go-to-Market 전략

**작성일**: YYYY년 M월 D일
**대상**: [팀 내부 / 투자자 / 이사회]
**현재 단계**: [Pre-seed / Seed / Series A]

---

## 목차
1. [Executive Summary](#1-executive-summary)
2. [GTM 모션 전략](#2-gtm-모션-전략)
3. [ICP (Ideal Customer Profile)](#3-icp-ideal-customer-profile)
4. [채널 전략 (PESO)](#4-채널-전략-peso)
5. [가격 패키징](#5-가격-패키징)
6. [90일 실행 계획](#6-90일-실행-계획)
7. [KPI 및 성공 지표](#7-kpi-및-성공-지표)
8. [예산 배분](#8-예산-배분)

---

## 1. Executive Summary

### One-liner
[제품 한 줄 설명]

### GTM 모션
- **Primary**: [PLG/Sales-Led/Community-Led/Content-Led/Founder-Led]
- **Secondary**: [...]
- **근거**: [왜 이 조합인가]

### 타겟 시장
- **ICP**: [주요 고객 프로필]
- **TAM/SAM/SOM**: $[X]M / $[Y]M / $[Z]M (3년)
- **지역**: [한국 / 미국 / 글로벌]

### 핵심 채널 (Top 3)
1. **[채널 1]**: [전략 요약]
2. **[채널 2]**: [...]
3. **[채널 3]**: [...]

### 90일 목표
- **MRR/GMV**: $[현재] → $[목표] ([배수]x)
- **고객 수**: [현재] → [목표]
- **채널별 CAC**: < $[목표]

---

## 2. GTM 모션 전략

### 선정된 모션

#### Primary: [모션명]

**정의**: [모션 설명]

**선정 이유**:
- ✅ [이유 1]: [상세]
- ✅ [이유 2]: [상세]
- ✅ [이유 3]: [상세]

**핵심 지표**:
| 지표 | 목표 | 벤치마크 |
|------|------|----------|
| [지표 1] | [목표] | [업계 평균] |
| [지표 2] | [목표] | [업계 평균] |
| [지표 3] | [목표] | [업계 평균] |

**실행 전략**:
1. **[전략 1]**: [구체적 액션]
2. **[전략 2]**: [...]
3. **[전략 3]**: [...]

#### Secondary: [모션명]

**정의**: [모션 설명]

**역할**: Primary 보완 ([어떻게])

**리소스 배분**: 20-30%

**예시**:
```
Primary: PLG (70% 리소스)
  - 무료 Trial → Self-serve 전환
  - Product Analytics로 PQL 식별

Secondary: Content-Led (30% 리소스)
  - SEO 블로그로 Inbound 트래픽
  - Trial 가입 전환
```

### 조합 근거

**제품 특성 분석**:
| 특성 | 값 | 최적 모션 |
|------|-----|----------|
| **복잡도** | [Simple/Complex] | [모션] |
| **ACV** | $[금액] | [모션] |
| **Self-serve 가능** | [Yes/No] | [모션] |
| **네트워크 효과** | [Yes/No] | [모션] |

**단계별 진화**:
- **Now (Seed)**: Founder-led + Content
  - 이유: 예산 제한, 브랜드 구축
- **Next (Series A)**: Content + PLG
  - 이유: 제품 성숙, Self-serve 준비
- **Future (Series B)**: PLG + Sales-Led
  - 이유: Enterprise 확장

---

## 3. ICP (Ideal Customer Profile)

### Primary ICP

**기본 정보**:
- **회사 유형**: [B2B/B2C, 산업]
- **회사 규모**: [직원 수 범위]
- **매출 규모**: [연매출 범위]
- **지역**: [지역]

**Firmographics** (B2B):
- **산업**: [제조, 금융, 리테일 등]
- **직원 수**: [50-200명]
- **매출**: [₩100억-500억]
- **IT 성숙도**: [ERP 사용, 클라우드 전환 중]

**Demographics** (B2C):
- **연령**: [25-40세]
- **직업**: [직장인, 전문직]
- **소득**: [상위 30%]
- **거주지**: [수도권]

**Psychographics** (태도/행동):
- **Pain Point**: [핵심 고민]
- **구매 동기**: [효율성, 비용 절감, 성장]
- **기술 수용도**: [Early Adopter / Majority]

**Buying Behavior**:
- **의사결정자**: [CEO, CTO, CFO]
- **구매 프로세스**: [단계 수, 소요 시간]
- **예산 주기**: [분기, 연말]

### Secondary ICP (2-3개)

**ICP #2**: [간략 설명]
- 차이점: [Primary 대비]
- 우선순위: [낮음, 6개월 후 공략]

**ICP #3**: [간략 설명]
- 차이점: [...]
- 우선순위: [...]

### Anti-ICP (피해야 할 고객)

**특징**:
- ❌ [특징 1]: [왜 안 맞는지]
- ❌ [특징 2]: [...]

**예시**:
- ❌ Enterprise (직원 1,000+): 구매 주기 1년+, 우리 리소스 부족
- ❌ Consumer (개인): LTV 낮음, CAC 회수 불가

---

## 4. 채널 전략 (PESO)

### PESO 배분

| 채널 유형 | 비중 | 예산 | 주요 채널 |
|-----------|------|------|-----------|
| **Paid** | [%] | $[금액]/월 | [채널명] |
| **Earned** | [%] | $[금액]/월 | [채널명] |
| **Shared** | [%] | $[금액]/월 | [채널명] |
| **Owned** | [%] | $[금액]/월 | [채널명] |

### Top 3 채널 상세

#### 1. [채널명] (Owned/Shared/Paid/Earned)

**타겟**: [ICP 세그먼트]

**전략**:
- **목표**: [MAU, MQL, Conversion]
- **콘텐츠**: [유형, 주기]
- **Distribution**: [배포 방식]

**실행 계획** (90일):
- **Week 1-4**: [초기 셋업]
- **Week 5-8**: [콘텐츠 발행]
- **Week 9-12**: [최적화]

**예산**:
- Setup: $[금액]
- Monthly: $[금액]
- Total (90일): $[금액]

**KPI**:
| 지표 | 30일 | 60일 | 90일 |
|------|------|------|------|
| Traffic | [목표] | [목표] | [목표] |
| MQL | [목표] | [목표] | [목표] |
| CAC | <$[목표] | <$[목표] | <$[목표] |

#### 2. [채널명]

[위와 동일한 구조]

#### 3. [채널명]

[위와 동일한 구조]

### 콘텐츠 전략

#### 콘텐츠 피라미드

```
     🔺 Pillar (월 1-2개)
    /  \   - 5,000+ 단어 가이드
   /    \  - SEO 최적화
  / Derivative\ (주 3-5개)
 /   Content   \ - 블로그, 비디오
──────────────────
   Atomic (일 1-3개)
  - 소셜 포스트
```

#### 주간 콘텐츠 캘린더

| 요일 | 채널 | 콘텐츠 유형 | 주제 |
|------|------|-------------|------|
| 월 | 블로그 | How-to | [주제] |
| 화 | LinkedIn | Insight | [주제] |
| 수 | 이메일 | Newsletter | [주제] |
| 목 | X (Twitter) | Thread | [주제] |
| 금 | 유튜브 | 튜토리얼 | [주제] |

---

## 5. 가격 패키징

### 가격 모델

**선정 모델**: [Per-Seat/Usage/Flat/Tiered/Hybrid]

**선정 이유**:
- [이유 1]: [상세]
- [이유 2]: [...]

### 3-Tier 패키징 (Good/Better/Best)

```
┌──────────────┬──────────────┬──────────────┐
│   Starter    │     Pro      │  Enterprise  │
│   (Good)     │  (Better)    │    (Best)    │
├──────────────┼──────────────┼──────────────┤
│  $[X]/월     │  $[Y]/월     │  Contact Us  │
│              │ Most Popular │              │
│              │              │              │
│ • [기능 1]    │ • All Starter│ • All Pro    │
│ • [기능 2]    │ • [기능 A]    │ • [기능 X]    │
│ • [제한]      │ • [제한]      │ • Unlimited  │
└──────────────┴──────────────┴──────────────┘
```

**타겟 Mix**:
- Starter: 20% (Entry)
- Pro: 60% (**Target**, Most Popular)
- Enterprise: 20% (High-value)

**Blended ARPA**: $[금액]/월

### Pricing Strategy

**연간 할인**: 15-20%
- Monthly: $[X]/월 × 12 = $[Y]/년
- Annual: $[Z]/년 (17% 할인)

**Volume Discount**:
- 10-50 users: 10% 할인
- 50-100 users: 15% 할인
- 100+ users: Custom

**Free Trial**: 14일 (신용카드 불필요)

---

## 6. 90일 실행 계획

### Week 1-4: Foundation (기반 구축)

**목표**: GTM 인프라 셋업, 초기 트래픽

**액션**:
- [ ] **채널 셋업**:
  - 블로그 론칭 (WordPress/Ghost)
  - LinkedIn/X 계정 최적화
  - Email Tool (Mailchimp/ConvertKit)
- [ ] **콘텐츠 제작**:
  - Pillar Content 1개 발행
  - Derivative 5개 준비
- [ ] **Analytics**:
  - Google Analytics 설정
  - UTM 파라미터 표준화
  - CRM 통합 (HubSpot/Pipedrive)
- [ ] **팀**:
  - Marketer 1명 채용 시작
  - Freelance Writer 계약

**KPI (Week 4)**:
- Website Traffic: 100 visits/day
- Email Subscribers: 50
- MQL: 5

**예산**: $5K
- Tool: $2K
- Content: $2K
- Ads (실험): $1K

### Week 5-8: Launch (출시 및 확산)

**목표**: 콘텐츠 배포 가속, Paid 실험

**액션**:
- [ ] **콘텐츠 발행**:
  - Pillar 1개 추가
  - Derivative 주 3-5개
  - Atomic 일 1-3개
- [ ] **Paid 캠페인**:
  - Google Ads (Brand + Generic)
  - LinkedIn Ads (Sponsored Content)
  - Retargeting 설정
- [ ] **Partnerships**:
  - 게스트 블로깅 3개
  - Podcast 게스트 1회
- [ ] **Conversion 최적화**:
  - Landing Page A/B 테스트
  - CTA 최적화

**KPI (Week 8)**:
- Traffic: 300 visits/day
- Email: 200 subscribers
- MQL: 20
- Trial Signups: 10

**예산**: $8K
- Paid Ads: $5K
- Content: $2K
- Tools: $1K

### Week 9-12: Optimize (최적화 및 확장)

**목표**: 데이터 분석, 최적화, Q2 준비

**액션**:
- [ ] **데이터 분석**:
  - 채널별 ROI 분석
  - Conversion Funnel 최적화
  - Churn 원인 파악
- [ ] **Scaling**:
  - Top 성과 채널 예산 2x
  - 하위 채널 중단 또는 Pivot
  - SEO 콘텐츠 확대
- [ ] **Team**:
  - Marketer 온보딩 완료
  - SDR 채용 시작 (Series A 이상)
- [ ] **Q2 Planning**:
  - 90일 회고
  - Q2 GTM 로드맵 수정

**KPI (Week 12)**:
- Traffic: 500 visits/day
- Email: 500 subscribers
- MQL: 40
- Customers: 5-10
- MRR: $5K-10K

**예산**: $12K
- Paid Ads: $8K (Scaling)
- Content: $3K
- Tools: $1K

### 90일 총 예산: $25K

---

## 7. KPI 및 성공 지표

### North Star Metric

**[ARR/MRR/GMV/MAU]**: [현재] → [90일 목표] ([배수]x)

### 채널별 KPI

| 채널 | 지표 | 30일 | 60일 | 90일 |
|------|------|------|------|------|
| **SEO/블로그** | Organic Traffic | 100/day | 300/day | 500/day |
| | MQL | 5 | 15 | 30 |
| | CAC | <$100 | <$80 | <$50 |
| **LinkedIn Ads** | Impressions | 10K | 30K | 50K |
| | MQL | 10 | 20 | 40 |
| | CAC | <$150 | <$120 | <$100 |
| **이메일** | Subscribers | 50 | 200 | 500 |
| | Open Rate | >20% | >22% | >25% |
| | MQL | 2 | 10 | 20 |

### Funnel Metrics

**파이프라인 퍼널** (90일 목표):
```
Website Visitors: 15,000
  ↓ 3%
Leads: 450
  ↓ 20%
MQL: 90
  ↓ 30%
Trial/Demo: 27
  ↓ 30%
Customers: 8

CAC: $3,125 (예산 $25K ÷ 8)
LTV: $15,000 (ARPA $500 × 30개월)
LTV:CAC: 4.8:1 ✅
```

### Success Criteria (성공 기준)

**Must-Have** (필수):
- [ ] 90일 MRR: >$5K
- [ ] 고객 수: >5
- [ ] CAC < LTV/3
- [ ] 1개 채널 PMF (Channel-Market Fit)

**Nice-to-Have** (선택):
- [ ] NPS > 30
- [ ] Churn < 5%/월
- [ ] Organic 트래픽 > Paid

---

## 8. 예산 배분

### 총 90일 예산: $[X]K

**카테고리별 배분**:
| 카테고리 | 금액 | 비중 | 용도 |
|----------|------|------|------|
| **Paid Ads** | $[X]K | [%] | Google, LinkedIn, Retargeting |
| **Content** | $[X]K | [%] | Writer, Designer, Video |
| **Tools** | $[X]K | [%] | Analytics, CRM, Email, SEO |
| **Team** | $[X]K | [%] | Marketer 급여 (일부) |
| **Events** | $[X]K | [%] | Webinar, Meetup |
| **Contingency** | $[X]K | [%] | 예비비 |

**월별 Burn Rate**:
- Month 1: $[X]K (Setup)
- Month 2: $[X]K (Launch)
- Month 3: $[X]K (Scale)

**ROI 목표**:
- CAC: <$[목표]
- Payback: <[N]개월
- LTV:CAC: >[X]:1

---

## 부록

### A. 경쟁사 GTM 분석
[링크 또는 요약]

### B. ICP Persona 상세
[링크]

### C. 콘텐츠 캘린더 (Q1)
[링크]

### D. 배틀카드 (Top 3 경쟁사)
[링크]

---

**다음 단계**:
1. ✅ GTM 계획 승인 받기 (팀/이사회)
2. ⏭️ Week 1 액션 아이템 시작
3. ⏭️ 주간 GTM 미팅 캘린더 설정
```

## 워크플로우

### 1단계: 입력 수집 (10분)

대화형 질문:
1. "어떤 제품/서비스인가요?" (한 줄 설명)
2. "주요 고객은?" (B2B/B2C, 산업, 규모)
3. "현재 단계는?" (Pre-seed/Seed/Series A)
4. "현재 트랙션은?" (고객 수, MRR)
5. "기존 GTM 활동은?" (채널, CAC)

**~~knowledge base** 연결 시:
- 기존 피치 덱에서 ICP 추출
- 재무 모델에서 ARPA 참조

### 2단계: GTM 모션 분석 (자동)

**gtm-strategy 스킬 활성화**:
```python
# 제품 특성 평가
complexity = analyze_complexity(product)
acv = estimate_acv(product, icp)
self_serve = check_self_serve(product)

# 최적 모션 선정
primary_motion = select_motion(complexity, acv, self_serve, stage)
secondary_motion = select_secondary(primary_motion, budget)
```

### 3단계: ICP 정의 (자동)

**입력 기반 ICP 생성**:
- Firmographics (B2B) 또는 Demographics (B2C)
- Pain Point (제품 가치 제안 역산)
- Buying Behavior (ACV 기반 프로세스 추정)

### 4단계: 채널 전략 (자동)

**PESO 배분 결정**:
```python
if stage == "Pre-seed":
    peso = {"Paid": 10%, "Earned": 20%, "Shared": 30%, "Owned": 40%}
elif stage == "Seed":
    peso = {"Paid": 20%, "Earned": 20%, "Shared": 30%, "Owned": 30%}
elif stage == "Series A":
    peso = {"Paid": 35%, "Earned": 15%, "Shared": 25%, "Owned": 25%}
```

**Top 3 채널 선정**:
- GTM 모션별 최적 채널
- 예산 고려
- ICP 접근성

### 5단계: 가격 패키징 (자동)

**pricing-strategy 스킬 활성화**:
- 가격 모델 추천
- 3-Tier 패키징 생성
- Blended ARPA 계산

### 6단계: 90일 계획 (템플릿)

**Week 1-4/5-8/9-12 구조**:
- 각 구간별 목표
- 액션 체크리스트
- KPI 목표
- 예산

### 7단계: KPI 설정 (자동)

**벤치마크 기반**:
- startup-metrics 스킬에서 목표 수치
- 채널별 전환율 (업계 평균)
- Funnel 계산 (역산)

### 8단계: 문서 저장

**파일명**: `gtm-plan-[회사명]-YYYY-MM-DD.md`

**저장 위치**: `docs/gtm/`

**Git Commit**: "Add GTM Plan for Q[X] YYYY"

## 연결 가능한 도구

| 도구 카테고리 | 플레이스홀더 | 용도 | 예시 도구 |
|---------------|-------------|------|-----------|
| 분석 플랫폼 | `~~analytics` | 기존 채널 성과 분석 | Google Analytics, Mixpanel |
| CRM | `~~CRM` | ICP별 Win Rate, CAC | HubSpot, Pipedrive |
| 지식 베이스 | `~~knowledge base` | 기존 GTM 자료 참조 | Notion, Confluence |
| 스프레드시트 | `~~spreadsheet` | 예산 모델링 | Google Sheets |

## 팁

- **Focus**: 3개 채널 집중이 10개 분산보다 효과적
- **Data-Driven**: 60일 실험 후 데이터 기반 Pivot
- **Iteration**: 첫 GTM은 가설, 90일마다 업데이트
- **Budget**: 초기 20-30% CAC 높아도 OK (학습 비용)
- **Team**: GTM 전략은 마케터만이 아닌 창업팀 전체 책임
- **Competitor**: 경쟁사 GTM 참고하되 복사 금지 (차별화)
- **Stage-적합**: Seed와 Series A는 다른 전략 (예산, 팀, 목표)
- **Channel-Market Fit**: 1개 채널이라도 PMF 달성이 우선

## 관련 스킬

- **gtm-strategy**: GTM 모션 및 콘텐츠 전략 (자동 호출)
- **pricing-strategy**: 가격 패키징 (자동 호출)
- **sales-playbook**: Sales-Led 프로세스 상세
- **competitive-landscape**: 경쟁사 GTM 분석

## 관련 커맨드

- **/business-case**: GTM 계획을 비즈니스 케이스에 통합
- **/investor-outreach**: GTM 전략을 VC 피치에 활용
- **/pitch-review**: GTM 슬라이드 검토
