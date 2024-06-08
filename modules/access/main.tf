
data "google_project_iam_binding" "devops_iam_binding" { 
    binding {
        role = "roles/editor"
        members = [ for email in local.access_list.groups["devops"].emails : "user:${email}" ]
    }
}

data "google_project_iam_binding" "eboard_iam_binding" { 
    binding {
        role = "roles/viewer"
        members = [ for email in local.access_list.groups["eboard"].emails : "user:${email}" ]
    }
}