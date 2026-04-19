terraform {
  backend "s3" {
    bucket         = "my-terraform-logistics-bucket-123456"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    use_lockfile   = true
    encrypt        = true
  }
}
