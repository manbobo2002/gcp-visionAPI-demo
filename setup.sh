export PROJECT_ID=$(gcloud config list --format 'value(core.project)' 2>/dev/null)

gcloud iam service-accounts create vision-api-account
gcloud iam service-accounts keys create vision-api-key.json --iam-account=vision-api-account@${PROJECT_ID}.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS=./vision-api-key.json
pip install --upgrade google-cloud-vision
python app.py