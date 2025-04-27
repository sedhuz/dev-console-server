from flask import jsonify, request
import src.response.response_handler as Response
import src.config.config_handler as GitlabConfig
import src.gitlab.gitlab_connector as GitlabConnector


def register_preferences_routes(app):
    @app.route("/preferences/gitlab", methods=["GET"])
    def get_gitlab_preferences():
        return Response.success(
            data={
                "url": GitlabConfig.get_gitlab_url(),
                "project_id": GitlabConfig.get_gitlab_project_id(),
                "token": GitlabConfig.get_gitlab_access_token(),
                "is_configured": GitlabConfig.is_gitlab_configured(),
            }
        )

    @app.route("/preferences/gitlab", methods=["PUT"])
    def update_gitlab_preferences():
        # —— Input validation —————————————————
        # —— Empty
        data = request.get_json()
        if not data:
            return Response.error("No data provided")
        # —— Required fields
        required_fields = ["url", "token", "project_id"]
        if not all(field in data for field in required_fields):
            return Response.error(
                f"Missing required fields. Required: {', '.join(required_fields)}"
            )

        # —— Test connection —————————————————
        connector = GitlabConnector.get_gitlab_connector(
            data["url"], data["token"], data["project_id"]
        )
        if not connector:
            return Response.error("Failed to create gitLab connector")

        is_connected = connector.test_connection()
        if not is_connected:
            return Response.error("Failed to connect with provided credentials")

        # —— Update configuration —————————————
        try:
            GitlabConfig.set_gitlab_url(data["url"])
            GitlabConfig.set_gitlab_access_token(data["token"])
            GitlabConfig.set_gitlab_project_id(data["project_id"])

            return Response.success(
                message="Gitlab preferences updated successfully",
                data={
                    "url": data["url"],
                    "project_id": data["project_id"],
                    "token": data["token"],
                    "is_configured": True,
                },
            )

        except Exception as e:
            return Response.error(f"Failed to update preferences: {str(e)}")
