resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket        = "${var.project_name}-${var.environment}-mlflow-artifacts"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "mlflow" {
  bucket = aws_s3_bucket.mlflow_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "helm_chart_bucket" {
  bucket        = "${var.project_name}-${var.environment}-helm-chart-bucket"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "helm" {
  bucket = aws_s3_bucket.helm_chart_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

