 Description
-----------

`changelog-git-amend` can be used to extract the ChangeLog content from the
message of the current commit, insert it in the appropriate ChangeLog files
and amend the commit.

It can be used standalone, where it will work on the currently checked out
commit.  It can also be used in conjunction with git rebase to apply the
operation on many commits.

The ChangeLog content should be laid out this way:

path/to/ChangeLog:

        * ChangeLog content...
        
path/to/otherChangeLog:

        * Other ChangeLog content...

Example
-------

Here is an example that uses `changelog-git-amend` with `git rebase`.

```
$ EDITOR=/bin/true git rebase master -i --exec changelog-git-amend.py
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 13ee93e] Factor out print_unpacked_pointer from generic_val_print
 2 files changed, 37 insertions(+), 17 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 618313a] Factor out array printing code from generic_val_print
 2 files changed, 47 insertions(+), 25 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD a0ae190] Factor out pointer printing code from generic_val_print
 2 files changed, 32 insertions(+), 12 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD c79d716] Factor out memberptr printing code from generic_val_print
 2 files changed, 21 insertions(+), 2 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD f594f73] Factor out reference printing code from generic_val_print
 2 files changed, 56 insertions(+), 37 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD adc758b] Factor out enum printing code from generic_val_print
 2 files changed, 77 insertions(+), 57 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 4e90576] Factor out flags printing code from generic_val_print
 2 files changed, 24 insertions(+), 6 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 3cc34f1] Factor out function/method printing code from generic_val_print
 2 files changed, 37 insertions(+), 15 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 4c85072] Factor out bool printing code from generic_val_print
 2 files changed, 39 insertions(+), 18 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 7fddbc3] Factor out int printing code from generic_val_print
 2 files changed, 29 insertions(+), 11 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 5ca57b6] Factor out char printing code from generic_val_print
 2 files changed, 40 insertions(+), 20 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 3266d9d] Factor out float printing code from generic_val_print
 2 files changed, 27 insertions(+), 9 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD 405cdb2] Factor out decfloat printing code from generic_val_print
 2 files changed, 23 insertions(+), 6 deletions(-)
Executing: /home/simark/src/gnu-changelog-tools/changelog-git-amend/changelog-git-amend.py
[detached HEAD f52a229] Factor out complex printing code from generic_val_print
 2 files changed, 39 insertions(+), 23 deletions(-)
Successfully rebased and updated refs/heads/split_generic_val_print.

```
