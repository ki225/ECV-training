# resource "aws_iam_role" "ecs_task_execution" {
#   name = "ec2_ssm_role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
       
#         Action :[
#                 "sts:AssumeRole",
#                 # "sts:SetSourceIdentity",
#                 # "sts:TagSession",
#                 # "ecs:RegisterTaskDefinition",
#                 # "ecs:ListTaskDefinitions",
#                 # "ecs:DescribeTaskDefinition",
#                 # "iam:CreateRole",
#                 # "iam:PutRolePolicy",
#                 # "iam:GetRole",
#                 # "iam:AttachRolePolicy",
#                 # "iam:PassRole",
                
#               ]
#         Effect = "Allow"
#         "Sid": "AllowCreateRoles"
#         Principal = {
#             "Service": [
#                   # "ecs.amazonaws.com",
#                   "application-autoscaling.amazonaws.com",
#                   "ecs-tasks.amazonaws.com"
#             ]
#         }
#       }
#     ]
#   })
# }

#  /* 
#         problem: creating ECS Task Definition (): operation error ECS: RegisterTaskDefinition
#         solution:
#         https://stackoverflow.com/questions/68873088/authorization-error-in-deploy-aws-ecs-task-definition-via-github-actions
#         */
#         // sts:AssumeRole needs to be in first position at the action attr.
#         // https://github.com/hashicorp/terraform-provider-aws/issues/32872
# resource "aws_iam_role_policy" "ecs_task_definition_policy" {
#   name = "ecsTaskDefinitionPolicy"
#   role = aws_iam_role.ecs_task_execution.id

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Action = [
#           "ecs:RegisterTaskDefinition",
#           "ecs:ListTaskDefinitions",
#           "ecs:DescribeTaskDefinition",
#           "iam:CreateRole"
#         ],
#         Resource = "*"
#       }
#     ]
#   })
# }


# resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
#   role       = aws_iam_role.ecs_task_execution.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
# }

# resource "aws_iam_role_policy_attachment" "ecs_ssm_policy" {
#   role       = aws_iam_role.ecs_task_execution.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
# }

# # Create an instance profile
# resource "aws_iam_instance_profile" "ssm_profile" {
#   name = "ec2_ssm_profile"
#   role = aws_iam_role.ecs_task_execution.name
# }


resource "aws_iam_role" "ecs_task_execution" {
  name = "ecs_task_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_ssm_policy" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
