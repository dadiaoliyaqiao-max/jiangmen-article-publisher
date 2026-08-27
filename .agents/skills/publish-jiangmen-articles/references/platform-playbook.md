# Platform playbook

## Shared preflight

Create a matrix with one row per article and columns for title, target date, body image count, cover, Toutiao, WeChat, Baijiahao, Zhihu, and Sohu. Use it as the only progress tracker.

The canonical body must already contain text, inline images, and visible captions in final order. Keep the title and cover outside the body.

Before opening platform editors:

- Run the manifest validator when a `publish-manifest.json` is available.
- Inspect every platform management page for the exact title and current state.
- Freeze the title/date/platform mapping for the run.
- Use the dedicated Chrome controller for logged-in Chrome sessions and keep one clean management tab plus one current editor tab.

## Toutiao

- Paste the complete rich-text body into the article editor once.
- Set the title separately and upload/select the cover separately.
- Use the native scheduled-publish control.
- Verify the content-management row says `定时发布中` and shows the requested date/time.

## WeChat Official Accounts

- Paste the complete rich-text body once; set title and cover separately.
- If the user chooses self-publication, save the complete article as a draft and do not enter the final scan/confirmation flow.
- A QR-code confirmation is not a reason to rebuild the article.
- Prefer rich clipboard paste over automated Word import when local file selection is denied or unstable.
- Wait for image processing and autosave before inspecting the draft list.
- Verify visible `figure` elements containing images; do not use the editor's raw internal `img` count.
- Choose the approved first正文图片 with `从正文选择`, save explicitly, then verify the draft card has a cover and no `内容不完整` warning.
- Record the WeChat `appmsgid` in tracker notes when visible.

## Baijiahao

- Paste the complete rich-text body into the editor iframe once.
- Choose a cover from正文图片 when the approved first image is suitable; otherwise upload the dedicated cover.
- Use the native `定时发布` dialog and set date, hour `20`, minute `0`.
- Treat `提交成功，正在审核中` as the authoritative submission result after the time was set.

## Sohu

- Paste the complete rich-text body into `.ql-editor` once.
- Fill an accurate summary separately.
- Prefer the first正文图片 as the cover to avoid a second upload.
- Use the native `定时发布` dialog and verify the content-management row shows `定时发布` with the exact date/time.
- Inspect the scheduler's current horizon before choosing a date. If the requested time is unavailable, keep the complete draft and schedule a follow-up when the exact requested time becomes selectable; never substitute the nearest available time.
- Do not overwrite the user's unrelated historical draft.

## Zhihu

- Paste the complete rich-text body once and upload the cover separately.
- Verify body figure/image count before leaving the editor.
- The current article editor may publish immediately when `发布` is clicked and may not expose a native scheduler. Inspect visible controls first.
- When no scheduler exists, save the finished article as a draft and create a one-time Codex continuation for the requested time. Do not click `发布` as a test.
- Use an explicit date-to-draft mapping in the continuation and publish exactly one mapped article per run.
- After publication, verify the public URL and expected figure count before updating the tracker.

## Minimal verification

For each pasted body, verify:

1. Exact title.
2. Expected image count.
3. Every image is followed by its `▲` caption.
4. First and last paragraphs match the canonical稿.
5. Cover is present.
6. Final status and time match the matrix.

Only run a full preview when one of these checks fails.

## Seven-article batch order

1. Finish and approve all seven canonical稿件.
2. Prepare seven cover paths and target dates.
3. For article 1, paste the same body into every target platform, then set each title and cover.
4. Schedule native platforms and save non-native platforms as complete drafts.
5. Repeat for articles 2-7.
6. Verify the matrix once at the end; do not repeatedly reopen already confirmed entries.

For a platform with a fragile long-form editor, it is acceptable to finish the full platform batch before moving to the next platform when that reduces tab churn and preserves a stable signed-in session. Keep the same article mapping and verification rules.
