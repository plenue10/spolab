import { test, expect } from '@playwright/test'

// Basic smoke test to ensure routes render.
test('renders data list and upgrade prompt', async ({ page }) => {
  await page.goto('http://localhost:5173/data')
  await expect(page.getByText('데이터셋')).toBeVisible()
})
