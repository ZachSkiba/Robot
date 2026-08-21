# Git Workflow

## Branches

* `main` = stable/released code
* `dev` = active development
* `feature/*` = individual features

## Rules

1. Feature branches are **always created from `dev`**.
2. Developers work **only on feature branches**.
3. Never push directly to `dev` or `main`.
4. Feature branches are merged into `dev` after testing.
5. `dev` is merged into `main` when stable.
6. Delete feature branches after they are merged.

---

## Start New Feature

```bash
git fetch origin
git switch dev
git pull origin dev
git switch -c feature/my-feature
```

## Work

```bash
git add .
git commit -m "..."
git push -u origin feature/my-feature
```

## Get an Existing GitHub Branch

```bash
git fetch origin
git switch --track origin/feature/my-feature
```

## Update Existing Branch

```bash
git pull
```

---

## Merge Feature → Dev

```bash
git switch dev
git pull origin dev
git merge feature/my-feature
git push origin dev
```

## Delete Feature

Delete the local branch:

```bash
git branch -d feature/my-feature
```

Delete the GitHub branch:

```bash
git push origin --delete feature/my-feature
```

Delete old remote branch:

```bash
git fetch --prune
```

---

## Promote Dev → Main

```bash
git switch main
git pull origin main
git merge dev
git push origin main
```

---

## Check GitHub Branches

```bash
git fetch origin
git branch -a
```
