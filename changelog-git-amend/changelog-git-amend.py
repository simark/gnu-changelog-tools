#!/usr/bin/env python3

import re
import subprocess
import time

def execute(cmd, dry_run, check=True):
  if not dry_run:
    if check:
      subprocess.check_call(cmd)
    else:
      subprocess.call(cmd)
  else:
    print(' '.join(cmd))

def get_output(cmd_list):
  return subprocess.check_output(cmd_list, universal_newlines=True).strip()

def get_commit_message():
  return get_output(['git', 'log', '--format=format:%B', '-n', '1', 'HEAD'])

def get_date():
  return time.strftime('%Y-%m-%d')


def get_author_name():
  return get_output(['git', 'log', '-n', '1', '--format=%aN'])


def get_author_email():
  return get_output(['git', 'log', '-n', '1', '--format=%aE'])


def get_changelog_header():
  return '{}  {}  <{}>'.format(get_date(),
                             get_author_name(),
                             get_author_email())


def extract_changelog_entries(commit_msg):
  lines = commit_msg.split('\n')
  entries = {}
  current_changelog_file = None
  skip = 0
  
  for line in lines:
    if skip:
      skip = skip - 1
      continue
    
    if current_changelog_file != None:
      if len(line) > 0 and line[0] == '\t':
        entries[current_changelog_file].append(line)
      else:
        current_changelog_file = None
    else:
      m = re.match(r'^(([^/]+/)*ChangeLog):$', line)
      if m:
        current_changelog_file = m.group(1)
        assert current_changelog_file not in entries
        entries[current_changelog_file] = []

        # Skip empty line between .../ChangeLog: and content.
        skip = 1

  return entries


def write_changelog_entries(entries):
  header = get_changelog_header()

  for path, line_list in entries.items():
    to_add = header + '\n' + \
             '\n' + \
             '\n'.join(line_list) + \
             '\n' + \
             '\n'
    with open(path, 'r+') as f:
      data = to_add + f.read()
      f.seek(0)
      f.write(data)

def amend_commit(entries):
  changelog_files = list(entries.keys())
  execute(['git', 'add'] + changelog_files, dry_run=False, check=True)
  execute(['git', 'commit', '--amend', '--reset-author', '-m', ''], dry_run=False, check=True)

def main():
  commit_msg = get_commit_message()
  changelogs = extract_changelog_entries(commit_msg)
  write_changelog_entries(changelogs)
  amend_commit(changelogs)
  
if __name__ == '__main__':
  main()
