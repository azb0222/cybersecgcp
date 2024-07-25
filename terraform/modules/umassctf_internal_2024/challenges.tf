// TODO: should read from auto generated terraform.tfvars upon merge
//TODO: shouldn't this be in a variables file?
variable "dynamic_challenges" {
  type = map(object({
    name = string
    dir = string //relative dir path to root dir
    category = string //TODO: place validation check so only some categories are allowed
    dbNeeded = bool
    cacheNeeded = bool
    #env values?
  }))
  default = {
    example_dynamic = {
      name = "example-dynamic"
      dir = "./challenges/examples/dynamic-example"
      category = "examples"
      dbNeeded = false
      cacheNeeded = false
    }
    web_test_delete_later = {
      name = "web-test-delete-later"
      dir = "./challenges/web/web-test-delete-later"
      category = "web"
      dbNeeded = false
      cacheNeeded = false
    }
  }
}
