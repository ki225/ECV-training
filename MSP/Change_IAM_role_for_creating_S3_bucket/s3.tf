provider "aws" {
  region = "us-east-1"  
}

# =========================== S3 ======================================
resource "aws_s3_bucket" "kiki-s3" {
  bucket = "kiki-s3-20240801"
  tags = {
    Name        = "kiki-bucket"
    Environment = "Dev"
  }
}
