locals { 
    access_list = jsondecode(file("${path.module}/accessList.json"))
    eboard_user_emails = [
        for email in local.access_list.groups[0] : email         
    ]
    devops_user_emails = [
        for email in local.access_list.groups[1] : email         
    ]
}

locals { 
    projects = jsondecode(file("${path.module}/projects.json"))
    project_ids = [
        for name in local.projects.project_names: "${projects.project_id}${name}"
    ]
    project_names = [
        for name in local.projects.project_names: name 
    ]
}

#TODO: delete after 
output "devops" { 
    value = local.devops_user_emails
}

output "eboard" { 
    value = local.eboard_user_emails
}
