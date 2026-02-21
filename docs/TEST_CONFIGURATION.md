# Test Configuration & Environment Setup

## Quick Start

```bash
# Run all unit tests (no API credentials needed)
pytest tests/

# Run integration tests (requires API credentials)
pytest tests/integration/
pytest tests/test_real_api_validation.py

# Run with verbose output
pytest -v tests/
```

## Environment Variables

### For Integration Tests

Create `.env` file:

```bash
# Jira
JIRA_URL=https://jira.samsungds.net
JIRA_USERNAME=your-username
JIRA_API_TOKEN=your-api-token

# OR use OAuth
ATLASSIAN_OAUTH_CLIENT_ID=your-client-id
ATLASSIAN_OAUTH_CLIENT_SECRET=your-client-secret
ATLASSIAN_OAUTH_REDIRECT_URI=http://localhost:8080/callback
ATLASSIAN_OAUTH_SCOPE=read:jira-work write:jira-work offline_access
ATLASSIAN_OAUTH_CLOUD_ID=your-cloud-id

# Confluence
CONFLUENCE_URL=https://confluence.samsungds.net/wiki
```

### For Real API Tests

Same as integration tests. Tests automatically skip if environment variables missing.

```bash
# This will skip automatically if JIRA_URL not set
pytest tests/test_real_api_validation.py
```

## Fixture Behavior

### Class-Scoped Fixtures

```python
@pytest.fixture(scope="class")
async def api_validation_client():
    # Created once per test class
    # Reused across all test methods in class
    # Better performance than function-scoped
```

**Impact:** Faster test execution, shared client connection within class.

### Config Fixtures with Fallback

```python
@pytest.fixture
def jira_config() -> JiraConfig:
    # Returns config from environment variables
    # Returns None if variables missing (no skip)
    return JiraConfig.from_env()
```

Tests handle None config gracefully (usually skip within test body).

## Missing Environment Variables

Tests do NOT automatically skip anymore:

**Before:**
```python
if not os.getenv("JIRA_URL"):
    pytest.skip("JIRA_URL not set")
```

**After:**
```python
# Automatic via from_env()
config = JiraConfig.from_env()  # Returns None if missing
# Test handles None gracefully
```

## Performance Notes

- **Unit tests** (~500ms): Fast, no API calls
- **Integration tests** (2-5s each): Require API credentials
- **Real API tests** (5-30s each): Depends on API response time

**Optimization:**
- Use `scope="class"` for fixtures shared by multiple tests
- Avoid creating new clients for every test
- Batch similar operations

## Troubleshooting

**Q: Tests fail with "JIRA_URL environment variable not set"?**
- A: Set environment variables in `.env` or shell

**Q: Tests timeout?**
- A: Check API connectivity and proxy settings

**Q: How do I run only one test?**
- A: `pytest tests/test_file.py::TestClass::test_method`

---

See `TESTING_STRATEGY.md` for what tests cover (MVP scope).
