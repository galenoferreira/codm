aws s3 ls s3://geonex-maas-prod-codm/ | grep PRE | awk '{print $2}' | xargs -I {} aws s3 rm s3://geonex-maas-prod-codm/{}cancel
aws s3 ls s3://geonex-maas-prod-codm/ | grep PRE | awk '{print $2}' | xargs -I {} aws s3 rm s3://geonex-maas-prod-codm/{}process
