import subprocess
import sys
import json
from modules.logginmod import Logging


class CromwellRequester:
    def __init__(self):
        self.CROMWELL_URL = 'http://localhost:8000'
        self.API_VERSION = 'v1'
        self.Logging = Logging('CromwellRequester', to_screen=False, screen_level='INFO')
        if not self.check_cromwell_running():
            self.Logging.critical("Cromwell is not running. Server URL: " + self.CROMWELL_URL)
            sys.exit()

    def submit_workflow(self, workflow, inputs=None, options=None):
        api_route = f'/api/workflows/{self.API_VERSION}'
        curl_command = f"curl -X 'POST' '{self.CROMWELL_URL+api_route}' -H 'accept: application/json' " \
                       f"-H 'Content-Type: multipart/form-data' " \
                       f"-F 'workflowSource=@{workflow}' "
        if inputs:
            curl_command += f"-F 'workflowInputs=@{inputs};type=application/json' "
        if options:
            curl_command += f"-F 'workflowOptions=@{options};type=application/json''"
        response = json.loads(self.execute(curl_command))
        message = f"Execution id:\t{response['id']} \nStatus:\t{response['status']}"
        self.Logging.info(message)
        print(message)

    def check_cromwell_running(self):
        api_route = f'/engine/{self.API_VERSION}/version'
        command = f"curl -s -X 'GET' '{self.CROMWELL_URL+api_route}' -H 'accept: application/json'"
        return bool(self.execute(command))

    @staticmethod
    def execute(command):
        execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        return execution.stdout.read().decode()

