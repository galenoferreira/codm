aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" | jq '.Reservations | length'
