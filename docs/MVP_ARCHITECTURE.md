# MVP Architecture: What's Been Removed & Why

## Design Principle

```
Core Operations > Advanced Features
Maintainability > Feature Completeness
Developer Experience > Simplicity
```

## Removed Configurations

### 1. HTTP Request Timeouts
**Removed from:** `oauth.py`, `oauth_setup.py`

- Removed: `HTTP_CONNECT_TIMEOUT`, `HTTP_READ_TIMEOUT` constants
- Removed: `timeout` parameters from `requests.post()` and `requests.get()` calls
- Uses: System default timeouts (~socket default: infinite or 120s depending on OS)

**Why:**
- Timeout tuning should happen at proxy/infrastructure layer
- Application-level timeouts add complexity for marginal benefit
- Samsung DS proxy (JFrog) handles timeout management

### 2. Client Certificate Authentication
**Removed from:** `ssl.py`

- Removed: `client_cert`, `client_key`, `client_key_password` parameters
- Removed: Client certificate setup logic

**Why:**
- Certificates are terminated at proxy layer, not application layer
- Simplifies codebase and reduces developer confusion
- Security policy: Keys managed centrally by IT

### 3. Stateless HTTP Server Mode
**Removed from:** CLI (`__init__.py`)

- Removed: `--stateless` command-line flag
- Removed: Stateless mode environment variable checks
- Removed: `stateless_http` server configuration

**Why:**
- Stateless mode is advanced, rarely needed
- MVP operates in stateful mode
- Adds complexity to CLI argument handling
- Platform-specific deployment can enable if needed

### 4. Windows CPU Optimization
**Removed from:** CLI initialization (`__init__.py`)

- Removed: `asyncio.WindowsSelectorEventLoopPolicy()` configuration
- Uses: Platform default event loop policy

**Why:**
- Windows-specific optimization for high-CPU scenarios
- Reduces CPU from ~3-5% to near-zero only in edge cases
- Should be handled at deployment/container level if needed
- Adds platform-specific code that complicates maintenance

## Architecture Decision

All "infrastructure concerns" moved out of application code:

| Concern | Handled By | Configuration |
|---------|-----------|---|
| SSL/TLS certificates | Proxy layer | `HTTP_PROXY`, `HTTPS_PROXY` |
| Request timeouts | Proxy/OS defaults | (none - uses defaults) |
| Client certificates | Proxy layer | (not applicable) |
| CPU optimization | Container/deployment | (not applicable) |

## For Developers

**If you need these features:**
1. Check proxy/infrastructure configuration first
2. Open an issue with specific use case
3. We can add back if proven necessary for core operations

---

See `PROXY_AND_AUTHENTICATION.md` for proxy setup details.
