---
name: notion-consolidate-notes
description: >
  Consolidates Notion subpages (notes, meeting notes, research pages, etc.) directly onto their
  parent pages as inline content — each note's title becomes an H1 heading and its full content
  appears below it on the same page. Use this skill whenever the user wants to merge, consolidate,
  flatten, or inline Notion subpages into a parent page, or says things like "put all my notes on
  one page", "consolidate my Notion pages", "merge these notes into the parent", "inline my
  subpages", "combine all notes into one", or any variation where individual Notion child pages
  need to be brought together as readable content on a parent. Also trigger when the user wants
  to reorganise a Notion database by collapsing note subpages into category/section pages.
---

# Notion: Consolidate Notes into Parent Pages

This skill flattens a set of Notion subpages into their parent pages as inline content. Instead of having many individual note pages linked as children, all the content lands directly on the parent — with each note's title as an H1 heading and the full note body below it. This makes everything readable in one place without clicking in and out of subpages.

## Step 1 — Understand the structure

Before writing anything, fetch the parent page(s) to understand what's already there and which child pages need to be consolidated. You need to know:

- Which pages are the **targets** (the parents that will receive the consolidated content)
- Which pages are the **sources** (the note subpages whose content will be written inline)
- Whether you're consolidating into one parent or multiple parents (e.g. category pages)

Ask the user if anything is unclear — specifically which pages are sources and which are targets.

## Step 2 — Fetch all source note pages in parallel

Use `notion-fetch` to retrieve every source note page. Send **all fetches in a single parallel batch** — don't wait for each one before starting the next. This is much faster and scales well to 20+ notes.

## Step 3 — Write content to each parent page

For each parent/target page, build a single consolidated content string containing all its source notes, then call `notion-update-page` with `command: "insert_content"` once per parent. Batching everything into one call per parent avoids race conditions and is more efficient than one call per note.

**Format each note as:**
```
# [Note title]

[Note content — full body, preserving all headings, bullets, tables etc.]
```

The `#` (H1) heading acts as a clear visual separator between notes. Preserve the original note order (typically chronological).

### Content cleaning rules

Notion's markdown export contains some elements that don't transfer cleanly. Apply these rules when building the content string:

| Element | Rule |
|---|---|
| Images (`![](https://...s3...amazonaws...`) | **Skip entirely** — S3 URLs are time-limited and expire immediately |
| Coloured text spans (`<span color="...">text</span>`) | Strip the tags, **keep the text** |
| Underline spans (`<span underline="true">text</span>`) | Strip the tags, **keep the text** |
| Page links (`<page url="...">label</page>`) | **Skip entirely** — these are references to other pages and don't make sense inline |
| Table of contents (`<table_of_contents>`) | **Skip entirely** |
| Callout blocks (`<callout ...>text</callout>`) | Keep the text content, skip the icon/colour markup |
| Tables (`<table ...>`) | Convert to standard Markdown table format: `\| col \| col \|` with a header row separator |
| Mention-page tags (`<mention-page url="..."/>`) | **Skip entirely** |
| Empty blocks (`<empty-block/>`) | Render as a blank line |

The goal is clean, readable plain markdown. When in doubt, keep the text and strip the markup.

### Handling very long notes

If a note is extremely long (e.g. a detailed F2F meeting with many sections), it's fine to include it in the same `insert_content` call as other notes — Notion handles large content well. Only split into separate calls if you're genuinely concerned about hitting a timeout.

## Step 4 — Confirm completion

After all writes succeed, tell the user:
- Which parent pages were updated and how many notes were consolidated into each
- That the **original note subpages still exist** and need to be manually deleted

### Why manual deletion is required

The Notion MCP doesn't currently include a delete/archive tool. To remove the original note pages, the user should open each parent page in Notion, select the note subpages listed there, and press **Delete** to send them to trash. This is quick — usually one Ctrl+A / Cmd+A to select all child pages, then Delete.

## Tips

- **Always fetch before writing** — don't guess at content or titles. The fetched content is the source of truth.
- **Parallel fetches, one write per parent** — this pattern is both fast and safe.
- **Preserve structure** — don't summarise or reformat the note content. The user wants the original notes consolidated, not rewritten.
- **Check for existing content** — if the parent page already has content, `insert_content` appends to it, which is usually the right behaviour. Mention this to the user if relevant.
- **Multiple database structures** — this workflow applies whether the notes live in a Notion database (entries with a parent set to the category page) or as regular page children. The fetch/write approach is the same either way.
