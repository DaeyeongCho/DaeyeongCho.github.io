# Daeyeong Cho · Portfolio

조대영의 소프트웨어·AI 응용·클라우드 엔지니어링 포트폴리오입니다.

사이트: https://daeyeongcho.github.io/

## 구조

기존 정적 HTML·CSS 구조를 유지합니다. 브라우저에서 실행하는 JavaScript와 운영 의존성은 없습니다. Python 표준 라이브러리로 콘텐츠 데이터를 HTML로 생성하며, 생성된 HTML을 저장소에 함께 커밋합니다. GitHub Pages는 루트 파일을 그대로 제공할 수 있습니다.

| 경로 | 역할 |
| --- | --- |
| `index.html` | 소개, 대표 작업 요약, 기술 적용 경험, 경력, 연구 결과 요약, 학력, 연락처 |
| `work/rag-microservices/` | RAG 기반 마이크로서비스 오류 식별·해소 방안 생성 |
| `work/microservice-deployment/` | LLM 기반 마이크로서비스 배치·약결합 |
| `work/multi-cloud/` | 멀티 클라우드 메타데이터 및 AI 가속기 과제 |
| `publications/` | 학술 논문 전체, 석사학위논문, 특허 상세 |
| `content/profile.json` | 소개, 경력, 학력, 기술, 수상·저작권 |
| `content/work.json` | 대표 작업의 요약·상세·과제·기간·자료 링크 |
| `content/publications.json` | 논문·저자·서지정보·특허의 단일 원본 |
| `scripts/build.py` | 공통 HTML 템플릿 및 정적 페이지 생성 |
| `styles.css` | 모든 페이지의 공통 디자인과 반응형 규칙 |
| `docs/renewal-review.md` | 조사 출처, 설계 판단, 사실 확인, 검증 기록 |

## 콘텐츠 수정

1. 해당 `content/*.json`을 수정합니다. 논문 ID와 작업 slug는 기존 링크 보존을 위해 가급적 유지합니다.
2. `python3 scripts/build.py`로 HTML과 sitemap을 갱신합니다.
3. `python3 scripts/build.py --check`와 `python3 scripts/check.py`로 생성 결과를 확인합니다.
4. 데이터와 생성 결과를 함께 커밋합니다.

논문 수는 `papers` 목록의 `type`으로 계산합니다. 석사학위논문은 별도 필드이며 이 집계에 포함하지 않습니다. 출원일과 우선권 기초출원일도 별도 필드로 관리합니다.

현재 실적을 보호하는 `scripts/check.py`의 집계·날짜 단언도 함께 확인하세요. 새 논문이나 특허 상태를 실제로 갱신할 때는 해당 기대값을 검증된 정보에 맞게 수정합니다.

## 로컬 실행

Python 3.12 이상만 있으면 빌드와 미리보기가 가능합니다.

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/serve.py
```

http://127.0.0.1:8000/ 을 엽니다. 미리보기 서버는 공개 페이지 경로만 제공하며, 미존재 경로에는 404 상태와 커스텀 404 화면을 반환합니다.

## 브라우저 검증

Node.js 22 이상은 테스트에만 사용합니다. 운영 사이트에는 npm 패키지가 전송되지 않습니다.

```bash
npm ci
npx playwright install --with-deps chromium
npm run check
npm test
```

Playwright는 360·390·768·1440px에서 문서, 가로 넘침, 리소스 로딩을 검사합니다. 390·1440px에서는 axe 접근성 검사와 화면 캡처를 추가합니다. 키보드 skip link, 고정 헤더와 앵커, 내부 경로, 상세 페이지 새로고침, 404, reduced motion도 검사합니다. 자동화 검사만으로 모든 접근성 요구사항을 보장하지 않으므로 캡처와 수동 탐색을 함께 확인하세요.

결과: `screenshots/`, `playwright-report/`, `test-results/` (git 제외). GitHub Actions의 `portfolio-review` 아티팩트에서도 확인할 수 있습니다.

## GitHub Pages

- 루트 정적 파일 구조와 기존 `#top`, `#about`, `#stack`, `#experience`, `#research`, `#education`, `#contact` 링크를 보존했습니다.
- `.nojekyll`로 정적 파일임을 명시합니다. 서버 라우팅과 SPA fallback은 필요하지 않습니다.
- 각 상세 URL은 디렉터리의 `index.html`에 대응하며 직접 접근·새로고침을 지원합니다.
- `404.html`, `sitemap.xml`, `robots.txt`, canonical·Open Graph 정보를 포함합니다.
- `.github/workflows/verify.yml`은 검증 및 아티팩트 업로드만 수행합니다. Pages 배포 권한, 배포 작업, 설정 변경은 포함하지 않습니다.
- 검토 브랜치를 운영 게시 소스에 병합하기 전에는 운영 사이트에 반영되지 않습니다.

## 콘텐츠 범위

연구 프로토타입과 회사의 현재 참여 영역을 구분합니다. 공개되지 않은 회사 구현·고객 정보나 비공개 코드, 이력서 원본은 포함하지 않습니다. 논문 원문은 재배포하지 않고 서지정보와 출처 링크로 연결합니다.
