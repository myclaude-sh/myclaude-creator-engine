# Git Push — myclaude-sh org

GITHUB_TOKEN env var is set to l0z4n0-a1 (no push access to org). Always run before git push:

```bash
unset GITHUB_TOKEN && gh auth switch --user lozanojoaog11
```

Then `git push origin main` works. Do this EVERY TIME before pushing.
