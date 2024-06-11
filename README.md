## Info 
- Because we do not have a Google Workspace or Cloud Identity Account, we do not have an "Organization" or "Folder" resource 

- "Project" resources are not managed via Terraform \
To create a new project, run: 
`gcloud projects create example-foo-bar-1 --name="Happy project" --labels=type=happy` \
*See: Terraform does not allow you to provision projects without an "Organization" resource* (https://stackoverflow.com/questions/60911807/terraform-google-cloud-why-cannot-i-create-a-new-project-without-having-an-org)


## GCP Structure 

#### Projects 
1) **General**: hosts any general resources, TODO: manage our DNS here too 
2) **Training Platform** //Cloud Run, Cloud Build 
3) **UMassCTF_Internal 2024** 
4) **LoadTesting** //we will shut off unless actively using 


#### IAM 
Because we do not have an "Organization" resource, we cannot create Google Groups. 
To add your email account to either group, modify the accessList.json, create a PR, and ping any person in the devops group for approval. 

#TODO: user will still have to be manually invited to join project? see if there is a gcloud command

We have two groups of user accounts: 
1) **eboard**: `roles/viewer` for all GCP resources
2) **devops**: `roles/editor` for all GCP resources  

## Getting Started
### Connecting to a provider
TODO

### Making the projects
You can configure the projects you want in the [projects.json](./data/projects.json) file then simply run the [setup.py](./setup.py) script to provision them.
