# FlaGs Visualisation 

python 


gcloud builds submit --tag gcr.io/flags-viz/dash-app --project=flags-viz
gcloud run deploy --image gcr.io/flags-viz/dash-app --platform manged project=flags-viz --allow-unauthenticated