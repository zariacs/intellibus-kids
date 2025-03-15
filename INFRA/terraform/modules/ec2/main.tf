resource "aws_instance" "app_server" {
  ami           = "ami-08b5b3a93ed654d19"
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  security_groups = [var.sg_id]
  key_name      = var.key_name

  tags = {
    Name = "NutriLabAppServer"
  }
}

output "instance_ip" {
  value = aws_instance.app_server.public_ip
}
