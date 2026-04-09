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


## Day 2

- **Terraform plan -out flag** — always save plan with -out=tfplan then
  apply that exact plan. Prevents unexpected changes between plan and apply.
  Enterprise standard — never run terraform apply without a saved plan.

- **Azure Boards + GitHub integration** — use AB# followed by PBI ID in
  commit messages to automatically link commits to work items. PRs linked
  to PBIs move automatically to Done when merged.

- **Storage account CLI issue** — az storage account create failed with
  SubscriptionNotFound despite correct subscription being active.
  Workaround: create via portal. Root cause: likely a tenant configuration
  issue with the free tier account. Terraform state storage is supporting
  infrastructure — creating it manually via portal is acceptable.

- **Docker layer caching** — copy .csproj files first, run dotnet restore,
  then copy source code. If source changes but dependencies don't, the
  restore layer is cached — significantly faster subsequent builds.

- **Directory.Packages.props** — eShopOnWeb uses central package management.
  This file defines TargetFramework and all package versions for the entire
  solution. Must be copied into Docker build context before dotnet restore
  — otherwise restore fails with NETSDK1013 TargetFramework not recognized.
  Always check for solution-level config files before writing a Dockerfile.

- **Multi-stage Docker build** — build stage uses SDK image (850MB base)
  and produces 2.23GB intermediate layer. Final runtime image uses aspnet
  base (218MB) and is only 430MB. Multi-stage is mandatory for .NET apps
  in production — never ship the SDK in the runtime image.
  