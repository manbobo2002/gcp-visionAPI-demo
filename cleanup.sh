export PROJECT_ID=$(gcloud config list --format 'value(core.project)' 2>/dev/null)

gcloud iam service-accounts delete vision-api-account@${PROJECT_ID}.iam.gserviceaccount.com -q