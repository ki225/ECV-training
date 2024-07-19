resource "aws_lb" "myalb" {
    name = "myalb"
    internal = false
    load_balancer_type = "application"
    security_groups = [ aws_security_group.alb_sg.id]
    subnets = [ aws_subnet.private1.id, aws_subnet.private2.id] 
}

resource "aws_lb_target_group" "alb_target_group" {
    name = "alb-tg"
    port = 80
    protocol = "HTTP"
    vpc_id = aws_vpc.main.id
}

resource "aws_lb_listener" "alb_listener" {
    load_balancer_arn = aws_lb.myalb.arn
    port = 80
    protocol = "HTTP"
    default_action {
        type = "forward"
        target_group_arn = aws_lb_target_group.alb_target_group.arn
    }
}

# alb security group
resource "aws_security_group" "alb_sg" {
  name        = "alb-sg"
  description = "Allow HTTP traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}