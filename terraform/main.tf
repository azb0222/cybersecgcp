module "access" {
    for_each = vars.providers
    source = "./modules/access"
    providers = {
      gcp = each.alias
    }
}


# can specify resource machine types, etc for the ctfd module, create var to differentiate for trianing paltform vs umass ctf, etc.
module "ctfd" { 
  source = "./modules/ctfd"
  providers = {
   #TODO: you should make providers into a dict so it makes more sense to reference them instead of indexing 
    gcp = providers["training"]
  }
}