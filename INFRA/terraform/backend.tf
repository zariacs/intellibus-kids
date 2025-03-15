terraform {
  backend "s3" {
    bucket         = "nutrilab-terraform-state-bucket"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    access_key     = "{{Enter access key}}"
    secret_key     = "{{Enter secret key}}"
  }
}
