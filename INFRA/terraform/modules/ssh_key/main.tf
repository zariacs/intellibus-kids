resource "null_resource" "generate_ssh_key" {
  provisioner "local-exec" {
    command = <<EOT
      if [ ! -f ~/Desktop/nutrilab ]; then
        ssh-keygen -t rsa -b 4096 -C "terraform-ec2" -f ~/Desktop/nutrilab -N ""
      fi
    EOT
  }
}

data "external" "read_ssh_public_key" {
  program = ["bash", "-c", "jq -n --arg key \"$(cat ~/Desktop/nutrilab.pub | tr -d '\n')\" '{\"output\": $key}'"]

  depends_on = [null_resource.generate_ssh_key]
}

resource "aws_key_pair" "deployer" {
  key_name   = var.key_name
  public_key = data.external.read_ssh_public_key.result["output"]

  depends_on = [data.external.read_ssh_public_key]
}

output "key_name" {
  value = aws_key_pair.deployer.key_name
}
