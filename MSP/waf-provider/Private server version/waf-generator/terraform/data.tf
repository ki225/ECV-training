data "aws_caller_identity" "kg_identity" {}

data "aws_iam_role" "existing_ssm_role" {
  name = "kg-terraform-role"  # Replace with your actual SSM role name
}