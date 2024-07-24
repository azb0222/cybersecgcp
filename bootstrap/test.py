from google.cloud import billing
from google.cloud import service_usage

project_id = "gcp-playground-69420"

#enable API
client = service_usage.ServiceUsageClient()
request = service_usage.EnableServiceRequest(name=f"projects/{project_id}/services/cloudbilling.googleapis.com")

# Make the request
operation = client.enable_service(request=request)

print("Waiting for operation to complete...")

response = operation.result()

print(response)
assert(response.service.state == service_usage.State.ENABLED)
#link billing
client = billing.CloudBillingClient()

billing_id = "01ECF2-0C4FDB-AA6DEE"

resource = f"projects/{project_id}"
project_billing_info = {
    "billing_account_name": f"billingAccounts/{billing_id}"
}
request = billing.UpdateProjectBillingInfoRequest(
        name= resource,
        project_billing_info=project_billing_info
    )

 # Make the request
response = client.update_project_billing_info(request=request)

# Handle the response
print(response)