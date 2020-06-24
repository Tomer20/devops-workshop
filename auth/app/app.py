from flask import Flask, request
from http import HTTPStatus
from exception_decorator import exit_exception
from logger import logger
from waitress import serve
import auth
import timer
import json
import os

app = Flask(__name__)
auth_users = auth.get_users_from_file()


class App:

    @staticmethod
    @exit_exception()
    def start_server():
        logger.info("Server is starting")
        serve(app, host='0.0.0.0', port=os.getenv("PORT", 8090))

    @staticmethod
    @app.route("/", methods=['GET'])
    def healthz():
        return app.response_class(
            response=json.dumps({"body": "devops k8s workshop"}),
            status=HTTPStatus.OK,
            mimetype='application/json'
        )

    @staticmethod
    @app.route("/<timetype>/<continental>/<capital>", methods=['GET'])
    def datetime(timetype, continental, capital):
        details = None
        try:
            logger.info(
                "Asked for {} in {}/{}".format(timetype, continental, capital))
            user_header = request.headers['k8s-ws']
            if user_header not in auth_users:
                details = "user unauthorized"
                status = HTTPStatus.UNAUTHORIZED
            else:
                response = timer.send_to_timer(timetype, continental, capital)
                status = HTTPStatus.OK
        except KeyError:
            details = "k8s-ws header is missing in the request"
            status = HTTPStatus.NOT_FOUND
        except Exception as e:
            details = "Internal server error: {trace}".format(trace=e)
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        if details:
            logger.error(details)
            response = json.dumps({"error": details})
        return app.response_class(
            response=json.dumps({"body": response}),
            status=status,
            mimetype='application/json'
        )


if __name__ == '__main__':
    App().start_server()
