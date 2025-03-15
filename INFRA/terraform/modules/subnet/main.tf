resource "aws_subnet" "main" {
  vpc_id     = var.vpc_id
  cidr_block = var.cidr_block
  availability_zone = var.az

  tags = {
    Name = "intellibus-subnet"
  }
}

output "subnet_id" {
  value = aws_subnet.main.id
}

output "cidr_block" {
  value = aws_subnet.main.cidr_block
}