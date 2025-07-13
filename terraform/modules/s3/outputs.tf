output "mlflow_bucket_name" {
  value = aws_s3_bucket.mlflow_artifacts.bucket
}

output "helm_chart_bucket_name" {
  value = aws_s3_bucket.helm_chart_bucket.bucket
}

