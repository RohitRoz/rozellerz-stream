# stream-infra

IaC and static files for live stream tooling.

## Structure

```
.github/workflows/deploy.yml
cloudformation/backend.yaml
cloudformation/hosting.yaml
lambda/lambda_function.py
static/streamadmin/index.html
static/overlay.html
```

## Setup

Add to GitHub repository secrets and variables before running the workflow.

Secrets: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Variables: AWS_ACCOUNT_ID

Trigger deploy manually via Actions tab.
