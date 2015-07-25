#!/usr/bin/env python3

import os
import re
import subprocess
import sys
import time


def execute(cmd):
    subprocess.check_call(cmd)


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

        if current_changelog_file is not None:
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


def write_changelog_entries(entries, gitroot):
    header = get_changelog_header()

    for path, line_list in entries.items():
        to_add = header + '\n' + \
            '\n' + \
            '\n'.join(line_list) + \
            '\n' + \
            '\n'
        with open(os.path.join(gitroot, path), 'r+') as f:
            data = to_add + f.read()
            f.seek(0)
            f.write(data)


def amend_commit(entries, gitroot):
    changelog_files = [os.path.join(gitroot, x) for x in entries.keys()]
    execute(['git', 'add'] + changelog_files)
    execute(['git', 'commit', '--amend', '--reset-author', '-m', ''])


def find_git_root():
    return get_output(['git', 'rev-parse', '--show-toplevel'])


def main():
    try:
        gitroot = find_git_root()
    except subprocess.CalledProcessError:
        print('It seems we are not in a git repo.')
        sys.exit(1)

    commit_msg = get_commit_message()
    changelogs = extract_changelog_entries(commit_msg)
    write_changelog_entries(changelogs, gitroot)
    amend_commit(changelogs, gitroot)

if __name__ == '__main__':
    main()
