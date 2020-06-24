from flask import Flask
from http import HTTPStatus
from exception_decorator import exit_exception
from logger import logger
from waitress import serve
import world_api
import json
import os

app = Flask(__name__)


class App:

    @staticmethod
    @exit_exception()
    def start_server():
        logger.info("Server is starting")
        serve(app, host='0.0.0.0', port=os.getenv("PORT", 8080))

    @staticmethod
    @app.route("/", methods=['GET'])
    def healthz():
        return app.response_class(
            response=json.dumps({"body": "devops k8s workshop"}),
            status=HTTPStatus.OK,
            mimetype='application/json'
        )

    @staticmethod
    @app.route("/datetime/<continental>/<capital>", methods=['GET'])
    def datetime(continental, capital):
        details = None
        try:
            logger.info(
                "Asked for time in {}/{}".format(continental, capital))
            response = world_api.get_datetime(continental, capital)
            status = HTTPStatus.OK
        except KeyError:
            details = "Datetime not found for {}/{}".format(
                continental, capital)
            status = HTTPStatus.NOT_FOUND
        except Exception as e:
            details = "Internal server error: {trace}".format(trace=e)
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        if details:
            logger.error(details)
            response = json.dumps({"error": details})
        return app.response_class(
            response=json.dumps({"datetime": response}),
            status=status,
            mimetype='application/json'
        )

    @staticmethod
    @app.route("/epochtime/<continental>/<capital>", methods=['GET'])
    def epochtime(continental, capital):
        details = None
        try:
            logger.info(
                "Asked for time in {}/{}".format(continental, capital))
            response = world_api.get_epochtime(continental, capital)
            status = HTTPStatus.OK
        except KeyError:
            details = "Epochtime not found for {}/{}".format(
                continental, capital)
            status = HTTPStatus.NOT_FOUND
        except Exception as e:
            details = "Internal server error: {trace}".format(trace=e)
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        if details:
            logger.error(details)
            response = json.dumps({"error": details})
        return app.response_class(
            response=json.dumps({"epochtime": response}),
            status=status,
            mimetype='application/json'
        )


if __name__ == '__main__':
    App().start_server()
