module "vpc" {
  source = "./modules/vpc"
}

module "security_group" {
  source = "./modules/security_group"
  vpc_id = module.vpc.vpc_id
}

module "ssh_key" {
  source = "./modules/ssh_key"
  key_name = "nutrilab-key"
  public_key_path = "~/.ssh/nutrilab.pub"
}

module "ec2" {
  source      = "./modules/ec2"
  subnet_id   = module.vpc.subnet_id
  sg_id       = module.security_group.sg_id
  key_name    = module.ssh_key.key_name
}
