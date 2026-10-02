---
name: cnki-navigate-pages
description: Navigate CNKI search result pages (next/previous/specific page) or change sort order. Use when user wants to see more results or change sorting.
argument-hint: "[next|previous|page N|sort by date|citations|downloads]"
---

# cnki-翻页排序 —— 结果翻页与排序

- 去哪找：知网检索结果页（kns.cnki.net）
- 什么时候用：要浏览更多结果页，或按相关度/发表时间/被引/下载/综合重排结果
- 实测：迁移自 cookjohn/cnki-skills，未本机逐条复测
- 上游：https://github.com/cookjohn/cnki-skills

All operations use a single async `evaluate_script` — no snapshot or wait_for needed.

## 参数

`$ARGUMENTS` should be one of:
- `next` / `previous` / `page N` — pagination
- `sort by date` / `sort by citations` / `sort by downloads` / `sort by relevance` / `sort by comprehensive` — sorting

## 翻页（单次 evaluate_script）

Replace `ACTION_HERE` with `"next"`, `"previous"`, or `"page 3"`:

```javascript
async () => {
  const cap = document.querySelector('#tcaptcha_transform_dy');
  if (cap && cap.getBoundingClientRect().top >= 0) return { error: 'captcha' };

  const action = "ACTION_HERE";
  const pageLinks = document.querySelectorAll('.pages a');
  const prevMark = document.querySelector('.countPageMark')?.innerText;

  if (action === 'next') {
    const next = Array.from(pageLinks).find(a => a.innerText.trim() === '下一页');
    if (!next) return { error: 'no_next_page' };
    next.click();
  } else if (action === 'previous') {
    const prev = Array.from(pageLinks).find(a => a.innerText.trim() === '上一页');
    if (!prev) return { error: 'no_previous_page' };
    prev.click();
  } else {
    const num = action.replace(/\D/g, '');
    const target = Array.from(pageLinks).find(a => a.innerText.trim() === num);
    if (!target) return { error: 'page_not_found', available: Array.from(pageLinks).map(a => a.innerText.trim()) };
    target.click();
  }

  // Wait for page change
  await new Promise((r, j) => {
    let n = 0;
    const c = () => {
      const mark = document.querySelector('.countPageMark')?.innerText;
      if (mark && mark !== prevMark) r();
      else if (++n > 30) j('timeout');
      else setTimeout(c, 500);
    };
    setTimeout(c, 1000);
  });

  const cap2 = document.querySelector('#tcaptcha_transform_dy');
  if (cap2 && cap2.getBoundingClientRect().top >= 0) return { error: 'captcha' };

  return {
    action,
    total: document.querySelector('.pagerTitleCell')?.innerText?.match(/([\d,]+)/)?.[1] || '0',
    page: document.querySelector('.countPageMark')?.innerText || '?',
    url: location.href
  };
}
```

## 排序（单次 evaluate_script）

Replace `SORT_HERE` with `"relevance"`, `"date"`, `"citations"`, `"downloads"`, or `"comprehensive"`:

```javascript
async () => {
  const cap = document.querySelector('#tcaptcha_transform_dy');
  if (cap && cap.getBoundingClientRect().top >= 0) return { error: 'captcha' };

  const sortBy = "SORT_HERE";
  const idMap = {
    'relevance': 'FFD', 'date': 'PT',
    'citations': 'CF', 'downloads': 'DFR', 'comprehensive': 'ZH'
  };

  const liId = idMap[sortBy];
  if (!liId) return { error: 'invalid_sort', valid: Object.keys(idMap) };

  const li = document.querySelector('#orderList li#' + liId);
  if (!li) return { error: 'sort_option_not_found' };

  const prevMark = document.querySelector('.countPageMark')?.innerText;
  li.click();

  // Wait for results to refresh (page resets to 1)
  await new Promise((r, j) => {
    let n = 0;
    const c = () => {
      const mark = document.querySelector('.countPageMark')?.innerText;
      if (mark && mark !== prevMark) r();
      else if (++n > 30) j('timeout');
      else setTimeout(c, 500);
    };
    setTimeout(c, 1000);
  });

  return {
    sortBy,
    total: document.querySelector('.pagerTitleCell')?.innerText?.match(/([\d,]+)/)?.[1] || '0',
    page: document.querySelector('.countPageMark')?.innerText || '?',
    activeLi: document.querySelector('#orderList li.cur')?.innerText?.trim(),
    url: location.href
  };
}
```

## 输出

> Navigated to page {page}. Total {total} results.
> Results now sorted by {sortBy}.

## 工具调用：1 次（仅 evaluate_script）

## 已验证选择器

| Element | Selector | Notes |
|---------|----------|-------|
| Page links | `.pages a` | numbers + 上一页/下一页 |
| Current page | `.pages a.cur` | |
| Next page | text `下一页`, class `pagesnums` | |
| Page counter | `.countPageMark` | text "1/300" |
| Sort container | `#sortList` (`.order-group`) | |
| Sort options | `#orderList li` | click to sort |
| 相关度 | `li#FFD` | data-sort="FFD" |
| 发表时间 | `li#PT` | data-sort="PT" |
| 被引 | `li#CF` | data-sort="CF" |
| 下载 | `li#DFR` | data-sort="DFR" |
| 综合 | `li#ZH` | data-sort="ZH" |
| Active sort | `#orderList li.cur` | has class `cur` |

## 验证码识别

Check `#tcaptcha_transform_dy` element's `getBoundingClientRect().top >= 0`.
Only active when `top >= 0` (visible). Pre-loaded SDK sits at `top: -1000000px`.
