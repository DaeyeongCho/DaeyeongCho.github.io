#!/usr/bin/env python3
"""Generate the committed GitHub Pages HTML using Python's standard library."""
import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / 'content' / name).read_text(encoding='utf-8'))


P = read('profile.json')
W = read('work.json')
R = read('publications.json')
PAPERS = {p['id']: p for p in R['papers']}
e = escape


def link(url, label, cls='text-link'):
    return f'<a class="{cls}" href="{e(url, quote=True)}">{e(label)}</a>'


def authors(names):
    return ', '.join(f'<strong>{e(n)}</strong>' if n == P['name'] else e(n) for n in names)


def tags(items):
    return '<ul class="tags" aria-label="사용 기술">' + ''.join(f'<li>{e(t)}</li>' for t in items) + '</ul>'


def count_summary():
    journals = sum(p['type'] == 'journal' for p in R['papers'])
    conferences = sum(p['type'] == 'conference' for p in R['papers'])
    return f'학술 논문 {journals + conferences}편 · Journal {journals} · Conference {conferences} · 석사학위논문 1편'


def head(title, description, path, prefix, noindex=False):
    canonical = P['url'] + path
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description, quote=True)}">
  <meta name="author" content="Daeyeong Cho">
  <meta name="theme-color" content="#101e32">
  {'<meta name="robots" content="noindex">' if noindex else ''}
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{e(title, quote=True)}">
  <meta property="og:description" content="{e(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{P['url']}assets/avatar.png">
  <meta property="og:image:alt" content="조대영 GitHub 프로필 이미지">
  <meta name="twitter:card" content="summary">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}styles.css">
</head>'''


def header(prefix='', active=''):
    nav = [('work', 'Work'), ('stack', 'Expertise'), ('experience', 'Experience'), ('research', 'Research'), ('contact', 'Contact')]
    links = ''.join(f'<a href="{prefix}index.html#{key}" {"aria-current=\"page\"" if key == active else ""}>{label}</a>' for key, label in nav)
    return f'''<a class="skip-link" href="#main">본문으로 바로가기</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{prefix}index.html#top" aria-label="조대영 포트폴리오 홈"><span class="brand-mark" aria-hidden="true">DC<span>.</span></span><span class="brand-name">Daeyeong Cho</span></a>
    <nav class="nav" aria-label="주요 메뉴">{links}</nav>
  </div>
</header>'''


def footer(prefix=''):
    return f'''<footer class="footer"><div class="container footer-inner"><span>© 2026 Daeyeong Cho</span><span>Software · AI · Cloud</span>{link(prefix + 'index.html#top', '처음으로 ↑')}</div></footer>'''


def page(title, description, path, body, prefix='', active='', noindex=False):
    return head(title, description, path, prefix, noindex) + '\n<body id="top">\n' + header(prefix, active) + body + footer(prefix) + '\n</body>\n</html>\n'


def section_title(number, english, title, note=''):
    return f'<div class="section-heading"><div><p class="eyebrow"><span>{number}</span> / {english}</p><h2>{title}</h2></div>{f"<p class=\"section-note\">{note}</p>" if note else ""}</div>'


def paper_item(p, prefix='', compact=False):
    venue = p['venue']
    if p.get('volume'):
        venue += f", {p['volume']}({p['issue']})"
    venue += f", pp. {p['pages']}, {p['year']}."
    links = []
    if p.get('doi'):
        links.append(link('https://doi.org/' + p['doi'], 'DOI ↗'))
    if p.get('url'):
        links.append(link(p['url'], '논문 정보 ↗'))
    links.append(link(prefix + 'work/' + p['work'] + '/', '연구 배경 →'))
    award = f'<p class="award">{e(p["award"])} · 제1저자</p>' if p.get('award') else ''
    label = 'Journal' if p['type'] == 'journal' else 'Conference'
    doi_line = f'<p class="doi">DOI: {e(p["doi"])}</p>' if p.get('doi') and not compact else ''
    return f'''<article class="paper" id="{p['id']}"><p class="paper-type">{p['year']} / {label}</p><div><h3>{e(p['title'])}</h3><p class="authors">{authors(p['authors'])}</p><p class="citation">{e(venue)}</p>{doi_line}{award}<div class="resource-links">{' '.join(links)}</div></div></article>'''


def work_teaser(w):
    return f'''<article class="work-row">
  <div class="work-index"><span>{w['number']}</span><p>{e(w['category'])}</p></div>
  <div class="work-overview"><h3>{link('work/' + w['slug'] + '/', w['title'], 'work-title')}</h3><p>{e(w['summary'])}</p><p class="contribution"><span>담당</span> {e(w['contribution'])}</p>{tags(w['tech'][:5])}</div>
  <div class="work-aside"><span class="work-kind">Engineering &amp; Research</span>{link('work/' + w['slug'] + '/', '상세 사례 보기 →', 'button small')}</div>
</article>'''


def home():
    current = P['experience'][0]
    focus_links = ''.join(f'<a href="work/{w["slug"]}/"><span class="focus-number">{w["number"]}</span><span><strong>{e(w["short_title"])}</strong><small>{e(w["category"])}</small></span><span aria-hidden="true">↗</span></a>' for w in W)
    expertise = ''.join(f'<article class="expertise-item"><h3>{e(x["title"])}</h3><p>{e(x["description"])}</p><p class="tech-line">{e(x["tech"])}</p>{link("work/" + x["work"] + "/", "적용 사례 →")}</article>' for x in P['expertise'])
    jobs = ''.join(f'<article class="timeline-item"><p class="date">{e(x["period"])}</p><div><h3>{e(x["company"])}</h3><p class="role">{e(x["role"])}</p><p>{e(x["summary"])}</p><p class="muted">{e(x["detail"])}</p></div></article>' for x in P['experience'])
    education = ''.join(f'<article class="education-item"><p class="date">{e(x["period"])}</p><h3>{e(x["school"])}</h3><p>{e(x["degree"])}</p><p class="gpa">GPA {e(x["gpa"])}</p></article>' for x in P['education'])
    achievements = ''.join(f'<li><strong>{e(x["title"])}</strong><span>{e(x["detail"])}</span></li>' for x in P['achievements'])
    patent = R['patent']
    body = f'''<main id="main">
<section class="hero" aria-labelledby="hero-title"><div class="container hero-grid">
  <div class="hero-intro"><p class="eyebrow">SOFTWARE ENGINEER / 조대영</p><h1 id="hero-title">AI 응용 개발과<br>클라우드 인프라를<br><span>함께 다룹니다.</span></h1><p class="hero-copy">{e(P['intro'])}</p><div class="hero-actions">{link('#work', '대표 작업 살펴보기 ↓', 'button primary')}{link('mailto:' + P['email'], '연락하기 ↗', 'button ghost')}</div><p class="hero-background">M.S. in Computer Engineering · PNU SELab</p></div>
  <aside class="focus-panel" aria-label="현재 역할과 대표 작업"><div class="now"><span class="status-dot" aria-hidden="true"></span><span>NOW / SMARTBANK</span></div><h2>Python Developer</h2><p>AI Service &amp; Backend<br>Sep 2026 – Present</p><div class="focus-list">{focus_links}</div><div class="panel-bottom"><span>Cloud Native · Microservices</span><span>LLM/RAG · Multi-Cloud</span></div></aside>
</div></section>
<section id="work" class="section"><div class="container">{section_title('01', 'SELECTED WORK', '구현과 연구로 다룬 문제들', '문제의 맥락부터 담당 범위와 검증까지.')}<div class="work-list">{''.join(work_teaser(w) for w in W)}</div></div></section>
<section id="stack" class="section section-tinted"><div class="container">{section_title('02', 'EXPERTISE', '기술을 적용한 방식')}<div class="expertise-grid">{expertise}</div><p class="additional-tech"><strong>그 밖의 개발·인프라 경험</strong> {e(P['additional_tech'])}</p></div></section>
<section id="experience" class="section"><div class="container">{section_title('03', 'EXPERIENCE', '연구에서 실무 개발로')}<div class="timeline">{jobs}</div></div></section>
<section id="research" class="section section-tinted"><div class="container">{section_title('04', 'PUBLICATIONS & PATENT', '기술적 접근을 기록한 결과물')}<p class="research-count">{count_summary()}</p><div class="papers">{''.join(paper_item(p, compact=True) for p in R['papers'] if p.get('selected'))}</div>
<div class="patent-teaser"><div><p class="eyebrow">PATENT APPLICATION</p><h3>{e(patent['title'])}</h3><p>{e(patent['summary'])}</p></div>{link('publications/#patent', '특허 상세 →')}</div><div class="section-action">{link('publications/', '논문 전체 목록·학위논문·특허 보기 →', 'button')}</div></div></section>
<section id="about" class="section"><div class="container about-grid"><div><img class="avatar" src="assets/avatar.png" alt="조대영 GitHub 프로필 이미지" width="52" height="52" loading="lazy"><p class="eyebrow">05 / BACKGROUND</p><h2>소프트웨어공학을 바탕으로</h2><p class="about-copy">석사 과정에서 서비스의 구조와 동작을 분석하고, AI를 개발·운영 지원에 적용하는 방법을 연구했습니다. 명세와 운영 데이터를 해석하고, 이를 실제 도구로 구현하는 경험을 쌓았습니다.</p><ul class="achievement-list">{achievements}</ul></div><div id="education">{education}</div></div></section>
<section id="contact" class="contact-section"><div class="container contact-grid"><div><p class="eyebrow">CONTACT</p><h2>기술과 경험을<br>나눌 대화를 기다립니다.</h2><p>소프트웨어 개발, AI 응용, 클라우드 기술에 관한<br class="desktop-break"> 협업과 교류는 이메일로 연락해 주세요.</p></div><div class="contact-detail">{link('mailto:' + P['email'], P['email'] + ' ↗', 'email-link')}<div class="resource-links">{link(P['github'], 'GitHub ↗')}{link(P['orcid'], 'ORCID ↗')}</div><p>조대영 · Daeyeong Cho<br>Busan, South Korea</p></div></div></section>
</main>'''
    return page('조대영 | Software Engineer · AI & Cloud', P['intro'], '', body)


def diagram(d):
    if 'lanes' in d:
        lanes = ''.join('<li>' + ''.join(f'<span>{e(l[k])}</span>' + ('<b aria-hidden="true">→</b>' if k != 'output' else '') for k in ('input', 'knowledge', 'output')) + '</li>' for l in d['lanes'])
        inner = f'<ol class="diagram-lanes">{lanes}</ol>'
    else:
        inner = '<ol class="diagram-steps">' + ''.join(f'<li><span class="step-number">0{i+1}</span><strong>{e(s[0])}</strong><span>{e(s[1])}</span></li>' for i, s in enumerate(d['steps'])) + '</ol>'
    return f'<figure class="flow-diagram"><figcaption>{e(d["caption"])}</figcaption>{inner}<p class="diagram-note">연구·개발 접근을 요약한 개념도</p></figure>'


def work_page(w):
    prefix = '../../'
    projects = ''.join(f'<li><strong>{e(p["name"])}</strong><span>{e(p["organization"])} · {e(p["period"])}</span></li>' for p in w['projects'])
    implementation = ''.join(f'<article class="implementation-step"><span class="step-number">0{i+1}</span><div><h3>{e(x["title"])}</h3><p>{e(x["body"])}</p></div></article>' for i, x in enumerate(w['implementation']))
    resources = ''.join(f'<li>{link(x["url"], x["label"] + " ↗")}<span>{e(x["note"])}</span></li>' for x in w['resources'])
    resources += ''.join(f'<li>{link(prefix + "publications/#" + pid, PAPERS[pid]["title"])}<span>{PAPERS[pid]["year"]} · {"Journal" if PAPERS[pid]["type"] == "journal" else "Conference"} · {"제1저자" if PAPERS[pid]["authors"][0] == P["name"] else "공동저자"}</span></li>' for pid in w['publications'])
    if w.get('thesis'):
        resources += f'<li>{link(prefix + "publications/#thesis", R["thesis"]["title"])}<span>2026 · 석사학위논문</span></li>'
    if w.get('patent'):
        resources += f'<li>{link(prefix + "publications/#patent", "생성형 AI 학습 기반 약결합 지원 특허")}<span>공동 발명 · 특허 출원</span></li>'
    next_work = W[(W.index(w) + 1) % len(W)]
    body = f'''<main id="main">
<section class="case-hero"><div class="container"><a class="back-link" href="../../index.html#work">← Selected Work</a><p class="eyebrow">CASE {w['number']} / {e(w['category'])}</p><h1>{e(w['title'])}</h1><p class="case-summary">{e(w['summary'])}</p>{tags(w['tech'])}</div></section>
<div class="container case-layout"><aside class="case-meta" aria-label="참여 정보"><h2>Project context</h2><p class="meta-label">ROLE</p><p>{e(w['role'])}</p><p class="meta-label">PROJECT{'S' if len(w['projects']) > 1 else ''}</p><ul class="project-context">{projects}</ul><nav class="case-nav" aria-label="사례 목차"><a href="#context">배경</a><a href="#contribution">담당한 일</a><a href="#approach">기술적 접근</a><a href="#validation">검증과 범위</a><a href="#resources">Resources</a></nav></aside>
<div class="case-content"><section id="context"><p class="eyebrow">CONTEXT</p><h2>어떤 문제를 다뤘나요?</h2><p>{e(w['context'])}</p>{diagram(w['diagram'])}</section><section id="contribution"><p class="eyebrow">MY CONTRIBUTION</p><h2>직접 담당한 일</h2>{implementation}</section><section id="approach" class="decision"><p class="eyebrow">APPROACH</p><h2>{e(w['decision_title'])}</h2><p>{e(w['decision'])}</p></section><section id="validation"><p class="eyebrow">VALIDATION & SCOPE</p><h2>검증과 결과의 범위</h2><p>{e(w['verification'])}</p><p class="scope-note">{e(w['scope'])}</p></section><section id="resources"><p class="eyebrow">RESOURCES</p><h2>관련 결과물</h2><ul class="resource-list">{resources}</ul></section></div></div>
<div class="container next-work"><span>다음 사례</span>{link('../' + next_work['slug'] + '/', next_work['short_title'] + ' →')}</div>
</main>'''
    return page(w['short_title'] + ' | 조대영', w['summary'], 'work/' + w['slug'] + '/', body, prefix, 'work')


def publications_page():
    t = R['thesis']
    p = R['patent']
    groups = ''.join(f'<section id="{kind}"><h2>{label} <span class="count">{sum(p["type"] == kind for p in R["papers"])}</span></h2>{"".join(paper_item(p, "../") for p in R["papers"] if p["type"] == kind)}</section>' for kind, label in [('journal', 'Journal Papers'), ('conference', 'Conference Papers')])
    body = f'''<main id="main"><section class="page-hero"><div class="container"><a class="back-link" href="../index.html#research">← Research</a><p class="eyebrow">RESEARCH OUTPUT</p><h1>Publications &amp; Patent</h1><p>{count_summary()}</p><nav class="subnav" aria-label="연구 결과 탐색"><a href="#journal">Journal</a><a href="#conference">Conference</a><a href="#thesis">Thesis</a><a href="#patent">Patent</a></nav></div></section><div class="container publication-content">{groups}
<section id="thesis"><h2>Master’s Thesis</h2><article class="thesis-entry"><p class="paper-type">{t['year']} / M.S.</p><h3>{e(t['title'])}</h3><p><strong>{e(t['author'])}</strong> · {e(t['institution'])} · {e(t['degree'])}</p>{link('../work/rag-microservices/', '연구 배경과 구현 보기 →')}</article></section>
<section id="patent"><p class="eyebrow">PATENT APPLICATION · 1건</p><h2>{e(p['title'])}</h2><p class="patent-description">{e(p['summary'])}</p><dl class="patent-data"><div><dt>상태</dt><dd>{e(p['status'])}</dd></div><div><dt>발명자</dt><dd>{authors(p['inventors'])}</dd></div><div><dt>출원인</dt><dd>{e(p['assignee'])}</dd></div><div><dt>출원번호 / 출원일</dt><dd>{p['application']} / {p['filed']}</dd></div><div><dt>우선권 기초출원</dt><dd>{p['priority_application']} / {p['priority_date']}</dd></div><div><dt>공개번호 / 공개일</dt><dd>{p['publication']} / {p['published']}</dd></div></dl><div class="resource-links">{link(p['url'], '공개문헌 KR20260065458A ↗')}{link('../work/microservice-deployment/', '관련 연구 보기 →')}</div></section>
</div></main>'''
    return page('Publications & Patent | 조대영', '마이크로서비스·LLM/RAG 관련 학술 논문, 석사학위논문 및 특허 출원.', 'publications/', body, '../', 'research')


def outputs():
    result = {'index.html': home(), 'publications/index.html': publications_page()}
    for w in W:
        result['work/' + w['slug'] + '/index.html'] = work_page(w)
    body = '<main id="main" class="not-found container"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>페이지를 찾을 수 없습니다.</h1><p>주소가 바뀌었거나 존재하지 않는 페이지입니다.</p><a class="button primary" href="/">포트폴리오 홈으로 →</a></main>'
    result['404.html'] = page('페이지를 찾을 수 없습니다 | 조대영', '조대영 포트폴리오 홈으로 이동하세요.', '404.html', body, '/', noindex=True)
    paths = ['', 'publications/'] + ['work/' + w['slug'] + '/' for w in W]
    result['sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{P["url"]}{p}</loc></url>\n' for p in paths) + '</urlset>\n'
    result['robots.txt'] = f'User-agent: *\nAllow: /\nDisallow: /docs/\nDisallow: /scripts/\nDisallow: /content/\nSitemap: {P["url"]}sitemap.xml\n'
    return {name: "\n".join(line.rstrip() for line in value.splitlines()) + "\n" for name, value in result.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if committed HTML is out of date.')
    args = parser.parse_args()
    stale = []
    generated = outputs()
    for name, content in generated.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    if stale:
        raise SystemExit('Generated files out of date: ' + ', '.join(stale))
    print(f'{"Checked" if args.check else "Built"} {len(generated)} static files.')


if __name__ == '__main__':
    main()
