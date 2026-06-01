#!/usr/bin/env python3
"""旺财日报 - 每日内容发布脚本
从思源笔记读取每日丰富内容，生成 Hugo markdown 并推送 GitHub
由 OpenClaw cron 在每日 12:00 触发
"""
import json, os, sys, subprocess, re, html as html_mod, urllib.request
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
REPO_DIR = "/home/node/.openclaw/workspace/wangcai-daily"
RUNS_DIR = "/home/node/.openclaw/cron/runs"
SIYUAN_API = "http://127.0.0.1:6806"
SIYUAN_TOKEN = "vuxrvnahxh29e6pm"
SIYUAN_NOTEBOOK = "20260517160427-xnp6zc1"

today = datetime.now(TZ).strftime("%Y-%m-%d")
today_display = datetime.now(TZ).strftime("%Y年%m月%d日")
page_file = f"{today}-daily.md"
post_dir = os.path.join(REPO_DIR, "content", "posts")
page_path = os.path.join(post_dir, page_file)
EXCLUDE_SECTIONS = ["每日学习", "今日待办"]


def read_siyuan_note(date_str):
    list_req = {"notebook": SIYUAN_NOTEBOOK, "path": "/"}
    list_data = json.dumps(list_req).encode()
    req = urllib.request.Request(
        f"{SIYUAN_API}/api/filetree/listDocsByPath", data=list_data,
        headers={"Authorization": f"Token {SIYUAN_TOKEN}", "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
    except: return None
    if result.get("code") != 0: return None
    files_data = result.get("data", {})
    files_list = files_data.get("files", []) if isinstance(files_data, dict) else (files_data if isinstance(files_data, list) else [])
    doc_id = None
    for f in files_list:
        if isinstance(f, dict) and f.get("name", "").startswith(date_str):
            doc_id = f.get("id"); break
    if not doc_id: return None
    export_req = {"id": doc_id}
    export_data = json.dumps(export_req).encode()
    req2 = urllib.request.Request(
        f"{SIYUAN_API}/api/export/exportMdContent", data=export_data,
        headers={"Authorization": f"Token {SIYUAN_TOKEN}", "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            result2 = json.loads(resp2.read())
    except: return None
    if result2.get("code") != 0: return None
    return result2["data"]["content"]


def parse_markdown_sections(md_content):
    sections = []
    lines = md_content.split('\n')
    current_title = None; current_content = []; in_front_matter = False
    def save_current():
        if current_title and current_content:
            if not any(excl in current_title for excl in EXCLUDE_SECTIONS):
                body = '\n'.join(current_content).strip()
                if body: sections.append({"name": current_title, "content": body})
    for line in lines:
        stripped = line.strip()
        if stripped == '---' and not in_front_matter: in_front_matter = True; continue
        if stripped == '---' and in_front_matter: in_front_matter = False; continue
        if in_front_matter: continue
        h2_match = re.match(r'^##\s+(.+)$', stripped)
        if h2_match:
            save_current()
            current_title = h2_match.group(1).strip()
            current_content = []
        elif current_title:
            current_content.append(line)
    save_current()
    return sections


def collect_sections_from_siyuan():
    md = read_siyuan_note(today)
    if not md: return None
    sections = parse_markdown_sections(md)
    if not sections: return None
    for sec in sections:
        title = re.sub(r'\s*[—\-–]\s*\d{4}-\d{2}-\d{2}\s*$', '', sec["name"]).strip()
        sec["name"] = re.sub(r'\s*—.*$', '', title).strip()
    print(f"  📖 思源笔记读取到 {len(sections)} 个板块")
    return sections


def collect_sections_from_cron():
    sections = []
    TASKS = [
        ("morning-news", "📰 晨间新闻"), ("ai-news", "🤖 AI 新闻速递"),
        ("chen-editor", "📋 陈版主日报"), ("it-audit", "🔍 IT 审计资讯"),
        ("hot-news-recap", "🔥 昨日热榜"), ("study-review", "📖 备考复盘"),
    ]
    for job_id, display_name in TASKS:
        log_file = os.path.join(RUNS_DIR, f"{job_id}.jsonl")
        if not os.path.exists(log_file): continue
        today_entries = []
        with open(log_file) as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    entry = json.loads(line); ts = entry.get("runAtMs", 0)
                    if ts and datetime.fromtimestamp(ts/1000, tz=TZ).strftime("%Y-%m-%d") == today:
                        today_entries.append(entry)
                except: continue
        if not today_entries: continue
        latest = today_entries[-1]
        content = ""
        for field in ["messagingToolSentTexts", "assistantTexts", "summary"]:
            val = latest.get(field)
            if val:
                if isinstance(val, list) and val: content = max(val, key=len) if field == "assistantTexts" else val[0]
                elif isinstance(val, str): content = val
            if content: break
        if content: sections.append({"name": display_name, "content": content})
    return sections


def collect_sections(cron_fallback=True):
    all_sections = []
    siyuan = collect_sections_from_siyuan()
    if siyuan: all_sections.extend(siyuan); print(f"  📖 思源提供 {len(siyuan)} 个板块")
    if cron_fallback:
        cron = collect_sections_from_cron()
        if cron:
            existing_names = {s["name"] for s in all_sections}
            new_count = 0
            for cs in cron:
                if not any(cs["name"] in en or en in cs["name"] for en in existing_names):
                    all_sections.append(cs); new_count += 1
            if new_count > 0: print(f"  📋 cron 补充 {new_count} 个板块")
    return all_sections


def generate_hugo_post(sections):
    parts = []
    for sec in sections:
        parts.append(f"**{sec['name']}**\n\n{sec['content']}\n")
    body = "\n---\n".join(parts)
    return f"""---
title: "旺财日报 · {today_display}"
date: {today}T12:00:00+08:00
draft: false
tags: ["日报"]
description: "今日资讯简报。"
---

{body}
"""


# ===== 主流程 =====
os.makedirs(post_dir, exist_ok=True)
sections = collect_sections(cron_fallback=True)
if not sections:
    print("今日无内容可发布，跳过"); sys.exit(0)

md = generate_hugo_post(sections)
with open(page_path, 'w') as f:
    f.write(md)
print(f"✅ Hugo 文章已生成: content/posts/{page_file}  ({len(sections)} 个板块)")

os.chdir(REPO_DIR)
subprocess.run(["git", "add", f"content/posts/{page_file}"], check=True)
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
if not status.stdout.strip():
    print("  无变更，跳过提交"); sys.exit(0)
subprocess.run(["git", "commit", "-m", f"docs: 添加 {today} 日报"], check=True)
try:
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], capture_output=True, text=True, timeout=15)
except: pass
try:
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print(f"\n✅ 已推送到 GitHub")
    else:
        print(f"\n⚠️ 推送失败: {result.stderr[:300]}")
        subprocess.run(["git", "reset", "HEAD~1", "--soft"], capture_output=True)
except subprocess.TimeoutExpired:
    print(f"\n⚠️ 推送超时")
    subprocess.run(["git", "reset", "HEAD~1", "--soft"], capture_output=True)
