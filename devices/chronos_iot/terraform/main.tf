locals {
  files = fileset(path.cwd, "devices/*/policy.json")
}

provider "aws" {
  profile    = "chronos"
  region     = "us-east-1"
}
