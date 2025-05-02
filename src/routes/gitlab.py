from flask import request
import src.gitlab.gitlab_connector as GitlabConnector
import src.gitlab.mr_custom_fields_handler as MrCustomFieldsHandler
import src.response.response_handler as Response


def register_gitlab_routes(app):
    # —— Test connection ————————————————————————————————————————————
    @app.route("/gitlab", methods=["GET"])
    def gitlab_test_connection():
        connector = GitlabConnector.get_gitlab_connector()
        if not connector:
            return Response.error("Gitlab is not configured")

        is_connected = connector.test_connection()
        if not is_connected:
            return Response.error("Failed to connect to Gitlab")
        return Response.success("Gitlab is connected")

    # —— Get merge requests ——————————————————————————————————————————
    @app.route("/gitlab/merge-requests", methods=["GET"])
    def gitlab_merge_requests():
        connector = GitlabConnector.get_gitlab_connector()
        if not connector:
            return Response.error("Gitlab is not configured")

        merge_requests = connector.get_merge_requests()
        if merge_requests is not None:
            return Response.success(
                message="Merge requests fetched successfully", data=merge_requests
            )
        return Response.error("Failed to fetch merge requests")

    # —— Update merge request custom fields ——————————————————————————
    @app.route(
        "/gitlab/merge-requests/<int:project_id>/<int:mr_iid>/custom-fields",
        methods=["POST", "PUT"],
    )
    def update_mr_custom_fields(project_id, mr_iid):
        try:
            data = request.get_json()
            if not data:
                return Response.error("No data provided")
        except Exception as e:
            return Response.error(f"Error: {e}")

        MrCustomFieldsHandler.update_mr_custom_fields(project_id, mr_iid, data)
        return Response.success(
            message="Merge request custom fields added/updated successfully",
            data=MrCustomFieldsHandler.get_mr_custom_fields(project_id, mr_iid),
        )
