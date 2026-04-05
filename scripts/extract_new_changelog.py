#!/usr/bin/env python3
"""
增量式翻譯差異識別腳本

功能：
  1. 比對 upstream README.md 是否有更新（透過 SHA256 hash 比對）
  2. 比對 upstream changelog.md，找出「新版本區塊」（hash 比對確認的全新內容）

輸出：
  - repos/translate-work/upstream.README.md  (如果 README 需要翻譯)
  - repos/translate-work/new_changelog_blocks.md (新版本區塊英文原文，供 AI 翻譯)
  - repos/translate-work/flags.env (供 GitHub Actions YAML 讀取的環境變數 flag)
  - repos/current/.upstream_readme_hash (記錄上次翻譯時的 upstream README hash)

使用方式：
  python3 repos/current/scripts/extract_new_changelog.py
"""

import sys
import os
import hashlib


def parse_version_blocks(content):
    """
    將 changelog 內容解析為版本區塊 list。
    每個版本區塊以 '## ' 開頭的行作為標題。
    回傳： list of {'header': str, 'content': str}
    """
    lines = content.split('\n')
    blocks = []
    current_header = None
    current_block_lines = []

    for line in lines:
        if line.startswith('## '):
            # 遇到新的版本標題，先把上一個 block 存起來
            if current_header is not None:
                blocks.append({
                    'header': current_header,
                    'content': '\n'.join(current_block_lines).strip()
                })
            current_header = line
            current_block_lines = [line]
        elif current_header is not None:
            current_block_lines.append(line)

    # 別忘了最後一個 block
    if current_header is not None:
        blocks.append({
            'header': current_header,
            'content': '\n'.join(current_block_lines).strip()
        })

    return blocks


def check_readme(flags):
    """
    比對 upstream README.md 的 SHA256 hash。
    若與上次記錄的 hash 不同，代表上游有更新，設定 TRANSLATE_README=true。
    """
    upstream_readme = 'repos/upstream/README.md'
    hash_record = 'repos/current/.upstream_readme_hash'

    if not os.path.exists(upstream_readme):
        print('[README] 找不到上游 README.md，跳過。')
        flags['TRANSLATE_README'] = 'false'
        return

    with open(upstream_readme, 'r', encoding='utf-8') as f:
        upstream_content = f.read()

    upstream_hash = hashlib.sha256(upstream_content.encode()).hexdigest()

    # 讀取上次記錄的 hash
    old_hash = ''
    if os.path.exists(hash_record):
        with open(hash_record, 'r') as f:
            old_hash = f.read().strip()

    if upstream_hash != old_hash:
        print(f'[README] 上游有變更，需要翻譯。'
              f'(hash: {old_hash[:8] or "N/A"}... -> {upstream_hash[:8]}...)')
        # 將上游 README 複製到翻譯工作區
        with open('repos/translate-work/upstream.README.md', 'w', encoding='utf-8') as f:
            f.write(upstream_content)
        # 將空的 README.md 放入工作區（供 AI 覆寫）
        current_readme = 'repos/current/README.md'
        if os.path.exists(current_readme):
            with open(current_readme, 'r', encoding='utf-8') as f:
                current_content = f.read()
            with open('repos/translate-work/README.md', 'w', encoding='utf-8') as f:
                f.write(current_content)
        # 記錄新的 hash（會在 Step 7 一起 Commit）
        with open('repos/current/.upstream_readme_hash', 'w') as f:
            f.write(upstream_hash)
        flags['TRANSLATE_README'] = 'true'
    else:
        print('[README] 上游未變更，不需要重新翻譯。')
        flags['TRANSLATE_README'] = 'false'


def check_changelog(flags):
    """
    比對 upstream changelog.md 與 current changelog.md。
    找出上游有但目前沒有的新版本區塊，輸出到 new_changelog_blocks.md。
    """
    upstream_changelog = 'repos/upstream/changelog.md'
    current_changelog = 'repos/current/changelog.md'

    if not os.path.exists(upstream_changelog):
        print('[CHANGELOG] 找不到上游 changelog.md，跳過。')
        flags['TRANSLATE_CHANGELOG'] = 'false'
        return

    with open(upstream_changelog, 'r', encoding='utf-8') as f:
        upstream_content = f.read()

    current_content = ''
    if os.path.exists(current_changelog):
        with open(current_changelog, 'r', encoding='utf-8') as f:
            current_content = f.read()

    upstream_blocks = parse_version_blocks(upstream_content)
    current_blocks = parse_version_blocks(current_content)

    # 建立目前已有的版本標題集合（用 strip() 避免空白問題）
    current_headers = set(block['header'].strip() for block in current_blocks)

    # 從上游的最新版本開始向下掃描，直到遇到已有的版本為止
    new_blocks = []
    for block in upstream_blocks:
        if block['header'].strip() not in current_headers:
            new_blocks.append(block)
        else:
            # 遇到已翻譯過的版本，立刻停止（假設版本是由新到舊排列）
            break

    if new_blocks:
        new_content = '\n\n'.join(block['content'] for block in new_blocks)
        with open('repos/translate-work/new_changelog_blocks.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        flags['TRANSLATE_CHANGELOG'] = 'true'
        flags['NEW_BLOCK_COUNT'] = str(len(new_blocks))
        print(f'[CHANGELOG] 發現 {len(new_blocks)} 個新版本區塊：')
        for block in new_blocks:
            print(f'  - {block["header"]}')
    else:
        print('[CHANGELOG] 沒有新的版本區塊，不需要翻譯。')
        flags['TRANSLATE_CHANGELOG'] = 'false'
        flags['NEW_BLOCK_COUNT'] = '0'


def main():
    os.makedirs('repos/translate-work', exist_ok=True)

    flags = {}

    print('=== Step A: 檢查 README.md ===')
    check_readme(flags)

    print('\n=== Step B: 檢查 changelog.md ===')
    check_changelog(flags)

    # 將 flags 寫入 flags.env 供 YAML 讀取
    flags_env_path = 'repos/translate-work/flags.env'
    with open(flags_env_path, 'w') as f:
        for key, value in flags.items():
            f.write(f'{key}={value}\n')

    print(f'\n=== Flags Summary ===')
    for k, v in flags.items():
        print(f'  {k}={v}')

    print('\n識別腳本執行完畢。')


if __name__ == '__main__':
    main()
