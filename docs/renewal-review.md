# 포트폴리오 개편 검토 기록

작성일: 2026-09-24. 검토 브랜치: `feat/portfolio-renewal-20260924`.

## 기준과 기존 사이트

- 웹사이트 기본 브랜치: `main`
- 시작 커밋: `a7466d310bec904fadfce91539493753f6df29b0`
- 시작 tree: `a448f9e8d9980e4c3f05f6eff9a0916d8b2c0627`
- 실제 저장소에는 `index.html`, `styles.css` 두 파일만 있었습니다. AGENTS.md, 프레임워크, 의존성·잠금 파일, 자산 디렉터리, 테스트, 별도 workflow는 없었습니다.
- HTML과 CSS 전체를 읽고 운영 사이트의 데스크톱 화면·DOM·링크·이미지 로딩을 확인했습니다.
- 배포 이력: GitHub가 생성한 `dynamic/pages/pages-build-deployment`, `main`, 위 시작 커밋, 성공(실행 35969519927). 최근 두 Pages 실행 모두 `main`이었습니다. Pages 설정 API 자체는 도구 범위 제한/인증 없는 404로 읽지 못했으므로, 설정 화면을 직접 확인했다고 주장하지 않습니다.
- 현재 프로필 README(main)의 파일 SHA `f5e5e467762bc42219db99648ab18bb88ecaa883`과 이전 Work에서 저장한 최종 초안, 이후 대화의 수정을 대조했습니다. 프로필 README 저장소는 수정하지 않았습니다.

### 진단

유지할 자산은 네이비 색상, DC 표식, 한국어 본문, GitHub 프로필 이미지, 경력·학력의 사실, 연락·ORCID·실험 자료 링크입니다.

기존 화면은 About·Tech Stack·경력·연구 주제에서 같은 설명을 반복했습니다. 대표 작업의 담당 범위와 설계 판단, 논문·특허 제목과 원출처로 연결되는 경로가 부족했습니다. 연구 숫자만으로 학술 논문과 학위논문의 구분을 알기 어려웠고, SmartBank 경력이 없으며 Contact는 구직 중 문구였습니다. CSS는 980px 이하에서 메뉴를 숨겼고 대체 메뉴가 없었습니다. 명시적인 skip link, focus-visible, reduced-motion, canonical, 404도 없었습니다.

## 세 매체의 역할

다음은 자료를 바탕으로 이번 작업에 적용한 설계 판단이며, 모든 포트폴리오에 적용되는 고정 규칙은 아닙니다.

| 매체 | 방문자가 얻을 것 | 이번 사이트와의 관계 |
| --- | --- | --- |
| GitHub 프로필 README | 개발자 정체성, 핵심 경험, 저장소·외부 자료의 빠른 안내 | 요약은 일치하되 같은 섹션을 그대로 복제하지 않음 |
| 이력서 | 경력 기간·역할·성과·학력의 빠른 비교 | 기간과 역할을 간결한 경력 목록에 유지 |
| 개인 웹사이트 | 관심 있는 경험의 배경·기여·접근·검증·근거를 선택해 탐색 | 대표 작업 요약 → 상세 사례 → 논문·특허·코드로 연결 |

## 조사 원칙과 출처

2026-09-24에 검색·확인했습니다. 오래된 지침도 현재 유효한 원칙에 한해 적용했으며 ‘2026년의 새 규칙’으로 소개하지 않습니다.

| 자료 | 성격 | 이번 구현에 적용 |
| --- | --- | --- |
| [Arc: Software Engineer Portfolio](https://arc.dev/talent-blog/software-engineer-portfolio/) | 개발자 채용 플랫폼에 실린 작성자의 커리어 조언 | 기술·비기술 방문자를 함께 고려. 사용 기술뿐 아니라 기여와 접근 이유 설명. 퍼센트 숙련도 제외 |
| [NN/g: Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/) | UX 전문가의 설계 원칙 | 메인 요약과 상세 사례를 분리하여 원하는 깊이로 탐색 |
| [W3C/WAI: Designing for Web Accessibility](https://www.w3.org/WAI/tips/designing/) | 공식 접근성 안내 | 명확한 메뉴·대비·포커스·제목 계층·본문 바로가기 |
| [W3C: Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | WCAG 2.2 이해 문서 | 탐색 링크·버튼의 충분한 터치 영역과 간격 |
| [web.dev: Learn Responsive Design](https://web.dev/learn/design) | Google의 웹 구현 교육 자료 | 고정 화면 폭 대신 유동 레이아웃, 읽기와 줄바꿈을 기준으로 분기 |
| [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) | 웹 플랫폼 문서 | 동작 감소 설정에서는 부드러운 스크롤 해제 |
| [GitHub Pages 게시 소스](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) | 공식 배포 문서 | 루트 정적 파일과 게시 소스 보존. 검증 workflow에 배포 단계를 두지 않음 |
| [Playwright CI](https://playwright.dev/docs/ci-intro), [접근성 검사](https://playwright.dev/docs/accessibility-testing) | 테스트 도구의 공식 문서 | CI에서 반응형 브라우저 검사·axe·스크린샷 아티팩트 |

### 실제 포트폴리오 3가지

아래는 각 사이트의 실제 콘텐츠와 탐색 구조를 보고 내린 관찰입니다. 문구·레이아웃·코드를 복제하지 않았습니다. 사례 사이트의 모바일 사용성은 실측하지 않았습니다.

| 사례 | 대상과 첫 화면 | 상세 정보와 개인 기여 | 적용 / 적용하지 않은 점 |
| --- | --- | --- | --- |
| [Brittany Chiang](https://brittanychiang.com/) | 프런트엔드 채용·협업. 역할과 접근성 중심 정체성 | 경력별 역할 설명과 사용 기술, 프로젝트 링크 | 설명 근처에 기술·근거 배치. 경력 분량과 시각 스타일은 복제하지 않음 |
| [Chip Huyen](https://huyenchip.com/) | AI 시스템 실무자·기술 독자. AI를 실제 환경에 적용하는 활동 소개 | 실무 경험에서 공개 도구·교육·책으로 연결 | 실무와 연구 배경의 연결. 출판·강의가 중심인 구조는 그대로 적용하지 않음 |
| [Yevgeniy Brikman](https://www.ybrikman.com/) | 클라우드·DevOps 실무자·협업 대상 | 현재 역할을 먼저 설명하고 work·책·발표로 상세 분리 | 현재 역할과 결과물의 탐색 경로 구분. 자료가 없는 블로그·발표 메뉴는 추가하지 않음 |

## 설계와 구현

- **메인 + 상세 4개**: 홈페이지, 사례 3개, 논문·특허 전체 목록. 이력서 사실은 메인에, 기술적 설명은 상세에 배치했습니다. 불필요한 검색·필터·빈 블로그는 없습니다.
- **대표 작업 3개 / 실제 과제 3개**: 앞의 두 기술 주제는 동일 NRF 과제임을 명시했습니다. 멀티 클라우드 페이지에서는 서로 다른 ETRI 과제 2개의 기간과 범위를 구분했습니다.
- **실제 작업에서 나온 설명**: 오류 내용과 해소 방안의 분리 저장, BCE 유형 식별, 메타데이터 스키마·요구사항 구조화 등 확인된 접근을 설명합니다. 서비스 배포 성과, 자동 복구, 성능 수치는 창작하지 않았습니다.
- **디자인**: 기존 네이비를 hero·contact에 유지하고, 밝은 본문·선형 구분·숫자 인덱스로 읽기 흐름을 만듭니다. 첫 화면의 작업 인덱스는 실제 상세 링크입니다. 배지 벽, 거대 통계, 자동 재생, 스크롤 효과는 없습니다.
- **개념도**: 제공된 연구 흐름을 HTML/CSS로 표현했습니다. 회사 내부 아키텍처나 서비스 구현 화면인 것처럼 표시하지 않습니다.
- **유지보수**: 프레임워크를 도입하지 않았습니다. Python 표준 라이브러리 생성기와 JSON 데이터만 추가해 중복 서지정보를 줄였습니다. Node 의존성은 CI 테스트용입니다.
- **기존 URL**: 기존 메인 앵커 7개를 유지합니다. 상세는 실제 디렉터리/index.html이며 SPA 라우팅에 의존하지 않습니다.
- **메타데이터**: 실제 주소의 canonical·OG, 존재하는 avatar 이미지, favicon·sitemap·robots·404. 가짜 이력서 다운로드나 문의 폼은 없습니다.

## 사실과 원출처 대조

| 항목 | 확인·반영 내용 | 출처 |
| --- | --- | --- |
| SmartBank | Python Developer, Sep 2026 – Present. 도면관리 플랫폼 참여 영역과 Python·LLM/RAG 개발 방향만 표시 | 사용자 명시 요청·현재 프로필. [회사 홈페이지](https://smartbank.ne.kr/)는 LLM·RAG 사업 방향만 확인; 개인 수행 실적의 근거로 사용하지 않음 |
| 신규 Journal | 정수민, 조대영, 박준석, 염근혁. 22(4), 22–35, 2026. DOI 10.23019/kingpc.22.4.202608.002 | [KCI 상세](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART003377738), [권호 목록](https://www.kci.go.kr/kciportal/landing/journalArticleList.kci?sere_id=SER000010579&vol_isse_id=VOL000200028) |
| 2025 Journal 2편 | 저자 순서·권호·페이지·DOI 대조 | [BCE 논문 KCI](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART003171258), [학습 기반 관리 KCI](https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART003262747) |
| Conference 4편 | ACK 2025, KCC 2025, ACK 2024, KCC 2024. Journal 및 학위논문과 분리 | [ACK 2025](https://kiss.kstudy.com/Detail/Ar?key=4209918), [KCC 2025](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12318188), [ACK 2024 프로그램](https://www.manuscriptlink.com/society/kips/conference/ack2024/programBook), [KCC 2024](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11861829) |
| 석사학위논문 | 2026, RAG를 적용한 컨테이너 기반 마이크로서비스의 오류 식별 방법 | 사용자 제공 학위논문. 인쇄 p.23–25의 지식 베이스·운영 정보 입력 확인 |
| 특허 | 공개 명칭, 발명자, 출원인, 2025 출원번호, 2024 우선권 기초출원, 2026 공개번호를 구분 | [공개문헌 KR20260065458A](https://patents.google.com/patent/KR20260065458A/ko) 및 [동일 문헌 영문 페이지](https://patents.google.com/patent/KR20260065458A/en) |
| ETRI 원장상 | ACK 2024 수상 논문 제1저자 | [부산대학교 SELab 공지](https://se.pusan.ac.kr/bbs/se_ce/5554/1699927/artclView.do?layout=unknown), 학회 프로그램 |
| 연구·과제 기간·학력·GPA·저작권 5건 | 제공된 경력기술서, 학위논문, 현재 프로필 대조 | 사용자 제공 기록. 원문 이력서·비공개 자료를 저장소에 업로드하지 않음 |
| 오류 실험 자료 | 제품 서비스 코드로 소개하지 않고 실험 자료로 연결 | [MSAError](https://github.com/DaeyeongCho/MSAError) 실제 README |
| 공개 기여 | Postgres 접근 오류의 재현 절차와 해결 과정을 작성한 이슈 | [Cloud-Barista #2249](https://github.com/cloud-barista/cb-tumblebug/issues/2249), 작성자 DaeyeongCho 확인 |

### 표현 보정과 확인 범위

- 현재 GitHub 프로필에 남아 있는 ‘오류 식별의 YAML 분석’ 표현은 복사하지 않았습니다. 오류 연구의 입력은 kubectl 출력·이벤트·로그와 Jaeger 흐름으로, YAML 명세 분석은 배치·약결합 연구로 구분했습니다.
- ‘처리’는 실제 논문 제목에서 유지하며, 구현 설명은 ‘오류 식별·해소 방안 생성’으로 씁니다.
- 신규 저널은 공동저자입니다. 관련 연구 페이지와 저자 목록에서 제1저자 논문과 구분했습니다.
- 학술 논문 7 = Journal 3 + Conference 4. 석사학위논문 1편은 별도 필드입니다.
- 특허는 공개문헌의 정확한 제목을 기본으로 사용합니다. 2024-10-29는 우선권 기초출원, 2025-01-10은 이 공개문헌의 출원일입니다. 출원 실적은 1건으로 표시합니다. Google Patents는 공보를 제공하는 2차 서비스이며, KIPRIS에서 최신 등록원부를 직접 조회하지 못했습니다. 따라서 ‘등록 특허’나 법적 유효성에 관한 주장은 하지 않습니다.
- Azure는 메타데이터 과제의 경험에 한정하고, AI 가속기 제공 현황은 AWS·Google Cloud 중심으로 설명합니다.
- 학회 원문 PDF의 403 경험을 고려해 주 링크는 논문 정보 페이지로 제공합니다. 원문 무료 열람·다운로드 가능 여부는 보장하지 않습니다.
- 비공개 코드가 필요한 사례에는 가짜 GitHub·데모 버튼을 만들지 않았습니다. 공개 실험·논문·특허·이슈만 연결합니다.

## 검증 기록

이 문서는 공개 포트폴리오 탐색 메뉴에 노출하지 않습니다.

### 실제 실행 결과

- 검증한 구현 커밋: `ee013a1fc9539f5cabee27f4bf24f9c9b1acc608`
- [GitHub Actions 실행 35980048421](https://github.com/DaeyeongCho/DaeyeongCho.github.io/actions/runs/35980048421): **성공, Playwright 25/25 통과**. 후속 문서·캡처 커밋은 사이트 코드·콘텐츠·테스트를 변경하지 않습니다.
- 로컬 의존성 설치 `npm ci --ignore-scripts`, CI의 `npm ci` 모두 성공했습니다.
- `python3 scripts/build.py`: 8개 정적 파일 생성. `npm run check`에서 생성 결과 일치 및 HTML 6개의 링크·앵커·제목 계층·메타데이터·서지정보 검사 통과.
- `node --check`로 테스트·설정 파일의 JavaScript 문법을 확인했습니다. 별도 ESLint 및 TypeScript 프로젝트는 아니므로 해당 린트·타입 검사를 실행했다고 표기하지 않습니다. `git diff --check`도 통과했습니다.
- Chromium에서 6개 경로를 각각 360·390·768·1440px로 렌더링해 가로 넘침, 제목, 메뉴, 실제 CSS 적용, 이미지 로딩, 예상하지 않은 콘솔·리소스 오류를 검사했습니다.
- 390·1440px의 6개 페이지에서 axe의 WCAG 2 A/AA·2.1 AA·2.2 AA 자동 검사 위반 0건입니다. 자동 검사로 접근성 전체를 보장하지는 않습니다.
- 키보드 본문 바로가기, 모바일 메뉴의 앵커 도착 위치, 모든 내부 링크와 fragment, 상세 페이지 직접 접근·새로고침, trailing slash 리다이렉트, reduced motion, 커스텀 404와 HTTP 404를 확인했습니다.
- 최초 실행은 21/25 통과했습니다. 홈 하단의 `loading="lazy"` 이미지를 스크롤 전에 검사한 테스트 4건이 실패했습니다. 이미지를 화면에 진입시킨 뒤 로딩을 기다리도록 테스트를 수정했고, 재실행에서 25건 모두 통과했습니다. 지연 로딩 자체는 유지했습니다.
- 구현 환경의 미리보기 서버는 실행했으나 연결된 대화형 브라우저가 localhost 접근을 차단했습니다. 따라서 새 사이트의 렌더링·탐색 검증은 저장소 CI의 Chromium으로 수행하고, 생성된 실제 화면 캡처를 열어 시각적으로 확인했습니다.

### 화면 검토

첫 화면의 정체성·SmartBank 역할·대표 작업 접근 경로, 홈 전체의 정보 순서, 상세 사례의 도식·담당 범위, 논문과 특허의 긴 제목 및 서지정보를 데스크톱·모바일 캡처에서 확인했습니다. 이미지와 텍스트의 겹침, 가로 잘림, 빈 섹션은 관찰되지 않았습니다. 태블릿 768px는 자동 렌더링·넘침 검사를 했으며 별도 수동 화면 검토는 하지 않았습니다.

| 화면 | 데스크톱 | 모바일 |
| --- | --- | --- |
| 홈 첫 화면 | [1440px](review/home-desktop-hero.png) | [390px](review/home-mobile-hero.png) |
| 홈 전체 | [1440px](review/home-desktop.png) | [390px](review/home-mobile.png) |
| 상세 사례 / 논문·특허 | [RAG 사례](review/case-rag-desktop.png) | [논문·특허](review/publications-mobile.png) |

캡처는 위 통과한 실행의 원본 PNG입니다. 전체 테스트 보고서와 다른 페이지 캡처는 해당 실행의 `portfolio-review` 아티팩트에 있으며 보관 기간은 14일입니다. 이 표의 주요 캡처는 저장소에 함께 보관합니다.

### 외부 링크와 확인 한계

- [외부 링크 GET 검사 기록](review/link-check.json): 중복을 제외한 HTTPS 링크 15개 중 12개가 HTTP 200으로 응답했습니다. GitHub, 실험 저장소, 공개 이슈, ORCID, KISS 2건, 특허 공개문헌 및 DOI 3건이 포함됩니다.
- DBpia 2건은 자동 접속에서 HTTP 502였습니다. 검색으로 해당 논문 정보가 존재하는 것을 확인했지만, 안정적인 직접 접근은 검증하지 못했습니다.
- 신규 논문의 KCI 직접 URL은 이 검사에서 시간 초과였으나 DOI를 통한 동일 KCI 페이지 접근은 HTTP 200이었습니다. 서지정보는 앞선 KCI 웹 조회로 별도 확인했습니다.
- HTTP 200은 원문 PDF 무료 열람이나 로그인 없는 다운로드를 의미하지 않습니다. 이메일은 실제 주소의 `mailto:` 링크를 확인했으며 메일을 발송하지 않았습니다.
- Chromium 이외의 Safari·Firefox, 실제 휴대폰, 스크린리더, Lighthouse는 실행하지 않았습니다. 성능 점수를 기재하지 않습니다. 홈 HTML·CSS·avatar 합계는 약 37.5KB이며 외부 런타임 폰트·스크립트는 없습니다.
- 새 상세 경로의 운영 GitHub Pages 응답은 아직 확인하지 않았습니다. 실제 디렉터리/index.html 구조와 로컬 HTTP 동작을 검증했으며 운영 배포는 수행하지 않았습니다.

### 변경 범위

별도 검토 브랜치만 업데이트했습니다. `main`, GitHub 프로필 README, Pages 설정은 변경하지 않았습니다. PR 생성·병합·운영 배포는 수행하지 않았습니다. 검증 workflow에는 배포 작업과 Pages 쓰기 권한이 없습니다.
