# rozelle-stream

Infrastructure-as-code and static files for Rozelle's stream setup.

## Structure

```
.github/workflows/deploy.yml   → GitHub Actions: deploys on push to main
cloudformation/backend.yaml    → DynamoDB + Lambda + API Gateway
cloudformation/hosting.yaml    → S3 + CloudFront + Route53 (rozellerz.com)
lambda/lambda_function.py      → Stream state API handler
static/streamadmin/index.html  → Admin dashboard → rozellerz.com/streamadmin
static/overlay.html            → OBS Browser Source overlay
```
