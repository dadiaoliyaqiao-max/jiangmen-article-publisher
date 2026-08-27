---
name: publish-jiangmen-articles
description: Prepare, localize, illustrate, review, and publish batches of Jiangmen-focused Chinese articles to Toutiao, WeChat Official Accounts, Baijiahao, Zhihu, and Sohu. Use when Codex receives one or more approved article manuscripts or Word documents and needs to match local images, preserve rich-text layout, paste the whole article once, add the title and cover separately, save drafts, schedule publication (usually 20:00), verify platform status, or continue an interrupted multi-platform publishing run.
---

# Publish Jiangmen Articles

Use one approved rich-text document as the source of truth. Paste the complete body once; never rebuild the article paragraph by paragraph.

## Read the operating references

Read [references/platform-playbook.md](references/platform-playbook.md) before operating publishing platforms. It contains platform-specific scheduling, verification, and recovery rules.

For browser automation, interrupted runs, timeouts, or multi-day batches, also read [references/recovery-runbook.md](references/recovery-runbook.md). It defines the Chrome-first control strategy, checkpoint model, and safe retry rules.

## Required workflow

1. Confirm the batch before editing:
   - List article titles, target dates, target platforms, and whether each platform should publish or save a draft.
   - Default time to 20:00 Asia/Shanghai only when the user has requested that schedule.
   - Preserve unrelated drafts and published content.
   - When a publish manifest exists, run `py -3 scripts/validate_publish_batch.py --manifest <path>` on Windows (or `python3 ...` elsewhere) before opening any platform editor.
2. Prepare one canonical rich-text稿 per article:
   - Keep the approved wording and paragraph order.
   - Insert each image directly after its corresponding paragraph or section.
   - Put a concise `▲ 图片内容说明` immediately below each image.
   - Do not write “AI生成” or negative disclaimers such as “非某项目现场/实景” in the visible image caption. Use a neutral, accurate description of what the image shows without claiming an unverified project source.
   - Do not include exact room numbers in captions.
   - Do not suppress a platform-required AI-content declaration when it genuinely applies.
3. Localize for Jiangmen without keyword stuffing:
   - Preserve natural mentions of 江门、江门楼盘、江门家居、江门装修 and verified local project or store names.
   - Prefer verified local cases, service radius, climate, housing type, delivery, installation, and after-sales context.
   - Never invent楼盘、门店、案例、资历、奖项 or customer facts.
4. Obtain the user's approval of the canonical稿 before publishing unless the user has already approved it.
5. Publish with the fast path:
   - Fill the title field separately.
   - Copy the entire approved rich-text body once and paste it into the editor once.
   - Reuse the same rich clipboard payload across all platform tabs until every body is pasted.
   - Upload or select the cover separately, normally using the approved first image unless a dedicated cover is supplied.
   - Add platform topics only when they are accurate; prefer `江门家居`, `江门装修`, `江门全屋定制`, or `家居`.
6. Verify cheaply, then schedule:
   - Check exact title, body image count, caption count, approximate text length, first paragraph, and final paragraph.
   - Open a full preview only when those checks disagree or the editor visibly changed formatting.
   - Set the requested date and 20:00 before the final submission.
   - Never click a final `发布` button merely to discover whether scheduling exists.
7. Record the authoritative result:
   - Capture the platform's success message or content-management row showing title, state, and scheduled time.
   - Update a publication matrix for every article and platform.
   - Keep incomplete work as a draft and report the exact remaining blocker.

## Speed rules

- Prepare all canonical稿件 and cover paths before opening platform editors.
- Process one article across all platforms while its rich-text body remains on the clipboard.
- Keep only the necessary publishing tabs open.
- Prefer the dedicated Chrome browser controller for logged-in publishing pages. Do not switch to Windows-level computer control merely because an editor is slow.
- Keep one clean management tab plus one current editor tab per platform. Use a fresh management tab to verify saved state instead of repeatedly attaching to a heavy or frozen editor.
- Use direct DOM checks instead of repeated screenshots or full-page snapshots.
- Perform one interaction, inspect the cheapest useful state, then continue.
- Allow long rich-text actions to finish. If an action times out, inspect the management page before retrying because the platform may have completed it asynchronously.
- Avoid local file uploads for body images when rich-text paste successfully transfers them; reserve uploads for covers or failed images.
- Do not refresh editors that autosave unless the current state is confirmed recoverable.
- Treat a CAPTCHA as a single blocking event: obtain the user's approval, solve it once, and continue without reloading.

## Failure recovery

- After interruption, inspect the current editor before pasting again.
- If title, text length, and image count match, continue from cover or scheduling.
- If the editor is unresponsive, leave it intact, open a fresh management tab, and locate the exact title and platform record ID. Resume the existing record from its edit control; do not create a same-title replacement unless the existing record is proven unrecoverable.
- Never repeat a paste, save, schedule, or publish action solely because the browser command timed out. First verify the platform's authoritative management row or draft card.
- For WeChat, count visible figures that contain images rather than raw internal `img` elements, which may be duplicated by the editor implementation.
- If a native scheduler is unavailable, save a complete draft and create a one-time Codex automation for the requested time. Tell the user the computer and Codex must be available for a local continuation.
- If a final publish happens early or unexpectedly, stop. Report it immediately; do not delete or retract the article without explicit approval.

## Completion report

Report each platform using only these states: `已定时`, `已发布`, `已保存草稿`, or `需用户处理`. Include the scheduled date/time or the precise reason it remains incomplete.

Distinguish these two completion levels:

- **制作完成**: canonical稿、图片、说明、标题、封面 and platform drafts/schedules are ready.
- **实际发布完成**: every scheduled date has passed and every platform management page confirms `已发布`.

Do not say “全部完成” when future Zhihu publications or scheduler-horizon follow-ups are still pending.
