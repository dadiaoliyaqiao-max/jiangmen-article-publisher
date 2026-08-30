# Browser execution and recovery runbook

Read this reference for multi-platform browser publishing, interrupted runs, slow editors, or multi-day continuations.

## Stable browser topology

Use the dedicated Chrome browser controller when publishing depends on the user's signed-in Chrome session.

Keep only:

1. One clean management or draft-list tab for authoritative checks.
2. One current editor tab for the article being changed.

Do not mix Chrome control with Windows-level computer control in the same publishing run. A Windows controller may stop when it cannot prove the active browser URL, even though the Chrome tab itself is usable.

Heavy editors can remain open if closing them may discard unsaved work, but stop interacting with them. Open a fresh management tab and resume from the platform record instead.

## Checkpoint model

Treat every article-platform pair as a state machine:

`未创建 → 正文已填 → 封面已设 → 已保存草稿 → 已定时/已发布 → 已核验`

Advance the tracker only after an authoritative platform signal:

- Draft card with the exact title, non-empty cover, and no incomplete warning.
- Management row with the exact scheduled date and time.
- Published row or public URL for an immediate publication.

Record the platform record ID in the tracker notes when visible. It makes recovery faster and prevents same-title duplicates.

## Timeout rule

A browser timeout is an unknown outcome, not proof of failure.

After a timeout:

1. Do not repeat the mutation.
2. Open a fresh management tab.
3. Search the exact title and expected record ID.
4. Compare title, first paragraph, last paragraph, image/figure count, cover, status, and scheduled time.
5. Resume only from the first missing checkpoint.

This rule applies to paste, save, schedule, and publish actions.

## Rich-text fast path

Prepare compact canonical HTML before opening platforms. Keep the title outside the body and include each inline image and visible `▲` caption in final order.

Use one rich clipboard payload per article:

1. Fill the title separately.
2. Focus the actual body editor.
3. Select the existing body once.
4. Paste the complete rich-text body once.
5. Wait for platform-side image processing and autosave before verification.

Prefer this path over Word import when automated local-file selection is unavailable or unreliable. Never rebuild a long article paragraph by paragraph.

## WeChat Official Accounts

- Create or resume exactly one draft per title.
- After the full-body paste, wait for autosave and verify from a fresh draft-list tab.
- In the editor, verify the number of `figure` elements that each contain an image. Do not rely on raw internal `img` count because WeChat may maintain duplicate implementation images.
- Set the cover separately with `从正文选择`, normally choosing the approved first image.
- Save explicitly, then verify the draft card has a non-empty cover and does not contain `内容不完整`.
- Never click `发表` for a draft-only request.
- If clicking a draft title opens `about:blank`, hover the exact draft card and use its visible `编辑` control instead.

## Scheduler horizons and daily continuations

Some platforms limit how far ahead a post can be scheduled. Do not choose a nearby but incorrect time.

When the requested time is outside the native horizon:

1. Save a complete draft.
2. Record the earliest valid follow-up time.
3. Create one local heartbeat automation with an explicit date-to-article mapping.
4. Recheck the management page before every continuation.
5. Tell the user that the computer, Codex, Chrome, and signed-in session must be available.

For platforms without a native scheduler, such as the observed Zhihu article editor, use the same draft-plus-heartbeat pattern and publish only one mapped article per run.

For a daily Zhihu sequence, store the exact date-to-title and draft-ID mapping in both the continuation prompt and the ignored local tracker. If the user has authorized automatic publication after verification, that standing authorization applies only to the mapped batch. After the management page confirms the day's public article, advance the automation so it cannot wake again until the next mapped date when the user has requested same-day suspension. Delete the automation after the last mapped article is published and verified.

When a pasted Zhihu image fails asynchronously, keep the current draft and inspect the figure state before changing the body. A local `blob:` source, error class, spinner, or `重试` control means the upload is not complete. Retry the existing upload once when the platform offers it, then require a server-hosted URL and the exact caption. Do not paste the full body again to repair one failed image.

## End-of-run verification

Run one consolidated verification pass instead of reopening each completed editor repeatedly. For every article check:

- exact title;
- expected figure/image count;
- every approved caption;
- first and last paragraphs;
- cover present;
- final platform state and exact time;
- platform record ID when available.

Update the single local tracker immediately after verification. Keep that tracker under ignored `local-data` paths.
