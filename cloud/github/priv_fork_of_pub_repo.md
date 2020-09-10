# Creating a Private Fork of a Public Repo

## Step by step

These instructions serve to guide the process for creating a private repo of a
fork for a public repo. The private repo should be able to pull changes from the
public (upstream) repo as well.

_with help from https://medium.com/@bilalbayasut/github-how-to-make-a-fork-of-public-repository-private-6ee8cacaf9d3_

_NOTE: If you have 2FA turned on for your GitHub account, you will need to
create a personal access token to login in. Visit
`https://github.com/settings/tokens` to generate one._

1. Create a private repo

- [For individuals](https://github.com/new)
- [For organizations](https://github.com/organizations/<org-name>/repositories/new)

2. Clone the **PUBLIC** repo

- `git clone --bare https://github.com/<user>/<public-repo.git> && cd <public-repo.git>`

3. Push to **PRIVATE** repo

- `git push --mirror https://github.com/<user>/<private-repo.git>`

4. Delete local copy of public repo

- `cd .. && rm -rf <public-repo.git>`

5. Clone the private repo

- `git clone https://github.com/<user>/<private-repo.git>`

## Condensed

Update the variables and save it to file so run as a script.

```bash
REPO_NAME='public-repo'
PUBLIC_REPO_URL='https://github.com/exampleuser/public-repo.git'
PRIVATE_REPO_URL='https://github.com/yourname/private-repo.git'

git clone --bare ${PUBLIC_REPO_URL}
cd ${REPO_NAME}
git push --mirror ${PRIVATE_REPO_URL}
cd ..
rm -rf ${REPO_NAME}
git clone ${PRIVATE_REPO_URL}
```

Once you have the repo set up, you can make changes like this.

```bash
cd <private-repo>
# make some changes
git commit
git push origin master
```

To pull changes from the public (upstream) repo do this.

_NOTE: you only need to add the remote once/_

```bash
# Add the upstream remote
cd <private-repo>
git remote add upstream <https://github.com/exampleuser/public-repo.git>
```

```bash
# Run this everytime you want to pull changes from the public
# upstream repo

# NOTE: You will have to resolve any conflicts that arise from this
git pull upstream master
```
