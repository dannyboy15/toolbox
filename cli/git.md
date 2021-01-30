# Useful `git` commands

Here are some useful git commmands. The best way to learn is by practicing them.

## Setting up git

This goes through some basic git setup

**create a repo**

```bash
git init
```

Clone one fromt the internet

```bash
git clone https://url/for/repo.git
```

**configuring git**

View your current configurations

```bash
git config --list
```
Add your name and email. _Note: this configures the current repo, to set it
globally use the `--global` flag._

```bash
git config user.name 'FirstName LastName'
git config user.email 'myemail@email.com'
```


## Stashing files

When you are working in a branch (or master  😬) and you want to save your work
without committing it, you can do that by 'stashing' your work. Stashing removes
those files from your working directory and saves them for later use. This can
also come in handy when you have staged changes but need to quickly switch to
anther branch.

_Note: by default `git stash` only stashes teacked files_

**stash all modified tracked files**

```bash
git stash
```
**stash specific modified tracked files**

```bash
git stash <file1> <file2>
```

using globs

```bash
git stash <file*.txt> <dir/*>
```

# stash certain changes (not everything that's been modified)
git stash -p

**stash untracked files**

```bash
git stash push -u <files/dirs>
```

To bring back those files you will have to pop them from the stash. You can also
pop specific stashes by providing the stash id/number.

**pop the last stash**

```bash
git stash pop
```

**pop a specific stash**
You may want to list out the stashes first.

```bash
git stash list
```
```
stash@{0}: WIP on branch-1: 4h45h01 last commit message
stash@{1}: WIP on branch-1: 4h45h02 last commit message
```
```bash
git stash pop 1
```


## Making commits

The basic way to do this

```bash
git add <files>
git commit -m "Message"
```

By default, when git stages a file (i.e. `git add <file>`), it stages the whole
things. If you want to stage part of a file you can use the interactive mode.

```bash
git add -i <file>
```

**[TODO: include some info on add commands]**


## Editing commits

Editing commits can be really tricky so be careful. **Once you push your changes
to a remote server it is harder to edit the history**

### Basics

The apply to the last commit you made.

**change the commit message**

```bash
git commit --amend -m "My new commit message"
```

**update the author**

This would be useful if you forgot to configure your name/email and want to fix
it _after you have configured it_.

```bash
git commit --amend --reset-author --no-edit
```
It may also be useful if you need to edit the commit to attribute someone else.

```bash
git commit --amend --author="Author Name <email@address.com>"
```

### Advanced

This is where things can get trickier so be patient and be careful.

To edit various commit, you can use the rebase command. This allows you to edit
the commit, edit the commit message, squash or separate commits.

The `-i` makes it interactive. The `5` in `HEAD~5` tells git to include the last
5 commit in this rebase session.

```bash
git rebase -i HEAD~5
```

Once your start rebasing use the commands to make the changes.

**[TODO: include some info on rebase commands]**


## Diffs and viewing changes

_Note: this uses the mac `diff` command, which is different than runnig
`git diff`.

Get the diff of 2 files, ignoring double quotes/single quotes and redirect
the diff to a file. Add the `.diff` file extension for syntax highlighting in
test editors.

The key here is `--ignore-matching-lines="['\"].*['\"]"`. It tells `diff` to
ignore changes if the only difference is a starting and ending single/double
qoute.

```bash
diff --ignore-matching-lines="['\"].*['\"]" file.txt file2.txt > files.diff
```

## TODO
- [ ] include some info on add commands
- [ ] include some info on rebase commands
- [ ] add info on git-cherry-pick
- [ ] add info on git-reflog
