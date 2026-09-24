const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 45000,
  fullyParallel: true,
  workers: process.env.CI ? 2 : undefined,
  retries: 0,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: 'http://127.0.0.1:8000',
    browserName: 'chromium',
    locale: 'ko-KR',
    reducedMotion: 'reduce',
    trace: 'retain-on-failure'
  },
  webServer: {
    command: 'python3 scripts/serve.py',
    url: 'http://127.0.0.1:8000',
    reuseExistingServer: !process.env.CI
  }
});
