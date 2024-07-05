
variable "providers" {
    type = list(object({
        alias = string 
        project = string 
        credentials = string 
    }))
    default = jsondecode(file("./data/project.json"))["providers"]
}