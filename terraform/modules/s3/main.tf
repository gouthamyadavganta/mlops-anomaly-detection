
resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket        = "${var.project_name}-${var.environment}-mlflow-artifacts"
  force_destroy = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "mlflow_artifacts" {
  bucket = aws_s3_bucket.mlflow_artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "mlflow_artifacts" {
  bucket                  = aws_s3_bucket.mlflow_artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


resource "aws_s3_bucket" "helm_chart_bucket" {
  bucket        = "${var.project_name}-${var.environment}-helm-chart-bucket"
  force_destroy = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "helm_chart_bucket" {
  bucket = aws_s3_bucket.helm_chart_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "helm_chart_block" {
  bucket                  = aws_s3_bucket.helm_chart_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

