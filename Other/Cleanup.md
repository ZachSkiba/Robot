# Repo Cleanup Guide — 6-DOF Arm Project

## Before You Touch Anything

```bash
git add .
git commit -m "snapshot: before repo cleanup"
```

Do not skip this. It is your undo button.

---

## Step 1 — Fix Phase Folder Naming (Sorting Bug)

Rename all phase folders so they sort correctly in file explorers and GitHub.

Current names sort like this: Phase0, Phase1, Phase10, Phase11, Phase2 — which is wrong.

Rename to zero-padded format:

| Old Name | New Name |
|---|---|
| Phase0-Plan | Phase00-Plan |
| Phase1-Arm | Phase01-Arm |
| Phase2-Trajectory | Phase02-Trajectory |
| Phase3-Optimize | Phase03-Optimize |
| Phase4-Learning | Phase04-Learning |
| Phase5-Vision | Phase05-Vision |
| Phase6-Autonomy | Phase06-Autonomy |
| Phase7-Optimization | Phase07-Optimization |
| Phase8-Deployment | Phase08-Deployment |
| Phase9-Specialization | Phase09-Specialization |
| Phase10-Mastery | Phase10-Mastery |
| Phase11+-Endgame | Phase11-Endgame |

> Remove the `+` from `Phase11+` — special characters in folder names cause issues on some systems.

---

## Step 2 — Rehome `Other/` and `Mini_Project/`

These folders have useful content but bad names. Do not delete them — move and rename.

**For `Mini_Project/`:**

Decide what it actually is. Pick one:
- If it's a standalone early prototype → move to `experiments/mini-project/`
- If it's part of Phase 1 → move content into `Phase01-Arm/`

**For `Other/`:**

Go through it file by file. For each file ask: *which phase or category does this belong to?*
Then move it there. If you genuinely cannot categorize something → move to `archive/unsorted/`.

Once both folders are empty → delete them.

---

## Step 3 — Create `archive/` and `experiments/`

```
Robot/
├── archive/          ← old content, nothing deleted
│   └── unsorted/
├── experiments/      ← mini projects, tests, throwaway work
```

This keeps the root clean without losing anything.

---

## Step 4 — Standardize File Names

Rename files to lowercase with hyphens. No spaces, no underscores, no capitals.

| Bad | Good |
|---|---|
| `New stuff.md` | `new-stuff.md` |
| `Overall_Project.md` | `overall-project.md` |
| `Project_Description.md` | `project-description.md` |
| `Software Setup.md` | `software-setup.md` |

> Only rename `.md` and `.txt` files. Do not rename source code files — that breaks imports.

---

## Step 5 — Create `docs/`

Move polished, presentable documentation here. This is what recruiters and professors read.

```
Robot/
└── docs/
    ├── README.md          ← index of all docs
    ├── setup/
    ├── architecture/
    └── hardware/
```

Only create subfolders you have content for right now. Empty folders look worse than no folders.

---

## Step 6 — Write the Root README

Create or overwrite `Robot/README.md` with this structure:

```markdown
# 6-DOF Robotic Arm

One sentence describing what this project is and what it does.

## Overview

2-3 sentences. What problem does this solve? What is the end goal?

## System Architecture

Short description or diagram of the overall system.
(Add a diagram here when you have one — even a rough one is better than none.)

## Project Structure

Brief explanation of what each top-level folder contains.

## Current Status

What phase are you in? What works right now? What is in progress?

## Setup

Link to docs/setup/ or list the steps directly.

## Team

Names and roles.

## Roadmap

Link to your phase folders or list phases briefly.
```

Write this in your own words. Do not leave placeholder text in — recruiters notice immediately.

---

## Step 7 — Commit Everything

```bash
git add .
git commit -m "refactor: repo structure cleanup and rename"
```

---

## Step 8 — Sanity Check

Ask yourself:
- Can a new team member find the setup docs in under 1 minute?
- Does the README explain what the project is without opening any other file?
- Are there any folders named `Other`, `New`, `Stuff`, or `Misc`?
- Are there any files with spaces in the name?

If any answer is wrong → fix it before pushing.

---

## What NOT to Do

- Do not create folders you have no content for yet
- Do not rename source code files
- Do not touch `.json`, `.yaml`, `Dockerfile`, `requirements.txt`, or any config
- Do not reorganize the `src/` ROS packages — that will break your build

---

## Priority Order

If this feels overwhelming, do it in this order. Stop after any step if you run out of time — each step is independently valuable.

1. Git commit (safety net)
2. Rename phase folders (fixes the sorting bug — highest visual impact)
3. Gut `Other/` and `Mini_Project/`
4. Write the README
5. Standardize file names
6. Create `docs/`