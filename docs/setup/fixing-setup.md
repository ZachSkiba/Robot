# Dev Container + ROS 2 Python Environment Fix Plan

---

## 0. Correct Mental Model (Read First)

Before any fix is applied, two things must be understood accurately.

**First: this is a reconstructible system, not a maintainable one.**

ROS + colcon + Python cannot be reliably held in a "correct persistent state." Runtime environment mutation is not a bug in ROS — it is the default operating model. `setup.bash` chains, `AMENT_PREFIX_PATH` appends on every source, `ros2 launch` spawns new shells, VSCode tasks inject environment overrides, `colcon test` re-evaluates subprocess contexts. Attempting to "maintain" correct state across all of these will fail. The correct invariant is:

> The environment is not maintained. It is reconstructed from Dockerfile + source code.

Rebuild is the only mechanism that produces a valid runtime state.

**Second: this document enforces conventions and partial guardrails, not hard mechanical guarantees.**

No shell variable, no `ENV` block, and no sourcing script can prevent a developer from manually running `source /opt/ros/humble/setup.bash` in a subprocess, or prevent VSCode from injecting `PYTHONPATH` overrides into a task shell. Every rule in this document is a convention with partial enforcement. The goal is to close the common paths to drift, not to assert that drift is impossible.

**The deployment model this document targets is:**

> Immutable container + single controlled entrypoint. All environment setup is centralized through one canonical script. No ad-hoc runtime sourcing. No overlay chaining outside the controlled chain. Rebuild is the only change mechanism.

This is one of two valid ROS deployment models. The other — mutable overlay workflow with dynamic colcon layering — is the ROS default but is incompatible with reproducibility requirements. This document does not support the mutable overlay model. Pick one and commit.

---

## 1. Current Failure Mode Summary

The environment currently has **3 competing Python states**:

- `/usr/bin/python3` — system + ROS base
- `~/.local` — user-site packages (pip contamination)
- `/workspace/Robot/.venv` — inactive but still introduces ambiguity

This causes:

- Inconsistent imports between terminals and tasks
- ROS vs NumPy ABI mismatch risk
- Non-reproducible builds across container rebuilds
- Unpredictable behavior depending on activation order

---

## 2. Target Architecture

### System Model

This system follows a **rebuild-deterministic container model**:

> Correctness is defined only by the reproducible build output of the Docker image + source code.

Runtime shells, interactive sessions, and subprocess environments are considered **non-authoritative** and may diverge without violating system correctness.

The only valid correction mechanism is:

- modify Dockerfile / apt package list / source
- rebuild container
- re-run validation suite

No runtime changes are considered persistent.

---

### Python Execution Model

Only `/usr/bin/python3` is used as the base interpreter.

However:
- interpreter identity does NOT define environment correctness
- import resolution depends on build-time dependency graph, not runtime state

Runtime Python state is treated as **ephemeral execution context**, not configuration state.

---

### Runtime Truth: `sys.path`

The ground truth of this system at runtime is a single thing:

> **The resolved `sys.path` at process startup, plus the binary linkage state of loaded `.so` extensions.**

Everything else — `apt`, colcon, `PYTHONPATH`, overlays — is a *construction mechanism* that produces this final state. Authority is not layered. It is compositional with deterministic precedence rules.

### Construction Layers and Precedence

`sys.path` at runtime is constructed from these inputs, in this order of precedence (higher = wins on conflict):

| Precedence | Input | Source | Controlled By |
|-----------|-------|--------|---------------|
| 1 (highest) | `PYTHONPATH` env var entries | set by `setup.bash` sourcing | `runtime-env.sh` |
| 2 | colcon overlay site-packages | `install/setup.bash` | colcon build output |
| 3 | apt site-packages | `/usr/lib/python3/dist-packages` | Dockerfile apt installs |
| 4 (lowest) | stdlib | Python installation | immutable |

**The correctness invariant is:** the final `sys.path` must be deterministic, reproducible, and contain no entries from user-site or pip-managed locations. The construction mechanism that produces it is secondary.

`apt` defines base packages. The colcon overlay mutates `PYTHONPATH` and `AMENT_PREFIX_PATH` on top of the apt state. Runtime truth is the deterministic composition of both, via the controlled entrypoint. Neither layer is "the authority" — the entrypoint-controlled composition is.

This has a direct consequence: a valid `apt` state with a stale colcon overlay produces a broken `sys.path`. A valid colcon overlay built against a different `apt` state produces ABI failures. Both inputs must be consistent and both must be reconstructed together.

**Dependency source rules per class:**

- ROS packages → `apt` only
- ALL Python runtime packages (ROS + non-ROS numeric stack included) → `apt` only via Ubuntu / ROS distribution
- ROS executable environment (node entrypoints, `PYTHONPATH` overlay) → colcon build output only, rebuilt from source on every environment change
- No entry in the final `sys.path` that is reachable by the ROS runtime interpreter may originate from user-site or pip-managed locations

**Scope of the `sys.path` origin invariant:** this rule applies to runtime execution paths — packages imported by ROS nodes during execution. Developer tooling installed via pip at build time (linters, formatters) physically shares the same interpreter binary but is not imported during ROS node execution. Those packages are outside the scope of this invariant. The invariant is violated only if a pip-managed package can be imported by a running ROS node.

---

### Environment Principle

> The system is not kept correct. It is repeatedly reconstructed into correctness.

There is no attempt to preserve environment state across sessions.

---

## 3. ABI Correctness and Reproducibility (Strict Definitions)

These are two separate concerns. Conflating them is a source of confusion.

### ABI Correctness

In a ROS 2 + Python system, ABI correctness is not a simple binary. It encompasses four distinct compatibility layers, all of which must hold simultaneously:

1. **Compiled extension compatibility** — Python extension modules (`.so` files) must be compatible with the running Python interpreter version
2. **Python C-API compatibility** — extensions compiled against a specific CPython version may not load under a different version
3. **NumPy binary compatibility** — extensions compiled against a specific NumPy C-API version (e.g. `cv_bridge`) will segfault or produce silent data corruption if the runtime NumPy version changes the underlying C struct layout
4. **ROS build-time linkage constraints** — ROS Python bindings are linked against specific versions of ROS C++ libraries at build time; those library versions must be present and unmodified at runtime

ABI failure can manifest as: import error, segfault, buffer pointer mismatch, silent data corruption, or incorrect node behavior. Not all ABI failures produce obvious errors. Silent corruption is worse than a clean crash.

**ABI validation checks:**

```bash
python3 -c "import rclpy"
python3 -c "from cv_bridge import CvBridge"
ros2 run <package> <node>
```

ABI is valid only if ALL of the following succeed after a clean build:

- `rclpy` imports successfully
- `cv_bridge` imports successfully
- at least one ROS node executes successfully via `ros2 run`

ABI is invalid if ANY of the following occur after a clean build:

- import failure for ROS Python bindings
- node execution failure
- runtime crash in previously validated nodes

### ABI Death Zone: NumPy

`cv_bridge` is compiled against the system NumPy C-API. NumPy C-API compatibility is a direct ABI constraint (layer 3 above) — not merely a reproducibility preference. If the runtime NumPy version changes the underlying C struct layout, the result is a segfault or buffer pointer mismatch at runtime — not a clean import error. This failure is silent until it occurs in live execution.

**Hard rule:** `numpy`, `scipy`, `setuptools`, and `protobuf` are ABI-constrained dependencies of ROS Python bindings. They must come from `apt` only. They must never be pip-installed or pip-upgraded. Any version change requires re-running the full validation suite, specifically Test #6, because the failure mode is silent data corruption, not a clean import error.

Validation Test #6 is the most critical guardrail in this document. A system that passes all other tests but fails Test #6 is broken.

Additionally: ROS 2 Humble is sensitive to `setuptools` version. If `setuptools` exceeds approximately `58.2.0`, `colcon` may throw `SetuptoolsDeprecationWarning` or fail to install package data. `setuptools` must come from `apt` and must never be pip-upgraded.

---

### Reproducibility

Reproducibility refers to:

- identical dependency graph across rebuilds
- identical package resolution from `apt` sources
- identical build output behavior after clean rebuild

Reproducibility is separate from ABI correctness. A system can have ABI correctness while not being reproducible (e.g. if apt sources drift between builds). Both must be maintained.

---

## 4. Python Dependency Policy

`requirements.txt` is **not used for system composition**.

It is permitted only for:

- developer tooling scripts (optional)
- non-runtime utilities (linting, formatting tools)
- CI helper scripts

It **must not** be used for:

- ROS packages
- numeric libraries (`numpy`, `scipy`, etc.)
- runtime application dependencies

The Dockerfile must not contain:

```dockerfile
# FORBIDDEN
RUN python3 -m pip install -r requirements.txt
```

All runtime Python dependencies are installed via `apt`. The `apt` graph is the single dependency authority.

---

## 5. Dependency Management Rules

### pip: Scope and Reality

`pip` cannot be fully eliminated from a ROS + Python ecosystem. Some ROS build tools invoke pip indirectly. Some colcon plugins introduce pip-like behavior depending on workspace configuration. Some ROS packages assume pip availability for optional components.

The correct framing is not "pip is eliminated." The correct framing is a scoped enforcement invariant across two distinct execution domains:

**ROS runtime execution domain** (packages imported by running ROS nodes):

> No Python package resolution in the ROS runtime execution domain may originate from user-site or pip-managed site-packages.

This is a `sys.path` origin constraint for runtime code paths. If a pip-managed package can be imported by a running ROS node — regardless of how pip was invoked — that is a system violation.

**Developer tooling domain** (linters, formatters, CI helpers):

> pip-installed developer tools (e.g. `flake8`, `black`) are permitted. They are installed at Docker build time, as root, before any `USER` directive. They physically share the interpreter binary but are never imported during ROS node execution. They are exempt from the `sys.path` origin invariant.

These two domains are logically separate even though they share one interpreter binary. The invariant applies to what ROS nodes can import at runtime, not to what exists on the filesystem.

Detection rule for the runtime domain: Test B1 checks that no entry in `sys.path` references `~/.local` or user-site paths. This catches user-site contamination. It does not flag Dockerfile-installed pip tooling installed to system site-packages as root, which is correct behavior.

### pip Usage Rule

`pip` as a direct authority is permitted **only** during Docker image build for developer tooling — not for runtime environment composition.

- `RUN pip install ...` for linting/tooling in Dockerfile BEFORE `USER` → conditionally allowed
- `pip install ...` for runtime dependencies → forbidden regardless of context
- `pip install ...` in running container → forbidden
- `pip install ...` in `postCreateCommand` → forbidden
- `pip install ...` in entrypoint or runtime scripts → forbidden
- transitive `pip` invocation by build tooling → accepted but must not introduce packages into `sys.path`

### Forbidden States

The system must never contain:

- `.venv` environments
- `~/.local` pip installations
- pip-installed ROS packages
- pip-installed numeric stack packages (`numpy`, `scipy`, `setuptools`, `protobuf`)
- unpinned `pip` tooling packages
- `requirements.txt` used as a runtime dependency source

### Dependency Authority Rule

- ROS packages → `apt` only
- system Python → Ubuntu / ROS distribution only
- ALL Python runtime packages → `apt` only
- developer tooling (optional) → Docker build-time `pip` only, before any `USER` directive

---

## 6. Immediate Cleanup

Run inside the container:

```bash
# Remove local user-site contamination
rm -rf ~/.local/lib/python*
rm -rf ~/.local/bin/pip*
rm -rf ~/.cache/pip

# Remove repo venv
rm -rf /workspace/Robot/.venv
```

Then verify:

```bash
which python3
python3 -c "import site; print(site.getsitepackages())"
```

**Expected:** no reference to `/home/.../.local`

---

## 7. Fix `devcontainer.json`

Remove any of the following:

- `.venv` creation logic
- `pip` installs in `postCreateCommand`
- Any `PATH` overrides pointing to `.venv/bin`
- Any `settings` that inject `PYTHONPATH` overrides

**VSCode environment injection is a real contamination vector.** VSCode tasks, launch configurations, and the Python extension can inject `PYTHONPATH`, `PATH`, and other environment variables into shell contexts independently of `.bashrc`. These override the container environment silently. Audit `tasks.json`, `launch.json`, and `settings.json` for any `env` blocks that modify Python-relevant variables.

Enforce:

```json
"postCreateCommand": "bash /workspace/Robot/.devcontainer/setup.sh"
```

`setup.sh` is a one-time container setup script. Its job is idempotent system checks and optional `rosdep` update. It does **not** source the ROS environment — that is `runtime-env.sh`'s job. Mixing setup actions with environment construction causes silent drift.

Create `/workspace/Robot/.devcontainer/setup.sh`:

```bash
#!/usr/bin/env bash
set -e

# One-time container setup — NOT environment definition.
# This script mutates the container once after creation.
# Do not source ROS setup files here. Do not call runtime-env.sh here.
# Environment construction is handled exclusively by runtime-env.sh.

rosdep update

echo "Container setup complete."
```

To prevent interactive terminals from bypassing the entrypoint environment, add this to `devcontainer.json`:

```json
"terminal.integrated.profiles.linux": {
  "bash": {
    "path": "/bin/bash",
    "args": ["--init-file", "/workspace/Robot/.devcontainer/runtime-env.sh"]
  }
}
```

This forces every VSCode-integrated terminal to source the ROS environment through `runtime-env.sh` (see Section 12 for the split between `runtime-env.sh` and `entrypoint.sh`). Without this, developers opening a terminal will get `command not found` for `ros2` and may begin manually sourcing `setup.bash`, creating the exact contamination this model is designed to prevent.

Also set the Python interpreter explicitly in `.vscode/settings.json` to prevent the Python extension from auto-selecting an interpreter:

```json
"python.defaultInterpreterPath": "/usr/bin/python3",
"python.analysis.extraPaths": [
    "/opt/ros/humble/lib/python3.10/site-packages",
    "/opt/ros/humble/local/lib/python3.10/dist-packages",
    "/workspace/Robot/install/local/lib/python3.10/dist-packages"
]
```

All three paths are required. `/opt/ros/humble/lib/python3.10/site-packages` is where ROS Python packages are installed by `apt`. `/opt/ros/humble/local/lib/python3.10/dist-packages` is the secondary ROS dist-packages location that the original setting omitted — missing it produces false "clean editor" import state where the editor reports missing symbols that actually exist at runtime. `/workspace/Robot/install/local/lib/python3.10/dist-packages` is the workspace colcon overlay path, required for the editor to resolve packages built from source.

---

## 8. Build Artifact Policy

`build/`, `install/`, and `log/` live inside the container filesystem. No Docker volumes for these paths. When the container is destroyed, they are destroyed.

This is non-negotiable for Rev 1.

The correct hash-invalidation approach for volume caching requires computing a deterministic hash across the full dependency input set: apt package list, Dockerfile, `rosdep` dependencies, and workspace source tree. A hasher that misses a single header file change will serve a stale ABI silently. Building and maintaining that correctly is a substantial DevOps project. The reproducibility risk of an incorrect implementation outweighs the build time savings.

If build times become a critical blocker to development velocity, revisit volume caching as a dedicated project with proper hash-invalidation infrastructure. Until then: feel the 4-minute rebuild when a dependency changes. That pain enforces disciplined dependency management.

Named volumes for `build/` and `install/` are also the primary cause of "it works on my machine" failures in dev containers. Even wiping directory contents inside a running container does not reliably clear the underlying Docker volume.

Any persistence of `build/` or `install/` that is not under the container filesystem invalidates reproducibility guarantees.

### Build Invalidation Rule

A full wipe of `install/` is required when any of the following change:

- Dockerfile or apt package list
- `package.xml` dependency declarations
- source tree structure (package renames, directory moves)
- interpreter or ABI state

A full wipe is **not** required for inner-loop logic changes — editing `.py` or `.cpp` files where the dependency graph and source structure are unchanged. `--symlink-install` handles Python file changes without a rebuild. For C++ changes, `colcon build` alone is sufficient.

When a full wipe is required:

```bash
rm -rf /workspace/Robot/build /workspace/Robot/install /workspace/Robot/log
colcon build --symlink-install
```

`--cmake-clean-cache` does not remove Python entrypoints or `install/` artifacts. Only a full directory wipe guarantees a clean build.

**Note on `--symlink-install` and renamed paths:** `--symlink-install` is useful during development — Python file changes take effect without a rebuild. However, symlinks are bound to the source path at the time `colcon build` ran. If any source folder is renamed or moved, `install/` will contain broken symlinks. The Build Invalidation Rule above handles this: when source structure changes, wipe and rebuild. Do not attempt to repair broken symlinks in place.

**Note on ROS Python entrypoints:** ROS Python packages installed via `ament_python` generate shebang-bound scripts and build-time resolved Python paths. These are bound to the interpreter state and overlay state at the time `colcon build` ran. If the interpreter, apt packages, or overlay state changes, `ros2 run` can silently point to stale or broken paths with no obvious error. `install/` is not portable across environment changes.

---

## 9. Fix Dockerfile

All pip hardening environment variables must be set before any pip invocation, and pip must run as root before any `USER` directive:

```dockerfile
# All four are required — not optional
ENV PYTHONNOUSERSITE=1 \
    PIP_USER=0 \
    PIP_NO_USER_CONFIG=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# pip install is permitted here ONLY for developer tooling — not runtime dependencies
# Runtime Python dependencies come from apt exclusively
RUN python3 -m pip install --no-cache-dir flake8 black  # example tooling only
```

Each variable closes a specific escape path:

- `PYTHONNOUSERSITE=1` — prevents `~/.local` from entering `sys.path` at interpreter startup
- `PIP_USER=0` — prevents pip from defaulting to user-install mode
- `PIP_NO_USER_CONFIG=1` — prevents `pip.conf` or `~/.config/pip/pip.conf` from overriding install target
- `PIP_DISABLE_PIP_VERSION_CHECK=1` — suppresses version-check network calls during build

These reduce accidental drift. They do not prevent a determined manual pip invocation. That is why the build-time-only rule must be enforced through code review.

---

## 10. Fix `requirements.txt`

`requirements.txt` must not contain runtime dependencies. If it currently exists for runtime use, it must be either deleted or repurposed strictly for developer tooling.

Delete all of the following categories from `requirements.txt`:

```
# DELETE — these must come from apt
rclpy
tf2-py
ament-index-python
colcon-core
launch-ros
cv-bridge

# DELETE — these are ABI-sensitive and must come from apt
numpy
scipy
setuptools
protobuf
pyyaml
transforms3d
```

Verify the correct versions are present from apt:

```bash
apt-cache show python3-numpy | grep Version
apt-cache show python3-scipy | grep Version
dpkg -l python3-setuptools | grep ii
```

If a package is not available via `apt`, the decision to pip-install it is an architecture decision that requires explicit team review and full ABI validation — not a default.

---

## 11. Fix ROS Installation

Ensure the Dockerfile contains:

```dockerfile
RUN apt-get install -y \
  ros-humble-desktop \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-vcstool \
  python3-numpy \
  python3-scipy \
  python3-yaml \
  python3-setuptools
```

Then initialise rosdep:

```dockerfile
RUN rosdep init 2>&1 || echo "WARNING: rosdep init failed — check output above" && rosdep update
```

Do not use `|| true` silently. A broken rosdep state is invisible if failures are swallowed.

---

## 12. Fix Environment Sourcing

This section enforces the **immutable container + single entrypoint** model. The mutable overlay model — sourcing in `.bashrc`, re-sourcing in scripts, chaining overlays interactively — is explicitly abandoned.

### The Core Problem with Runtime Sourcing

`setup.bash` appends to `AMENT_PREFIX_PATH` and `PYTHONPATH` on every invocation. Every new shell evaluates `.bashrc`. `ros2 launch` spawns new shell contexts. VSCode opens multiple terminals. `colcon test` spawns subprocesses. Any of these can re-source `setup.bash` and accumulate duplicate overlay entries.

**The only robust solution is to centralize all runtime sourcing through a single canonical script, and eliminate ad-hoc sourcing everywhere else.**

### Overlay Cardinality Constraint

ROS 2 overlays are additive. Every `source install/setup.bash` appends to `AMENT_PREFIX_PATH`, `PYTHONPATH`, and `LD_LIBRARY_PATH`. Multiple overlays are not peers — they are ordered, and ordering determines import resolution when package names conflict.

This is a real ROS failure class, not a theoretical one. If more than one overlay is active at runtime:

- Python import resolution becomes order-dependent
- two nodes can import different versions of the same package depending on which overlay sourced first
- the failure is silent unless the packages have incompatible APIs

**Invariant:** exactly one overlay chain is permitted to be active at runtime. That chain is:

1. `/opt/ros/humble/setup.bash` (base ROS layer)
2. `/workspace/Robot/install/setup.bash` (workspace overlay, if built)

No other overlays. No additional `source` calls. No nested overlay sourcing. If a third overlay is detected in `AMENT_PREFIX_PATH`, the environment is contaminated and must be reconstructed.

### Script Architecture: One Canonical Environment Script

There is exactly **one canonical environment construction script**. Everything else calls it. Logic must not be duplicated across scripts — duplication means the scripts can silently diverge.

The three environment consumers in this system are:

1. Container process launch (`entrypoint.sh`)
2. VSCode integrated terminals (`--init-file`)
3. CI runners (explicit source)

All three must call the same canonical script. If the canonical script changes, all three consumers update automatically because they reference it — not because someone remembered to update each one.

**`/workspace/Robot/.devcontainer/runtime-env.sh`** — the canonical environment construction script. This is the single source of truth for ROS environment setup. It is designed to be *sourced*, not executed:

```bash
#!/usr/bin/env bash

# CANONICAL ENVIRONMENT SCRIPT — single source of truth.
# This script is sourced, not executed.
# All environment consumers (entrypoint.sh, VSCode terminals, CI) source this file.
# ROS environment logic lives here and nowhere else.
# Do not add exec "$@" here — this is not an entrypoint.

source /opt/ros/humble/setup.bash

if [ -f /workspace/Robot/install/setup.bash ]; then
  source /workspace/Robot/install/setup.bash
fi
```

**`/workspace/Robot/.devcontainer/entrypoint.sh`** — the container process entrypoint. This script is *executed*, not sourced. It has no environment logic of its own — it calls the canonical script and hands off:

```bash
#!/usr/bin/env bash
set -e

# Container process entrypoint.
# Contains no environment logic — sources runtime-env.sh for that.
# Do not duplicate ROS sourcing here.

source /workspace/Robot/.devcontainer/runtime-env.sh

exec "$@"
```

**Rule:** if you find yourself writing `source /opt/ros/humble/setup.bash` anywhere other than `runtime-env.sh`, stop. That logic belongs in `runtime-env.sh` only. Every other script calls `runtime-env.sh`.

If `.bashrc` currently contains `source /opt/ros/humble/setup.bash`, delete that line. The terminal wrapper in `devcontainer.json` (Section 7) handles environment construction for interactive shells via `runtime-env.sh`. `.bashrc` must not contain any ROS sourcing.

### VSCode Task and Launch Configuration

Every VSCode task that needs the ROS environment must explicitly source `runtime-env.sh` as the first step. Audit `tasks.json` for any `"env"` blocks injecting `PYTHONPATH`, `ROS_PACKAGE_PATH`, or `AMENT_PREFIX_PATH`. These silently override the container environment. Remove them.

---

## 12.1 Execution Correctness Scope

Correctness guarantees apply to:

- processes launched via `entrypoint.sh`
- CI pipeline execution
- explicitly wrapped launch scripts that invoke the entrypoint
- interactive shells routed through `runtime-env.sh` via the terminal wrapper defined in `devcontainer.json`

### Ad-hoc Shells and `docker exec`

`docker exec` sessions, manual shells, and CI repro attempts are real execution contexts. ROS debugging always happens here. Calling them "out of scope" and stopping there is operationally useless.

The correct guidance for these contexts:

**For `docker exec` sessions:**

```bash
docker exec -it <container> bash --init-file /workspace/Robot/.devcontainer/runtime-env.sh
```

This gives a fully configured ROS shell without modifying `.bashrc` or re-sourcing outside the canonical script.

**For manual shell entry inside the container:**

```bash
source /workspace/Robot/.devcontainer/runtime-env.sh
```

Source the canonical script explicitly. Do not source `/opt/ros/humble/setup.bash` directly — that bypasses the overlay chain and breaks the cardinality invariant.

**For CI repro:**

CI runners must source `runtime-env.sh` explicitly before any `ros2` or `colcon` invocation. The CI pipeline must not assume the environment is pre-configured.

These contexts are not covered by reproducibility guarantees because they are ad-hoc by nature. But they are not correctness hazards if they source the canonical script. The hazard is sourcing anything else.

---

## 12.2 Runtime Drift Model (Explicit Risk Boundary)

### Known Behavior of ROS + Python + VSCode

The following forms of drift are expected and cannot be fully prevented:

- re-sourcing of ROS setup files in child shells
- environment divergence in `ros2 launch` subprocess trees
- VSCode task environment injection
- Python import path variation across execution contexts
- colcon-generated entrypoints bound to build-time interpreter state

### System Assumption

> Runtime environment is not stable by design.

Therefore:

- runtime divergence is not treated as failure
- only build output divergence is considered a failure

### Failure Definition

A system failure is defined only by reproducibility violation.

The system is in a **FAILED** state if ANY of the following occur after a clean rebuild:

- `rclpy` import fails
- `cv_bridge` import fails
- `colcon build` fails in a clean workspace
- `ros2 run` fails for a previously validated node
- dependency graph changes between rebuilds without intentional version change

Non-failure conditions (expected behavior):

- environment differences between shells
- differences between interactive and non-interactive terminals
- variations in VSCode task environments
- differences caused by manual sourcing outside the entrypoint or terminal wrapper

These are classified as runtime contamination and not build system faults.

---

## 13. Fix `software-setup.md`

The audit found a direct contradiction:

- **Line 141** instructs developers to create a venv and install packages manually.
- **Line 449** says never run manual pip install for team-wide features.

Required changes:

- Remove venv creation instructions at line 141. Replace with: **all setup occurs via container rebuild — no local setup path exists.**
- Consolidate into one unambiguous rule at a clearly visible location.
- Add explicit prohibition: no developer runs `pip install` after container creation. If a dependency is missing, add it to the apt package list in the Dockerfile and rebuild.

The bar: if a developer can follow the documentation start to finish and end up with a venv or a `~/.local` install, the documentation is not fixed.

---

## 14. Validation Tests

Run after every container rebuild from a clean state.

A clean state means:

- no existing `build/`
- no existing `install/`
- no cached colcon artifacts
- no persisted pip or user-site state

The tests below are organized into **four orthogonal categories**. Each category validates a different property. Each test within a category is atomic — it checks exactly one thing. Passing all tests in one category does not imply anything about another category.

| Category | What it validates |
|----------|-------------------|
| A — Dependency Graph Auditing | the correct packages are installed from the correct sources |
| B — `sys.path` Origin Enforcement | no entry in the resolved import path came from user-site or pip |
| C — Reproducibility Validation | the environment is identical across rebuilds |
| D — Runtime Correctness | the system actually executes correctly at the ABI boundary |

---

### Category A — Dependency Graph Auditing

These tests verify that packages are installed from the correct sources. They check installation facts, not runtime behavior.

**Test A1 — Single interpreter check**

```bash
which python3
```

Must output: `/usr/bin/python3`. Any other output means a non-system interpreter is on `PATH`.

**Test A2 — pip hardening environment check**

```bash
echo $PYTHONNOUSERSITE    # must be 1
echo $PIP_USER            # must be 0
echo $PIP_NO_USER_CONFIG  # must be 1
```

These prevent user-site contamination at interpreter startup. If any value is wrong, the Dockerfile `ENV` block is missing or overridden.

**Test A3 — NumPy installation source check**

```bash
python3 -c "import numpy; print(numpy.__file__)"
```

Must be under `/usr/lib/python3/dist-packages`. If it resolves to any other location, numpy came from the wrong source.

---

### Category B — `sys.path` Origin Enforcement

These tests verify the ground truth invariant: no entry in the resolved `sys.path` originated from user-site or pip-managed locations. This is one invariant expressed three ways to catch different failure modes.

**Test B1 — `sys.path` user-site exclusion (primary enforcement check)**

```bash
python3 -c "
import sys
violations = [p for p in sys.path if '/home/' in p or '.local' in p]
assert not violations, f'FAIL: user-site in sys.path: {violations}'
print('PASS')
"
```

This is the canonical enforcement check for the `sys.path` origin invariant. If this fails, the system is in a forbidden state regardless of other test results.

**Test B2 — Overlay accumulation check**

```bash
# Run in a fresh shell, then again in a second fresh shell
echo $AMENT_PREFIX_PATH | tr ':' '\n' | wc -l
```

Count must be identical across fresh shells. If it grows, overlay accumulation is occurring and the cardinality invariant is violated.

**Test B3 — Overlay cardinality check**

```bash
echo $AMENT_PREFIX_PATH | tr ':' '\n'
```

Must contain exactly two entries: `/opt/ros/humble` and `/workspace/Robot/install` (if built). Any additional entry is a foreign overlay and must be investigated.

---

### Category C — Reproducibility Validation

These tests verify the environment is identical across rebuilds. A system that passes A and B but fails C will drift over time.

**Test C1 — apt manifest consistency check**

```bash
dpkg-query -W > /tmp/dpkg_current.txt
diff /workspace/Robot/expected/dpkg.lock /tmp/dpkg_current.txt
```

Checks the `apt` construction layer against a known-good baseline. If differences exist, rebuild is required.

To generate the initial lock file after a validated clean build:

```bash
dpkg-query -W > /workspace/Robot/expected/dpkg.lock
```

**Test C2 — ROS package graph check**

```bash
ros2 pkg list > /tmp/ros_pkgs.txt
diff /workspace/Robot/expected/ros_pkgs.txt /tmp/ros_pkgs.txt
```

If differences exist, the environment is not reproducible.

---

### Category D — Runtime Correctness

These tests verify the system executes correctly at the ABI boundary. Passing A–C does not guarantee D. ABI failures can exist in a clean, reproducible environment.

**Test D1 — ROS import test**

```bash
python3 -c "import rclpy; print('rclpy OK')"
```

Verifies compiled extension loading. Failure here is an ABI layer 1 or 2 failure (see Section 3).

**Test D2 — cv_bridge C-API boundary test (CRITICAL)**

```bash
python3 -c "
from cv_bridge import CvBridge
import numpy as np
import cv2
bridge = CvBridge()
img = np.zeros((480, 640, 3), dtype=np.uint8)
msg = bridge.cv2_to_imgmsg(img, encoding='bgr8')
result = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
assert result.shape == img.shape, 'FAIL: shape mismatch'
print('cv_bridge ABI OK')
"
```

This exercises the actual NumPy C-API boundary (ABI layer 3). A clean import of `cv_bridge` is not sufficient — NumPy ABI mismatch manifests as silent data corruption or segfault, not an import error. This is the only test that catches it.

**If D2 fails after any package change, the environment is broken regardless of what A, B, and C report.**

---

## 15. Hard Rules

- The ground truth of this system is a deterministic, reproducible `sys.path` + binary linkage state; everything else is a construction mechanism that produces it
- No entry in `sys.path` reachable by the ROS runtime execution domain may originate from user-site or pip-managed locations; pip-installed developer tooling (linters, formatters) installed as root at build time is exempt from this invariant
- No `pip install` as a direct authority after container creation — any runtime dependency change requires a Docker image rebuild
- `pip` permitted as a direct tool only for developer tooling in Dockerfile `RUN` layers, as root, before any `USER` directive
- All four pip hardening env vars must be set: `PYTHONNOUSERSITE=1`, `PIP_USER=0`, `PIP_NO_USER_CONFIG=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`
- All Python runtime packages installed via `apt` only — no `requirements.txt` for runtime deps
- `numpy`, `scipy`, `setuptools`, `protobuf` are ABI-constrained dependencies; they must come from `apt` only and must never be pip-installed or pip-upgraded
- `setuptools` must not exceed the apt-provided version; colcon is sensitive to `setuptools` beyond ~58.2.0
- No `.venv` anywhere
- Exactly one overlay chain active at runtime: base ROS layer + workspace overlay only; any third entry in `AMENT_PREFIX_PATH` is contamination
- All sourcing is centralized through `runtime-env.sh`; ad-hoc sourcing is eliminated; `entrypoint.sh` calls it, VSCode terminals call it, CI calls it, `docker exec` sessions source it; nothing else contains ROS sourcing logic
- `build/`, `install/`, `log/` live inside the container filesystem only — no named Docker volumes for these paths
- Full wipe of `install/` required on: Dockerfile changes, apt package changes, `package.xml` dependency changes, source tree restructuring, interpreter or ABI changes; not required for inner-loop logic edits
- All ROS Python packages rebuilt after any environment change
- VSCode `tasks.json` and `launch.json` audited for `env` blocks injecting Python-relevant variables
- `.vscode/settings.json` must explicitly set `python.defaultInterpreterPath` to `/usr/bin/python3` and include all three `extraPaths` entries
- Test D2 (`cv_bridge` C-API round-trip) must pass after every rebuild — import success alone is not sufficient; passing Categories A–C does not guarantee runtime correctness

---

## 16. Expected Final State

- One Python interpreter: `/usr/bin/python3`
- Runtime truth is a deterministic `sys.path` constructed from: apt site-packages (base) + colcon overlay (workspace) + `PYTHONPATH` from `runtime-env.sh` — no other inputs reachable by the ROS runtime execution domain
- No entry in `sys.path` reachable by ROS nodes originates from user-site or pip-managed locations; pip-installed dev tooling at system site-packages is explicitly exempt
- ROS Humble from `apt` only; all Python runtime packages from `apt` only
- Exactly one overlay chain active: base ROS layer + workspace colcon overlay only
- All sourcing centralized through `runtime-env.sh`; no ad-hoc sourcing permitted; `entrypoint.sh` calls it; VSCode terminals call it; CI calls it; `docker exec` sessions source it explicitly
- `build/`, `install/`, `log/` ephemeral — no Docker volume persistence
- `install/` wiped on dependency graph changes, source tree restructuring, and ABI changes; inner-loop logic edits do not require a wipe
- ABI validation covers all four layers: compiled extension, C-API, NumPy binary compatibility, ROS build-time linkage
- Validation suite: three atomic categories (A: installation sources, B: `sys.path` origin enforcement for runtime domain, C: reproducibility) plus one behavioral category (D: runtime ABI correctness)
- Known residual risks documented explicitly rather than hidden behind false guarantees
- The system is reconstructible from source, not maintained in state

---

> **Engineering Note**
>
> ROS is a runtime environment mutation system by design. Every `source setup.bash` appends to the environment. Every new shell can re-evaluate. Every subprocess can diverge. The attempt to force this into a statically correct model will always leave residual escape paths. The correct response is not to claim those paths are closed — it is to make the system reconstructible so that when drift occurs, the fix is a rebuild, not a debugging session. All rules in this document exist to make drift visible and rebuilding the default response, not to assert that drift cannot happen.
