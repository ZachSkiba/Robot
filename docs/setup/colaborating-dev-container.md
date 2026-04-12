# Dev Container Onboarding — Partner Guide

## What Your Partner Needs Installed (One-Time, On Their Machine)

1. Git
2. Docker Desktop
3. VS Code
4. VS Code extension: **Dev Containers**

No ROS. No manual dependencies. The container handles all of that.

---

## First Time Setup (One-Time)

```bash
git clone <your-repo-url>
cd Robot
```

Then in VS Code:
- Open the `Robot` folder
- VS Code will prompt: **"Reopen in Container"** → click it
- Wait for the container to build
- Run `colcon build` to verify everything works

If the build fails — inspect the logs, run a clean build, then tell you. Do not install or modify dependencies to fix it. That's a repo problem, not a local one.

**Clean build (if needed):**
```bash
rm -rf build install log
colcon build
```

---

## Branch Protection on Main (Do This Before Anything Else)

Go to your GitHub repo → **Settings → Branches → Add rule** for `main`:

- ✅ Require pull request before merging
- ✅ Require at least 1 approval
- ✅ Block direct pushes

This is not optional. Without it, someone will push directly to `main` "just this once." Once is all it takes.

---

## Every Time They Work Solo

```bash
git pull                          # always first
# do work
git add .
git commit -m "fix: description"
git push
```

**Rules:**
- Pull before touching anything
- If `git pull` results in conflicts, stop and coordinate before resolving them
- Never commit `build/`, `install/`, or `log/`
- Branches may be broken temporarily — that's acceptable
- `main` must always build — that is non-negotiable
- PRs must build cleanly before merging

---

## When You Work Together at the Same Time

You do not both work on `main`. Direct pushes to `main` are blocked anyway (see above).

**Each person uses a branch:**
```bash
git checkout -b yourname/what-youre-doing
```

When done → push branch → open a Pull Request → other person reviews → merge to `main`.

---

## If They Need a Local Config File

Some files aren't in the repo intentionally. If something is missing:

1. Look for a `.example` version (e.g., `.env.example`)
2. Copy it: `cp .env.example .env`
3. Fill in the local values
4. Do not commit the real file

**If a file is not meant for Git and has no template, stop and ask before creating it.** Calibration files, hardware-specific YAMLs, test configs — all of these count. Silent local divergence is how environments fall out of sync without anyone noticing.

---

## If You Want to Work Live Together

Use **VS Code Live Share** inside the container. One person shares, the other joins. One person drives at a time unless you explicitly split into separate files.

---

## What They Must Never Do

- Install ROS or any packages directly on their machine
- Modify `.devcontainer/` without telling you and branching first
- Commit anything from `build/`, `install/`, `log/`
- Push directly to `main` (it's blocked, but don't try)
- Install or modify dependencies inside the container to fix a build failure