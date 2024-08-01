aws s3 ls s3://galeno-codm-dev-codm/ | awk '{print $2}' | xargs -I {} aws s3 cp settings.yaml s3://galeno-codm-dev-codm/
