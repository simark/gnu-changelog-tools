#!/usr/bin/env python3

import email.utils
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

def get_date_rfc2822():
    return email.utils.formatdate(localtime=True)

def get_date_for_changelog():
    return time.strftime('%Y-%m-%d')


def get_author_name():
    return get_output(['git', 'log', '-n', '1', '--format=%aN'])


def get_author_email():
    return get_output(['git', 'log', '-n', '1', '--format=%aE'])


# Build a default changelog header, used when none is provided in the changelog.
def get_changelog_header():
    return '{}  {}  <{}>'.format(get_date_for_changelog(),
                                 get_author_name(),
                                 get_author_email())

# Build a header for a list of authors used when authors is provided in the
# changelog.
def build_changelog_header(authors):
    header = '{}  {}'.format(get_date_for_changelog(),
                             authors.pop(0))
    for author in authors:
        header = '{}\n\t    {}'.format(header, author)

    return header

def extract_changelog_entries(commit_msg):
    lines = commit_msg.split('\n')
    entries = {}
    current_changelog_file = None
    author_search = 0
    skip = 0

    for line in lines:
        if skip:
            skip = skip - 1
            continue

        if current_changelog_file is not None:
            m = re.match(r'^....-..-..  (.*  <.*@.*>)$', line)
            m2 = re.match(r'^\t    (.*  <.*@.*>)$', line)
            if author_search and m:
                author = m.group(1)
                entries[current_changelog_file]['authors'].append(author)
                continue
            elif author_search and m2:
                author = m2.group(1)
                entries[current_changelog_file]['authors'].append(author)
                continue
            elif author_search and entries[current_changelog_file]['authors']:
                author_search = 0
                continue
            else:
                author_search = 0

            if len(line) > 0 and line[0] == '\t':
                entries[current_changelog_file]['lines'].append(line)
            else:
                current_changelog_file = None
        else:
            m = re.match(r'^(([^/]+/)*ChangeLog):$', line)
            if m:
                current_changelog_file = m.group(1)
                assert current_changelog_file not in entries
                changelog = {}
                changelog['authors'] = []
                changelog['lines'] = []
                entries[current_changelog_file] = changelog

                author_search = 1
                # Skip empty line between .../ChangeLog: and content.
                skip = 1

    return entries


def write_changelog_entries(entries, gitroot):
    defheader = get_changelog_header()

    for path, changelog in entries.items():
        header = defheader
        line_list = changelog['lines']
        if changelog['authors']:
            header = build_changelog_header(changelog['authors'])

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
    os.environ['EDITOR'] = '/bin/true'
    execute(['git', 'add'] + changelog_files)
    execute(['git', 'commit', '--amend',
             '--date', get_date_rfc2822()])


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
