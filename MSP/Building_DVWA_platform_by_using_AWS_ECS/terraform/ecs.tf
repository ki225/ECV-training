# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "kiki-docker"
}

# Task Definition
resource "aws_ecs_task_definition" "dvwa" {
  family                   = "dvwa"
  /*
  creating ECS Service (my-service): operation error ECS: CreateService, https response error StatusCode: 400, RequestID: 475a59bf-c562-4890-abc1-320bae82358c, InvalidParameterException: The provided target group arn:aws:elasticloadbalancing:us-east-1:429555954826:targetgroup/main-tg/f3e27a2ceae781be has target type instance, which is incompatible with the awsvpc network mode specified in the task definition.
  */
  network_mode             = "bridge" # https://stackoverflow.com/questions/60502112/ecs-target-type-ip-is-incompatible-with-the-bridge-network-mode-specified-in-t
  requires_compatibilities = ["EC2"]
  cpu                      = "256"
  memory                   = "512"

  execution_role_arn = aws_iam_role.ecs_task_execution.arn
  container_definitions = jsonencode([
    {
      name  = "dvwa"
      image = "vulnerables/web-dvwa:latest"
      essential = true
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
  launch_type     = "EC2"

  // 當使用 bridge network mode 時，不需要在 aws_ecs_service 資源中指定 network_configuration。相反，當使用 awsvpc network mode 時，必須指定 network_configuration。
  # network_configuration {
  #   subnets = [aws_subnet.subnet_1.id]
  #   security_groups = [aws_security_group.sg.id] 
  #   assign_public_ip = true
  # }
  load_balancer {
    target_group_arn = aws_lb_target_group.main.arn
    container_name   = "dvwa" # name should be right
    container_port   = 80
  }
  # depends_on = [aws_lb_target_group.main]
  # deployment_minimum_healthy_percent = 50
  # deployment_maximum_percent         = 200
  # lifecycle {
  #   ignore_changes = [task_definition]
  # }
}

resource "aws_instance" "ecs_instance" {
  ami           = "ami-09aa9497baa9dbca3" # amzn2-ami-ecs-hvm-2.0.20240723-x86_64-ebs
  instance_type = "t2.micro"
  key_name      = "kp"
  subnet_id     = aws_subnet.subnet_1.id 
  vpc_security_group_ids = [aws_security_group.sg.id]  

  tags = {
    Name = "ecs-instance"
  }

  # 安裝 ECS agent
  user_data = <<-EOF
                #!/bin/bash
                sudo apt-get update -y
                sudo apt-get upgrade -y
                sudo docker pull vulnerables/web-dvwa
                sudo docker run -d -p 80:80 vulnerables/web-dvwa
                EOF
}
