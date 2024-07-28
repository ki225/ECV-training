resource "aws_ssm_association" "example" {
  name = "AmazonCloudWatch-ManageAgent"

  targets {
    key    = "InstanceIds"
    values = [aws_instance.ecs_instance.id]
  }
}