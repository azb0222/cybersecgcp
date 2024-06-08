{for s in var.list : s => upper(s)}

data "google_project_iam_binding" "devops_iam_binding" { 

    binding {
        role = "roles/editor"

        members = [
            # "user:abodepudi@umass.edu", 
            # "user:ogpatel@umass.edu", 
            # "user:asrithabodepudi@gmail.com", 
            for email in devops_user_emails : "user:${email}" 
        ]
    }
}

//CREATE FOR LOOP TO GO THROUGH EACH PROJECT AND ADD THESE

data "google_project_iam_binding" "eboard_iam_binding" { 
    project = "your-project-id" #TODO: add as data variable 

    binding {
        role = "roles/viewer"

        members = [
            for email in eboard_user_emails : "user:${email}" 
        ]
    }
}