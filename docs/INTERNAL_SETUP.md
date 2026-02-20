# Internal Setup Guide for Samsung DS Environment

## JFrog Artifactory Configuration

This project uses **JFrog Artifactory** as the default PyPI repository for internal dependency management.

### Quick Start

```bash
uv install
```

That's it. The `pyproject.toml` is already configured to use `repo.samsungds.net`.

### What This Means

- ✅ All dependencies are resolved through Samsung DS internal Artifactory
- ✅ Works behind corporate proxy automatically
- ✅ No manual proxy configuration needed in `uv` or `pip`
- ✅ All team members use the same version set

### If You See Dependency Issues

**Problem**: Package resolution fails even with correct credentials

**Solution**:
1. Check your network connection to `repo.samsungds.net`
2. Verify VPN is active (if required)
3. Clear cache: `uv cache clean`
4. Retry: `uv install`

## Version Compatibility

- **Python**: 3.10+
- **fastmcp**: 2.3.4 (pinned for internal compatibility)
- **starlette**: 0.37.1 (pinned for internal compatibility)

These versions are tested on Samsung DS infrastructure and may differ from upstream. Do not update without team approval.

## Why This Matters

Bringing external open-source into Samsung DS requires:
1. Proxy handling (Artifactory solves this)
2. Version pinning to tested baselines
3. Security scanning (handled by Artifactory)
4. Reproducible builds

---

**First-time setup?** Start with JFrog authentication. Ask your team lead for credentials.
