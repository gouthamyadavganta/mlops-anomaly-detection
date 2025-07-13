terraform {
  backend "s3" {
    bucket         = "mlops-remote-backend-state"      # You'll create this
    key            = "dev/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "mlops-terraform-locks"           # You'll create this
    encrypt        = true
  }
}
