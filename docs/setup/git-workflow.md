# Daily Robot Workflow: Open, Save, Close

This is your day-to-day checklist for working on the repository. Always pull in the morning and push at night.

## 1. Morning Routine (Opening & Getting Updates)

1. Start the engine: Open Docker Desktop and let it run.
2. Open the lab: Open VS Code → File > Open Folder → select `Robot`.
3. Jack in: Click `Reopen in Container` (bottom-right) if prompted. Wait for this terminal:

```text
devuser@docker-desktop:/workspace/Robot$
```

4. Get the latest code (CRITICAL): Pull your partner's changes:

```bash
cd Robot
git pull
```

## 2. Throughout the Day (Saving & Sharing)

- Save locally as you code (`Ctrl+S` / `Cmd+S`).
- When a feature is ready, push to GitHub:

```bash
# 1. Stage all changed files
# 2. Commit with a descriptive message
# 3. Push to GitHub
git add .
git commit -m "Added the base link to the URDF file"
git push
```

Tip: Commit small, frequent changes. Don't wait until the end of the week.

## 3. Evening Routine (Closing Down)

### Final Push

```bash
cd /workspace/Robot
git add .
git commit -m "End of day save"
git push
```

### Close Down

- Close VS Code: Click the X. The container will automatically sleep.
- Save battery/RAM: Right-click Docker Desktop → Quit.
