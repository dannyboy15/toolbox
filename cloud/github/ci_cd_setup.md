# CI/CD Setup

This runs through setting up a basic CI/CD[<sup id="p-ci-cd">1</sup>](#fn-ci-cd)
workflow. It will connect a [GitHub](https://github.com/) repo to
[CircleCI](https://circleci.com/) for testing and
[Docker Hub](https://hub.docker.com/) for building a docker image.

## Setting up GitHub

_Note: you will need admin permisions._

1. Create a repo

- if you're creating private fork of parsons,
  [read more about that here](./priv_fork_of_pub_repo.md)

2. (Optional) Generate ssh keys <a name="sshgen"></a>

- do this if your workflow will require write access to the repo e.g. you want
  CircleCI to update your docs.
- use the following command and don't enter a password
- `ssh-keygen -m PEM -t rsa -b 4096 -C "email@domain.com"`

3. (Optional) Add ssh keys to the repo

- https://github.com/<org-user>/<repo>/settings/keys
- copy public key to clipboard `cat ~/.ssh/id_rsa.pub | pbcopy`
- check [x] for write access

## Setting up CircleCi

CircleCi is for autmated testing and other CI/CD workflows. For example,
commited code can be tested and have results show up in GitHub PRs.

1. Sign in/create an account

- You can use your existing github account. This makes it trivial to link to
  your GitHub repos.
- If you want to include your organization, you will need admin access to
  grant CirlceCi permission to your repo.

2. Write yaml config file. [Sample here](https://circleci.com/docs/2.0/sample-config/)
3. Connect to Github

- this will automatcially generate an ssh key, keep it!
- Note: the aute-generated ssh key only has read access to your repo.

4. (Optional) Add an ssh key with write access

- Use the same key generated in [step 2 of Setting up GitHub](#sshgen)
- **NOTE: use the private key for this**
- https://app.circleci.com/settings/project/github/<org-user>/<repo>/ssh
- copy private key to clipboard `cat ~/.ssh/id_rsa | pbcopy`

## Setting up Docker Hub

1. Sign in/create an account
2. Connect to GitHub
3. Create a Docker Hub repo
4. Add build rule triggers
5. (Optional) Connect to Civis

- add `crobot` as a collaborator
- _(auth required) https://civis.zendesk.com/hc/en-us/articles/218200643-Container-Scripts_

### Config Auto Builds

**To build on update from master:**

> Source Type: Branch; Source: master; Tag: latest

**To build on update from any branch:**

'beta' would be fixed but '{sourceref}' would be the name of the branch

> Source Type: Branch; Source: /.\*/; Tag: beta-{sourceref}

---

<!-- TODO: Add more info on CI/CD -->

1. <span id="fn-ci-cd"></span> [CI = Continuous Integration, CD = Continuous
   Deployment](#p-ci-cd)
