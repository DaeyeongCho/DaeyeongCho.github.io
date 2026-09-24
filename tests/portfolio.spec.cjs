const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('node:fs');

const pages = [
  ['home', '/'],
  ['rag', '/work/rag-microservices/'],
  ['deployment', '/work/microservice-deployment/'],
  ['cloud', '/work/multi-cloud/'],
  ['publications', '/publications/'],
  ['404', '/missing-page/']
];

for (const width of [360, 390, 768, 1440]) {
  for (const [name, url] of pages) {
    test(`${name}: ${width}px, content, overflow, resources and accessibility`, async ({ page }) => {
      await page.setViewportSize({ width, height: 1000 });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('requestfailed', request => errors.push(request.url()));
      page.on('console', msg => {
        if (msg.type() === 'error' && name !== '404') errors.push(msg.text());
      });
      const response = await page.goto(url);
      expect(response.status()).toBe(name === '404' ? 404 : 200);
      await expect(page.locator('h1')).toHaveCount(1);
      await expect(page.locator('h1')).toBeVisible();
      await expect(page.getByRole('navigation', { name: '주요 메뉴' })).toBeVisible();
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      // Lazy images load when their section enters the viewport.
      for (const image of await page.locator('img').all()) {
        await image.scrollIntoViewIfNeeded();
        await expect.poll(() => image.evaluate(el => el.complete && el.naturalWidth > 0)).toBe(true);
      }
      await page.evaluate(() => window.scrollTo(0, 0));
      // Verify actual computed styling, rather than accepting an unstyled document.
      expect(await page.locator('body').evaluate(el => getComputedStyle(el).backgroundColor)).toBe('rgb(252, 252, 250)');
      if (width === 390 || width === 1440) {
        const a11y = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
        expect(a11y.violations).toEqual([]);
        fs.mkdirSync('screenshots', { recursive: true });
        await page.screenshot({ path: `screenshots/${name}-${width}.png`, fullPage: true });
        if (name === 'home') await page.screenshot({ path: `screenshots/home-${width}-hero.png` });
      }
      expect(errors).toEqual([]);
    });
  }
}

test('navigation, direct paths, reload, fragments and keyboard focus', async ({ page, request }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: '본문으로 바로가기' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/#main$/);
  for (const id of ['work', 'stack', 'experience', 'research', 'contact']) {
    await page.locator(`nav.nav a[href="index.html#${id}"]`).click();
    await expect(page).toHaveURL(new RegExp(`#${id}$`));
    const y = await page.locator(`#${id}`).evaluate(el => el.getBoundingClientRect().top);
    const headerHeight = await page.locator('.site-header').evaluate(el => el.getBoundingClientRect().height);
    expect(y).toBeGreaterThanOrEqual(headerHeight - 2);
  }
  await page.goto('/');
  await page.getByRole('link', { name: '상세 사례 보기 →' }).first().click();
  await expect(page).toHaveURL(/\/work\/rag-microservices\/$/);
  await page.reload();
  await expect(page.getByRole('heading', { level: 1 })).toContainText('해소 방안');
  for (const [, path] of pages.filter(([name]) => name !== '404')) {
    await page.goto(path);
    const internal = await page.locator('a').evaluateAll(links => [...new Set(links.map(a => a.href).filter(h => h.startsWith(location.origin)))]);
    for (const href of internal) {
      const response = await request.get(href);
      expect(response.ok(), href).toBe(true);
      const fragment = new URL(href).hash.slice(1);
      if (fragment) expect(await response.text(), href).toContain(`id="${decodeURIComponent(fragment)}"`);
    }
  }
  const redirect = await request.get('/work/rag-microservices', { maxRedirects: 0 });
  expect(redirect.status()).toBe(301);
  await page.goto('/');
  expect(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');
});
