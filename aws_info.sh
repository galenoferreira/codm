#!/bin/bash

# Função para checar se a AWS CLI está instalada
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        echo "AWS CLI não está instalada. Por favor, instale a AWS CLI e configure as credenciais."
        exit 1
    fi
}

# Função para obter a quantidade de instâncias EC2 rodando
get_ec2_instances() {
    echo "Quantidade de instâncias EC2 rodando:"
    aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].[InstanceId]" --output text | wc -l
}

# Função para obter a quantidade de buckets no S3
get_s3_buckets() {
    echo "Quantidade de buckets no S3:"
    aws s3 ls | wc -l
}

# Função para obter a quantidade de spot requests ativas
get_spot_requests() {
    echo "Quantidade de Spot Requests ativas:"
    aws ec2 describe-spot-instance-requests --filters "Name=state,Values=active" --query "SpotInstanceRequests[*].SpotInstanceRequestId" --output text | wc -l
}

# Função para obter o valor gasto em USD no mês até a data atual
get_month_to_date_cost() {
    echo "Valor gasto em USD desde o primeiro dia do mês corrente até hoje:"
    end_date=$(date +%Y-%m-%d)
    start_date=$(date +%Y-%m-01)
    aws ce get-cost-and-usage --time-period Start=$start_date,End=$end_date --granularity MONTHLY --metrics "UnblendedCost" --query "ResultsByTime[0].Total.UnblendedCost.Amount" --output text
}


# Checar se a AWS CLI está instalada
check_aws_cli

# Obter informações
get_ec2_instances
get_s3_buckets
get_spot_requests
get_month_to_date_cost
