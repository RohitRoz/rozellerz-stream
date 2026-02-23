# rozelle-stream

Infrastructure-as-code and static files for Rozelle's live stream setup.

## Structure

```
.github/workflows/deploy.yml   → GitHub Actions: deploys on push to main
cloudformation/backend.yaml    → DynamoDB + Lambda + API Gateway
cloudformation/hosting.yaml    → S3 + CloudFront + Route53 (rozellerz.com)
lambda/lambda_function.py      → Stream state API handler
static/streamadmin/index.html  → Admin dashboard → rozellerz.com/streamadmin
static/overlay.html            → OBS Browser Source overlay
```

## Live

| | URL |
|---|---|
| Stream Admin | https://rozellerz.com/streamadmin |
| API | https://bpxi65yy45.execute-api.us-east-1.amazonaws.com/live/state |

---

## One-time setup

### GitHub secrets (Settings → Secrets → Actions)

| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |

### GitHub variable (Settings → Variables → Actions)

| Variable | Value |
|---|---|
| `AWS_ACCOUNT_ID` | `882951811364` |

### Clean up manually-created resources before first push

```bash
# Delete manually-created API Gateway
aws apigateway delete-rest-api --rest-api-id bpxi65yy45 --region us-east-1

# Delete Lambda
aws lambda delete-function --function-name rozelle-stream-state --region us-east-1

# Delete IAM role (detach policies first)
aws iam detach-role-policy --role-name rozelle-stream-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role-policy --role-name rozelle-stream-lambda-role --policy-name dynamo-stream-state
aws iam delete-role --role-name rozelle-stream-lambda-role
```

> DynamoDB table has `DeletionPolicy: Retain` — it will never be auto-deleted.

---

## Deploying changes

Push to `main` — the workflow only redeploys what changed.

For a full redeploy: **Actions → Deploy Rozelle Stream → Run workflow**

## Cost: ~$0.50/month (Route53 only)
