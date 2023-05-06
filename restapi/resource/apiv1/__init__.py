from restapi.app import apiv1 as api
from restapi.resource.apiv1.user import UserResource

api.add_resource(
	UserResource,
	"/telegramalerts",
	methods=["GET", "POST"],
	endpoint="telegramalerts"  # It will be shown in response as key name.
)

