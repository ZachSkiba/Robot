📅 Daily Robot Workflow: Open, Save, Close

This is your day-to-day checklist for working on the repository. Always pull in the morning and push at night.

🌅 1. Morning Routine (Opening & Getting Updates)

Start the Engine: Open Docker Desktop and let it run.

Open the Lab: Open VS Code → File > Open Folder → select Robot.

Jack In: Click Reopen in Container (bottom-right) if prompted. Wait for terminal:

devuser@docker-desktop:/workspace/Robot$

Get the Latest Code (CRITICAL): Pull your partner’s changes:

git pull

💾 2. Throughout the Day (Saving & Sharing)

Save locally as you code (Ctrl+S / Cmd+S).

When a feature is ready, push to GitHub:

# 1. Stage all changed files
# 2. Commit with a descriptive message
# 3. Push to GitHub

git add .
git commit -m "Added the base link to the URDF file"
git push

Tip: Commit small, frequent changes. Don’t wait until the end of the week.

🌙 3. Evening Routine (Closing Down)

Final Push:

cd /workspace/Robot
git add .
git commit -m "End of day save"
git push

Close VS Code: Click the X. The container will automatically sleep.

Save Battery/RAM: Right-click Docker Desktop → Quit.  Cool W