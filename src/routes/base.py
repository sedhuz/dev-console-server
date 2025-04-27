import src.response.response_handler as Response


def register_base_routes(app):
    @app.route("/", methods=["GET"])
    def connection_check():
        return Response.success("OK")
