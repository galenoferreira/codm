aws s3 ls s3://galeno-codm-dev-codm/ | grep PRE | awk '{print $2}' | xargs -I {} aws s3 rm s3://galeno-codm-dev-codm/{}cancel
aws s3 ls s3://galeno-codm-dev-codm/ | grep PRE | awk '{print $2}' | xargs -I {} aws s3 rm s3://galeno-codm-dev-codm/{}process
