import logging
import constants
import yaml
from python_on_whales import DockerClient

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')

def execute(portNumber):
    logging.debug('trying to perform docker compose with {port}'.format(port=portNumber))
    dockerComposeDict = {'version': '3.7','services': {'backend': {'build': {'context': '.', 'dockerfile': 'Dockerfile'}, "command": "python3 main.py", 'ports': ['{port}:5000'.format(port=portNumber)], 'volumes': ['.:/app']}}}

    with open(r'{serviceName}-dockerCompose.yaml'.format(serviceName = constants.SERVICE_NODEMANAGER), 'w') as file:
        documents = yaml.dump(dockerComposeDict, file,sort_keys=False)

    
    docker = DockerClient(compose_files=["./{serviceName}-dockerCompose.yaml".format(serviceName = constants.SERVICE_DEPLOYER)])
    docker.compose.build()
    docker.compose.up(detach=True)
    logging.debug('{serviceName} loaded successfully'.format(serviceName = constants.SERVICE_DEPLOYER))