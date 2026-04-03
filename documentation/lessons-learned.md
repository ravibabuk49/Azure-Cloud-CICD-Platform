# Lessons Learned

## Day 1

- **ADRs are purely technical** — context, decision, technical reasons,
  and consequences only. No mention of learning goals or personal motivations.
- **subprocess.run() flag parsing** — passing "version --client" as a single
  string fails. Fix requires two changes together:
  1. Under check_tool function In run_command() change `run_command([tool, version_flag])` 
     to `run_command([tool] + version_flag.split())`
  2. Change the kubectl call to use `"version --client --output=yaml"` 
     so the output is parseable
  Both changes together fixed the issue — either alone did not work.
- **ADO Scrum terminology** — PBIs not User Stories, Effort not Story Points,
  columns are New → Approved → Committed → Done.
- **heredoc single quotes** — << 'EOF' prevents variable expansion.
  Use << EOF when you need $(date) or other variables to evaluate.
