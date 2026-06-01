#!/usr/bin/env python3
"""旺财日报 - 每日内容发布脚本
从 cron run logs 中提取今日推送内容，生成 HTML 页面并推送 GitHub Pages
由 OpenClaw cron 在每日 12:00 触发
"""
import json, os, sys, subprocess
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
REPO_DIR = "/home/node/.openclaw/workspace/wangcai-daily"
CONTENT_DIR = REPO_DIR
RUNS_DIR = "/home/node/.openclaw/cron/runs"

today = datetime.now(TZ).strftime("%Y-%m-%d")
today_display = datetime.now(TZ).strftime("%Y年%m月%d日")
page_file = f"{today}.html"

# 任务配置
TASKS = [
    ("morning-news", "📰 晨间新闻"),
    ("daily-study-push", "📚 每日学习"),
    ("ai-news", "🤖 AI 新闻速递"),
    ("chen-editor", "📋 陈版主日报"),
    ("it-audit", "🔍 IT 审计资讯"),
    ("hot-news-recap", "🔥 昨日热榜"),
    ("study-review", "📖 备考复盘"),
    ("ics-today-tasks", "📅 今日待办"),
]

def load_today_content(job_id, latest):
    """从今日运行记录中提取内容"""
    content = ""
    # 方式1：messagingToolSentTexts（message 工具发送的完整内容）
    delivered_msgs = latest.get("messagingToolSentTexts", [])
    if delivered_msgs and delivered_msgs[0]:
        content = delivered_msgs[0]
    # 方式2：assistantTexts 最终回复
    if not content:
        assistant_texts = latest.get("assistantTexts", [])
        if assistant_texts:
            sorted_texts = sorted(assistant_texts, key=len, reverse=True)
            content = sorted_texts[0]
    # 方式3：summary
    if not content:
        content = latest.get("summary", "")
    return content

def collect_sections():
    """收集今日所有板块内容"""
    sections = []
    for job_id, display_name in TASKS:
        log_file = os.path.join(RUNS_DIR, f"{job_id}.jsonl")
        if not os.path.exists(log_file):
            continue
        today_entries = []
        with open(log_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = entry.get("runAtMs", 0)
                    if ts:
                        dt = datetime.fromtimestamp(ts / 1000, tz=TZ).strftime("%Y-%m-%d")
                        if dt == today:
                            today_entries.append(entry)
                except:
                    continue
        if not today_entries:
            continue
        latest = today_entries[-1]
        content = load_today_content(job_id, latest)
        if content:
            sections.append({"name": display_name, "content": content})
    return sections

def md_to_html(text):
    """简单的 Markdown 转 HTML"""
    import html
    text = html.escape(text)
    lines = text.split('\n')
    result = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('## '):
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(f'<h3>{stripped[3:]}</h3>')
        elif stripped.startswith('# '):
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(f'<h2>{stripped[2:]}</h2>')
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{stripped[2:]}</li>')
        elif stripped.startswith('1. ') or stripped.startswith('2. ') or stripped.startswith('3. '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{stripped[3:]}</li>')
        elif stripped.startswith('---'):
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append('<hr>')
        elif stripped == '':
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append('')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            # 处理粗体和链接
            line_html = stripped
            # 粗体 **text**
            import re
            line_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line_html)
            # 链接 [text](url)
            line_html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', line_html)
            if line_html:
                result.append(f'<p>{line_html}</p>')
            else:
                result.append('<br>')
    if in_list:
        result.append('</ul>')
    return '\n'.join(result)

def get_existing_pages():
    """获取已发布的文章列表"""
    pages = []
    for f in os.listdir(CONTENT_DIR):
        if f.endswith('.html') and f[0].isdigit():
            date_str = f[:10]
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                pages.append((date_str, f))
            except:
                continue
    pages.sort(reverse=True)
    return pages

def generate_page(sections):
    """生成今日日报 HTML 页面"""
    body_parts = []
    for sec in sections:
        body_parts.append(f'''
        <div class="section">
          <h2>{sec['name']}</h2>
          <div class="section-content">
            {md_to_html(sec['content'])}
          </div>
        </div>
        ''')

    body_html = '\n'.join(body_parts)

    if not body_html:
        body_html = '<p style="text-align:center;color:#aaa;padding:40px 0;">今日暂无内容更新 🐶</p>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>旺财日报 · {today_display}</title>
  <link rel="alternate" type="application/rss+xml" href="feed.xml" title="旺财日报">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif; line-height: 1.6; color: #333; background: #f8f9fa; }}
    .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
    header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #fff; padding: 30px 0; text-align: center; }}
    header h1 {{ font-size: 1.8em; margin-bottom: 5px; }}
    header h1 a {{ color: #fff; text-decoration: none; }}
    header p {{ font-size: 0.9em; opacity: 0.8; }}
    .nav-links {{ margin-top: 10px; }}
    .nav-links a {{ color: #e94560; text-decoration: none; font-size: 0.85em; margin: 0 10px; }}
    .post {{ background: #fff; padding: 30px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
    .post-date {{ color: #888; font-size: 0.85em; margin-bottom: 15px; text-align: center; }}
    .section {{ margin: 20px 0; padding: 15px 0; border-bottom: 1px solid #f0f0f0; }}
    .section:last-child {{ border-bottom: none; }}
    .section h2 {{ font-size: 1.2em; color: #1a1a2e; border-bottom: 2px solid #e94560; padding-bottom: 8px; margin-bottom: 12px; }}
    .section h3 {{ font-size: 1.05em; color: #0f3460; margin: 12px 0 6px; }}
    .section-content {{ font-size: 0.95em; }}
    .section-content p {{ margin: 6px 0; }}
    .section-content ul {{ padding-left: 20px; margin: 6px 0; }}
    .section-content li {{ margin: 3px 0; }}
    .section-content hr {{ border: none; border-top: 1px solid #eee; margin: 15px 0; }}
    .section-content a {{ color: #e94560; }}
    .section-content strong {{ color: #0f3460; }}
    .section-content blockquote {{ border-left: 3px solid #e94560; padding: 5px 12px; margin: 8px 0; background: #f8f9fa; color: #666; font-size: 0.9em; }}
    .footer {{ text-align: center; font-size: 0.8em; color: #aaa; margin: 30px 0; padding: 15px; border-top: 1px solid #eee; }}
    .footer a {{ color: #e94560; text-decoration: none; }}
    .home {{ background: #fff; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
    .home h2 {{ font-size: 1.1em; color: #888; margin-bottom: 15px; }}
    .home-item {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; }}
    .home-item:last-child {{ border-bottom: none; }}
    .home-item a {{ color: #1a1a2e; text-decoration: none; flex: 1; }}
    .home-item a:hover {{ color: #e94560; }}
    .home-item .date {{ font-size: 0.8em; color: #888; min-width: 85px; }}
    .rss-badge {{ display: inline-block; background: #f60; color: #fff; padding: 2px 8px; border-radius: 3px; font-size: 0.75em; vertical-align: middle; text-decoration: none; }}
    .back-link {{ display: inline-block; margin-bottom: 15px; color: #e94560; text-decoration: none; font-size: 0.9em; }}
    @media (max-width: 600px) {{ .container {{ padding: 10px; }} .post {{ padding: 15px; }} header h1 {{ font-size: 1.4em; }} }}
  </style>
</head>
<body>
  <header>
    <div class="container">
      <h1><a href="/wangcai-daily/">🐶 旺财日报</a></h1>
      <p>由旺财整理的每日资讯简报</p>
      <div class="nav-links">
        <a href="/wangcai-daily/">🏠 首页</a>
        <a href="/wangcai-daily/feed.xml">📡 RSS</a>
      </div>
    </div>
  </header>
  <div class="container">
    <div class="post">
      <h1 style="font-size:1.3em;text-align:center;">旺财日报 · {today_display}</h1>
      <div class="post-date">📅 {today_display}</div>
      {body_html}
      <div class="footer">
        <p>由旺仔整理发布 · <a href="/wangcai-daily/">返回首页</a> · <a href="/wangcai-daily/feed.xml">RSS 订阅</a></p>
      </div>
    </div>
  </div>
</body>
</html>'''

def generate_index(existing_pages):
    """生成首页 index.html"""
    items_html = []
    for date_str, fname in existing_pages:
        # 跳过首页本身和 feed
        if fname in ('index.html', 'feed.xml'):
            continue
        items_html.append(f'''
        <div class="home-item">
          <div class="date">📅 {date_str}</div>
          <a href="{fname}">旺财日报 · {date_str}</a>
        </div>
        ''')

    items = '\n'.join(items_html) if items_html else '<p style="text-align:center;color:#aaa;padding:40px 0;">暂无文章，等待首次发布 🐶</p>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>旺财日报</title>
  <link rel="alternate" type="application/rss+xml" href="feed.xml" title="旺财日报">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC", sans-serif; line-height: 1.6; color: #333; background: #f8f9fa; }}
    .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
    header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #fff; padding: 40px 0; text-align: center; }}
    header h1 {{ font-size: 2em; margin-bottom: 8px; }}
    header p {{ font-size: 1em; opacity: 0.8; }}
    .rss-link {{ display: inline-block; margin-top: 10px; background: #f60; color: #fff; padding: 4px 12px; border-radius: 4px; font-size: 0.85em; text-decoration: none; }}
    .home {{ background: #fff; padding: 25px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
    .home h2 {{ font-size: 1.1em; color: #888; margin-bottom: 15px; }}
    .home-item {{ padding: 14px 0; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; }}
    .home-item:last-child {{ border-bottom: none; }}
    .home-item a {{ color: #1a1a2e; text-decoration: none; flex: 1; font-size: 1.05em; }}
    .home-item a:hover {{ color: #e94560; }}
    .home-item .date {{ font-size: 0.85em; color: #888; min-width: 90px; }}
    .footer {{ text-align: center; font-size: 0.8em; color: #aaa; margin: 30px 0; padding: 15px; border-top: 1px solid #eee; }}
    .footer a {{ color: #e94560; text-decoration: none; }}
    @media (max-width: 600px) {{ .container {{ padding: 10px; }} header h1 {{ font-size: 1.5em; }} }}
  </style>
</head>
<body>
  <header>
    <div class="container">
      <h1>🐶 旺财日报</h1>
      <p>由旺仔整理的每日资讯简报 · 每天更新</p>
      <a class="rss-link" href="feed.xml">📡 RSS 订阅</a>
    </div>
  </header>
  <div class="container">
    <div class="home">
      <h2>📅 全部文章</h2>
      {items}
    </div>
  </div>
  <div class="footer">
    <p>由旺仔整理发布</p>
    <p style="margin-top:5px;"><a href="https://github.com/spring-admin/wangcai-daily">GitHub 仓库</a></p>
  </div>
</body>
</html>'''

def generate_rss(existing_pages):
    """生成 RSS feed"""
    now_rfc = datetime.now(TZ).strftime("%a, %d %b %Y %H:%M:%S +0800")
    items = []
    for date_str, fname in existing_pages[:10]:
        if fname in ('index.html', 'feed.xml'):
            continue
        pub_date = datetime.strptime(date_str, '%Y-%m-%d').strftime("%a, %d %b %Y 12:00:00 +0800")
        items.append(f'''    <item>
      <title>旺财日报 · {date_str}</title>
      <link>https://spring-admin.github.io/wangcai-daily/{fname}</link>
      <guid>https://spring-admin.github.io/wangcai-daily/{fname}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>旺财日报 · {date_str} - 每日资讯简报</description>
    </item>''')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>旺财日报</title>
    <link>https://spring-admin.github.io/wangcai-daily/</link>
    <description>由旺财整理的每日资讯简报</description>
    <language>zh-CN</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="https://spring-admin.github.io/wangcai-daily/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>'''

# ===== 主流程 =====
page_path = os.path.join(CONTENT_DIR, page_file)

# 如果今日文章已存在，更新它
if os.path.exists(page_path):
    print(f"今日文章已存在: {page_file}，更新中...")

# 收集内容
sections = collect_sections()

if not sections:
    # 尝试从 output/ 目录读取
    output_dir = "/home/node/.openclaw/workspace/tasks/output"
    output_map = {
        "morning-news.json": "📰 晨间新闻",
        "daily_study_push.json": "📚 每日学习",
        "ai-news.json": "🤖 AI 新闻速递",
        "chen-editor.json": "📋 陈版主日报",
        "it-audit.json": "🔍 IT 审计资讯",
    }
    for fname, display_name in output_map.items():
        fpath = os.path.join(output_dir, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath) as f:
                    d = json.load(f)
                content = d.get("content", d.get("summary", ""))
                if content:
                    sections.append({"name": display_name, "content": content})
            except:
                pass

if not sections:
    print("今日无内容可发布，跳过")
    sys.exit(0)

# 生成今日页面
page_html = generate_page(sections)
with open(page_path, 'w') as f:
    f.write(page_html)
print(f"✅ 文章已生成: {page_file}  ({len(sections)} 个板块)")
for sec in sections:
    print(f"   - {sec['name']}")

# 获取已有页面，重新生成首页和 RSS
existing_pages = get_existing_pages()

# 首页
index_html = generate_index(existing_pages)
with open(os.path.join(CONTENT_DIR, 'index.html'), 'w') as f:
    f.write(index_html)

# RSS
rss_xml = generate_rss(existing_pages)
with open(os.path.join(CONTENT_DIR, 'feed.xml'), 'w') as f:
    f.write(rss_xml)

# Git 提交并推送
os.chdir(REPO_DIR)

# 添加所有文件
subprocess.run(["git", "add", page_file], check=True)
subprocess.run(["git", "add", "index.html"], check=True)
subprocess.run(["git", "add", "feed.xml"], check=True)

# 检查是否有变更
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
if not status.stdout.strip():
    print("  无变更，跳过提交")
    sys.exit(0)

subprocess.run(["git", "commit", "-m", f"docs: 添加 {today} 日报"], check=True)

# 先拉取再推送
try:
    subprocess.run(["git", "pull", "--rebase", "origin", "main"],
                   capture_output=True, text=True, timeout=15)
except Exception:
    pass

try:
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        print(f"\n✅ 已推送到 GitHub Pages")
        print(f"   地址：https://spring-admin.github.io/wangcai-daily/")
    else:
        print(f"\n⚠️ 推送失败: {result.stderr[:300]}")
        subprocess.run(["git", "reset", "HEAD~1", "--soft"], capture_output=True)
except subprocess.TimeoutExpired:
    print(f"\n⚠️ 推送超时")
    subprocess.run(["git", "reset", "HEAD~1", "--soft"], capture_output=True)
