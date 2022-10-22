import subprocess
import sys
import json
from modules.logginmod import Logging


class CromwellRequester:
    def __init__(self):
        self.CROMWELL_URL = 'http://localhost:8000'
        self.API_VERSION = 'v1'
        self.Logging = Logging('CromwellRequester', to_screen=True, screen_level='ERROR')
        if not self.check_cromwell_running():
            self.Logging.critical("Cromwell is not running. Server URL: " + self.CROMWELL_URL)
            sys.exit()
        else:
            self.Logging.debug("Cromwell is running")

    def submit_workflow(self, workflow, inputs=None, options=None):
        api_route = f'/api/workflows/{self.API_VERSION}'
        curl_command = f"curl -s -X 'POST' '{self.CROMWELL_URL + api_route}' -H 'accept: application/json' " \
                       f"-H 'Content-Type: multipart/form-data' " \
                       f"-F 'workflowSource=@{workflow}' "
        if inputs:
            curl_command += f"-F 'workflowInputs=@{inputs};type=application/json' "
        if options:
            curl_command += f"-F 'workflowOptions=@{options};type=application/json'"
        self.Logging.debug(f"Submit command: {curl_command}")
        exec_output = self.execute(curl_command)
        try:
            response = json.loads(exec_output)
            message = f"Execution id:\t{response['id']} \nStatus:\t{response['status']}"
            self.Logging.info(message)
            print(message)
            return response['id']
        except json.JSONDecodeError:
            self.Logging.critical(f"Could not be decoded into json: {exec_output}")

    def get_log(self, execution_id):
        return self.execute(self.base_get_command(execution_id, 'logs'))

    def get_status(self, execution_id):
        return self.execute(self.base_get_command(execution_id, 'status'))

    def get_outputs(self, execution_id):
        return self.execute(self.base_get_command(execution_id, 'outputs'))

    def get_metadata(self, execution_id):
        return self.execute(self.base_get_command(execution_id, 'metadata'))

    def abort_execution(self, execution_id):
        return self.execute(self.base_post_command(execution_id, 'abort'))

    def base_get_command(self, execution_id, option):
        api_route = f'/api/workflows/{self.API_VERSION}/{execution_id}/{option}'
        return f"curl -s -X 'GET' '{self.CROMWELL_URL + api_route}' -H 'accept: application/json'"

    def base_post_command(self, execution_id, option):
        api_route = f'/api/workflows/{self.API_VERSION}/{execution_id}/{option}'
        return f"curl -s -X 'POST' '{self.CROMWELL_URL +api_route}' -H 'accept: application/json' -d ''"

    def check_cromwell_running(self):
        api_route = f'/engine/{self.API_VERSION}/version'
        command = f"curl -s -X 'GET' '{self.CROMWELL_URL + api_route}' -H 'accept: application/json'"
        return bool(self.execute(command))

    @staticmethod
    def execute(command):
        execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        return execution.stdout.read().decode()
