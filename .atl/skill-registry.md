# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

See `_shared/skill-resolver.md` for the full resolution protocol.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| When creating a pull request, opening a PR, or preparing changes for review. | branch-pr | /home/compneuro/.config/opencode/skills/branch-pr/SKILL.md |
| When writing Go tests, using teatest, or adding test coverage. | go-testing | /home/compneuro/.config/opencode/skills/go-testing/SKILL.md |
| When creating a GitHub issue, reporting a bug, or requesting a feature. | issue-creation | /home/compneuro/.config/opencode/skills/issue-creation/SKILL.md |
| When user says "judgment day", "judgment-day", "review adversarial", "dual review", "doble review", "juzgar", "que lo juzguen". | judgment-day | /home/compneuro/.config/opencode/skills/judgment-day/SKILL.md |
| When user asks to create a new skill, add agent instructions, or document patterns for AI. | skill-creator | /home/compneuro/.config/opencode/skills/skill-creator/SKILL.md |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### branch-pr
- Every PR MUST link an approved issue; blank PRs without issue linkage are blocked.
- Every PR MUST have exactly one `type:*` label that matches the change intent.
- Branch names MUST match `type/description` using lowercase `a-z0-9._-` only.
- Use conventional commits only; no `Co-Authored-By` trailers.
- Run `shellcheck` on modified shell scripts before opening the PR.
- PR body MUST include linked issue, summary, changes table, test plan, and checklist.

### go-testing
- Prefer table-driven tests for pure or multi-case Go logic.
- Test Bubbletea state transitions by calling `Model.Update()` directly.
- Use `teatest.NewTestModel()` for full interactive TUI flows.
- Use golden files for stable view/output assertions.
- Use `t.TempDir()` for file-system tests and mocks/interfaces for side effects.
- Cover both success and error paths explicitly.

### issue-creation
- Issues MUST use the provided templates; blank issues are disabled.
- Search for duplicates before creating a new issue.
- New issues get `status:needs-review`; a maintainer MUST add `status:approved` before any PR.
- Questions belong in Discussions, not Issues.
- Bug reports MUST include repro steps, expected vs actual behavior, and environment details.
- Feature requests MUST describe the problem, proposed solution, and affected area.

### judgment-day
- Run two blind judges in parallel; neither judge sees the other review.
- Resolve project skills first and inject matching compact rules into both judge prompts.
- Classify warnings as `real` vs `theoretical`; only real warnings block approval.
- Fix only confirmed issues, then re-judge; do not self-review as the orchestrator.
- After two fix iterations, escalate to the user before continuing.
- If no registry exists, warn and proceed with generic review only.

### skill-creator
- Create a skill only for reusable, non-trivial patterns or workflows.
- Structure skills as `skills/{skill-name}/SKILL.md` with optional `assets/` and `references/`.
- Frontmatter MUST include `name`, `description` with Trigger, `license`, and `metadata`.
- Keep critical patterns actionable; keep examples minimal and focused.
- Use local paths in `references/`; do not use web URLs there.
- Register new skills in `AGENTS.md` after creation.

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| — | — | No project convention files detected in the project root. |

Read the convention files listed above for project-specific patterns and rules. All referenced paths have been extracted — no need to read index files to discover more.
