# Repo Cleanup Guide v2 — 6-DOF Arm Project

## Before You Touch Anything

```bash
git diff HEAD
```

Read every line. Codex already created files — verify they are correct before proceeding.

If anything looks wrong:

```bash
git checkout -- .
```

Then commit your clean state:

```bash
git add .
git commit -m "snapshot: before repo cleanup"
```

---

## Step 0 — Fix What Codex Already Did

### Check the README Codex Created

Open `README.md` and verify:
- It does not contain placeholder text
- It accurately describes your project
- It does not misrepresent what is built vs. planned

If it is wrong or generic → rewrite it yourself using the template in Step 5.

### Check the .gitignore Codex Modified

Open `.gitignore` and verify it contains only ignore rules, one per line.

Example of correct format:
```
build/
install/
log/
.venv/
__pycache__/
*.pyc
```

If it contains prose, shell text, or anything that is not an ignore rule → fix it manually.

---

## Step 1 — Rename Phase Folders Yourself (Do Not Use Codex)

Do this manually in your terminal. Codex should not touch folder names.

```bash
cd Robot/src

mv Phase0-Plan     Phase00-Plan
mv Phase1-Arm      Phase01-Arm
mv Phase2-Trajectory Phase02-Trajectory
mv Phase3-Optimize Phase03-Optimize
mv Phase4-Learning Phase04-Learning
mv Phase5-Vision   Phase05-Vision
mv Phase6-Autonomy Phase06-Autonomy
mv Phase7-Optimization Phase07-Optimization
mv Phase8-Deployment Phase08-Deployment
mv Phase9-Specialization Phase09-Specialization
mv "Phase11+-Endgame" Phase11-Endgame
```

> Phase10 and Phase11 stay as-is — they already sort correctly with zero-padded single digits.

Commit immediately after:

```bash
git add .
git commit -m "refactor: zero-pad phase folder names for correct sorting"
```

---

## Step 2 — Fix package.xml Metadata (Do This Yourself)

Codex flagged placeholder values. Open every `package.xml` and replace:

| Placeholder | Replace With |
|---|---|
| `0.0.0` | Your actual version e.g. `0.1.0` |
| `TODO: Package description` | One sentence describing the package |
| `devuser@example.com` | Your real email |
| `TODO` in maintainer/author | Your real name |

This takes 5 minutes and makes an immediate difference to anyone who opens the file.

---

## Step 3 — Trim requirements.txt (Do This Yourself)

340 lines reads as an environment dump, not a deliberate dependency list.

Go through it and keep only packages your code actually imports. Everything else delete.

If you are unsure what is needed, add a comment at the top:

```
# ROS dependencies are managed via rosdep
# Python dependencies for robot_control package only
```

---

## Step 4 — Tell Codex to Clean Up File Names and Move Files

Send this exact message to Codex:

```
Do not make any changes yet.

Scan only .md and .txt files in the Robot/ directory (ignore src/, build/, install/, log/, .git/, .venv/, .devcontainer/).

Produce a PLAN ONLY listing:
1. Files to rename → lowercase-hyphen format (e.g. "New stuff.md" → "new-stuff.md")
2. Files to move out of Other/ → suggest destination or archive/unsorted/
3. Files to move out of Mini_Project/ → suggest destination or experiments/mini-project/
4. Folders to create: docs/, archive/unsorted/, experiments/

Do not create, edit, move, or rename anything until I reply "Approved."
```

Review the plan line by line. Reject anything that:
- Touches a file you do not recognize
- Moves something to a destination that does not make sense
- Renames something you want to keep as-is

Then reply "Approved" only for the items you accept.

---

## Step 5 — Write the Root README Yourself

Do not let Codex write this. It will be generic. Write it yourself.

Use this structure:

```markdown
# 6-DOF Robotic Arm

One sentence: what this is and what it does.

## Overview

What problem does this solve?
What is the end goal of the project?
What makes this project interesting or challenging?

## System Architecture

[Add a diagram here — even a hand-drawn photo is better than nothing]

Brief description of the main components and how they connect.

## What Works Right Now

Be honest. List what is actually functional today.
Do not list planned features here.

## Project Structure

| Folder | Contents |
|---|---|
| src/ | ROS2 packages and robot control code |
| Phase00-Plan/ | Initial planning and requirements |
| Phase01-Arm/ | Arm kinematics and hardware setup |
| docs/ | Polished documentation |
| experiments/ | Prototypes and test work |
| archive/ | Old content, kept for reference |

## Setup

Link to docs/setup/ or list steps here.

## Team

| Name | Role |
|---|---|
| ... | ... |

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| Phase00 | Planning | Complete |
| Phase01 | Arm Hardware | In Progress |
| ... | ... | ... |
```

---

## Step 6 — Make Your Docs Evidence-First

Codex flagged that phrases like "Provable Safety" and "Resume-Grade Artifacts" in your `Overall_Project/README.md` are claims without evidence.

For each claim, ask: *can I point to something that proves this?*

- Diagram → add it
- Test result → screenshot it
- Demo → link a video
- Plot → export it from your code and embed it

If you cannot back it up yet → remove the claim and replace it with what you are working toward.

---

## Step 7 — Fix Commit Messages Going Forward

Your history currently shows mostly `End of day save`. That is normal while building but looks unprofessional under review.

Use this format from now on:

```
type: short description

Examples:
docs: add root README
feat: scaffold robot_control package
fix: correct DH parameter table in Phase01
refactor: rename phase folders for sorting
```

You cannot fix old commits easily — just start now.

---

## Step 8 — Commit Everything

```bash
git add .
git commit -m "refactor: full repo cleanup and documentation polish"
```

---

## Step 9 — Sanity Check

Before pushing, ask:

- Can a new team member find setup docs in under 1 minute?
- Does the README explain what is built vs. what is planned?
- Are there any folders named `Other`, `Misc`, or `New`?
- Are there any files with spaces or underscores in the name?
- Does `package.xml` have your real name and a real description?
- Is `requirements.txt` under 50 lines?

If any answer is wrong → fix it before pushing.

---

## What NOT to Delegate to Codex

| Task | Why |
|---|---|
| Rename phase folders | Too risky — do it in terminal |
| Fix package.xml | Needs your real personal info |
| Trim requirements.txt | Only you know what is actually used |
| Write the README | Generic output is worse than none |
| Fix commit history | Cannot be automated safely |

---

## Priority Order

1. `git diff HEAD` — verify what Codex already did
2. Fix phase folder names manually in terminal
3. Fix `package.xml` metadata
4. Run Codex for file renames and moves (plan → approve → execute)
5. Write the README yourself
6. Trim `requirements.txt`
7. Final commit and push