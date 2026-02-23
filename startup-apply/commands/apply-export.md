---
description: 사업계획서를 HWP 파일로 내보냅니다 — Markdown → HWPX 변환, 양식 기반 작성, PDF 출력
argument-hint: "<공고명> [--template 양식파일] [--format hwpx|pdf]"
---

# /apply-export

> 익숙하지 않은 플레이스홀더가 보이거나 연결된 도구를 확인하려면 [CONNECTORS.md](../CONNECTORS.md)를 참조하세요.

완성된 사업계획서 Markdown을 HWPX 파일로 변환합니다. 공고에서 제공하는 양식 파일이 있으면 해당 양식에 내용을 자동으로 채웁니다.

## 사용법

```
/apply-export 창업성장기술개발                           # HWPX 생성
/apply-export TIPS --template 양식.hwpx                # 양식 기반 (HWPX 양식)
/apply-export TIPS --template 양식.hwp                 # 양식 기반 (구형 HWP 자동 변환)
/apply-export 창업성장기술개발 --format pdf              # PDF 출력
```

---

## 작동 방식

```
┌─────────────────────────────────────────────────────────────────┐
│                     APPLY EXPORT                                 │
├─────────────────────────────────────────────────────────────────┤
│  기본 모드 (양식 없음)                                            │
│  ✓ 표준 사업계획서 HWPX 템플릿으로 신규 생성                       │
│  ✓ 한국 정부 공문서 서식 자동 적용                                │
│    (함초롬바탕, 11pt, 줄간격 160%, A4, 표준 여백)                │
├─────────────────────────────────────────────────────────────────┤
│  양식 모드 (--template)                                          │
│  ✓ .hwp 입력 → hwp2hwpx(Java)로 HWPX 자동 변환                  │
│  ✓ .hwpx 입력 → 빈 필드 자동 탐지 및 내용 삽입                   │
│  ✓ 원본 양식의 서식/레이아웃 유지                                  │
├─────────────────────────────────────────────────────────────────┤
│  hwp-generator MCP 서버 필요                                     │
│  MCP 서버 미실행 시: Markdown 초안 + 수동 안내로 fallback         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4단계 워크플로우

```
/apply-export 창업성장기술개발
        │
        ▼
1단계: 소스 확인
  사업계획서 Markdown 파일 로드
  이미지, 표, 차트 등 첨부 자료 확인
        │
        ▼
2단계: 양식 분기
  ├── --template 양식.hwp
  │     → convert_hwp_to_hwpx 도구로 변환
  │     → fill_template 도구로 내용 삽입
  ├── --template 양식.hwpx
  │     → fill_template 도구로 내용 삽입
  └── 양식 없음
        → create_document 도구로 신규 생성
        → 표준 서식 적용
        │
        ▼
3단계: HWPX 생성 (hwp-generator MCP 서버)
  - add_heading: 제목 구조 생성
  - add_paragraph: 본문 텍스트 삽입
  - add_table: 표 변환
  - add_image: 이미지 삽입
  - set_page_setup: 페이지/여백/머리말 설정
  - 페이지 수 / 글자수 제한 검증
        │
        ▼
4단계: 검증 및 출력
  파일 정상 생성 확인
  페이지 수 / 용량 리포트
  → ./output/[공고명]_[날짜].hwpx
```

---

## MCP 도구 참조

hwp-generator MCP 서버에서 제공하는 도구 (`skills/hwp-format/SKILL.md` 참조):

| 도구 | 사용 시점 |
|------|---------|
| `convert_hwp_to_hwpx` | HWP 양식 파일 변환 |
| `create_document` | 양식 없는 신규 문서 생성 |
| `fill_template` | 양식 빈 필드 자동 채우기 |
| `add_heading` | 제목/소제목 삽입 |
| `add_paragraph` | 본문 텍스트 삽입 |
| `add_table` | 표 삽입 |
| `add_image` | 이미지 삽입 |
| `set_page_setup` | 페이지 설정 |
| `export_file` | 최종 파일 저장 |

---

## 출력 예시

```
✅ HWPX 생성 완료

파일: ./output/창업성장기술개발_2026_Moonklabs.hwpx
페이지 수: 23페이지 (제한: 25페이지 이내 ✅)
파일 크기: 2.1 MB

→ 한컴오피스에서 열어 최종 확인 후 제출하세요.
→ .hwp로 변환 필요 시: 한컴오피스에서 "다른 이름으로 저장 → HWP"
```

---

## 한계 및 폴백

| 상황 | 대응 |
|------|------|
| hwp-generator MCP 서버 미실행 | Markdown 초안 출력 + 한컴오피스에서 수동 작업 안내 |
| 복잡한 양식 파싱 실패 | 섹션별 Markdown + 양식에 수동 복붙 안내 |
| Java 미설치 (HWP→HWPX 변환 불가) | HWPX 직접 생성으로 fallback |
| 구형 기관 .hwp만 수락 | HWPX 생성 후 "한컴오피스에서 .hwp로 저장" 안내 |

---

## hwp-generator MCP 서버 설정

이 커맨드를 완전히 사용하려면 로컬 MCP 서버가 필요합니다:

```bash
# 저장소 클론 후
cd startup-apply/hwp_server
pip install -r requirements.txt
python main.py
```

서버가 실행 중이면 Claude Code가 자동으로 연결합니다.
서버 미실행 시에도 Markdown 초안은 생성됩니다.

---

## 관련 커맨드

- `/apply-write` — 사업계획서 작성
- `/apply-update` — 기존 사업계획서 재활용

## 관련 스킬

이 커맨드 실행 시 `hwp-format` 스킬이 자동 활성화됩니다.
