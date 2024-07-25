# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "kiki-docker"
}

# Task Definition
resource "aws_ecs_task_definition" "dvwa" {
  family                   = "dvwa"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  execution_role_arn = aws_iam_instance_profile.ssm_profile.arn
  container_definitions = jsonencode([
    {
      name  = "dvwa"
      image = "vulnerables/web-dvwa:latest"
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}



# ECS Service
resource "aws_ecs_service" "main" {
  name            = "my-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.dvwa.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [aws_subnet.subnet_1.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.main.arn
    container_name   = "my-container"
    container_port   = 80
  }
}