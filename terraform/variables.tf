
variable "providers" {
    type = list(object({
        alias = string 
        project_name = string 
        credentials = string 
    }))
}