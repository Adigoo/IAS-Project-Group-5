from flask import Flask,request
import logging
import constants
from services import node_manager ,action_manager,app_manager,deployer,kafka,model_manager,scheduler,sensor_manager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')
app= Flask(__name__)


@app.route('/init', methods=['POST'])
def init():
    response = {
        'status':500,
    }
    platform_services = [constants.SERVICE_MODEL_MANAGER,
                   constants.SERVICE_ACTION_MANAGER,
                   constants.SERVICE_APPLICATION_MANAGER,
                   constants.SERVICE_DEPLOYER,
                   constants.SERVICE_MESSAGE_BUS,
                   constants.SERVICE_NODEMANAGER,
                   constants.SERVICE_SCHEDULER,
                   constants.SERVICE_SENSOR_MANAGER
       ]
    dataFromRequest = request.args
    logging.debug('Received Request as {data}'.format(data=dataFromRequest))
    serviceInitStatus = {}
    logging.debug('============Initializing Platform for Hackathon 2===============')
    for service in platform_services:
        logging.debug('Platform Initilizer : Starting {serviceName}'.format(serviceName=service))
        try:
            logging.debug('Doing something for {serviceName}'.format(serviceName = service))
            if service == constants.SERVICE_NODEMANAGER:
                node_manager.execute()
            elif service == constants.SERVICE_ACTION_MANAGER:
                action_manager.execute()
            elif service == constants.SERVICE_APPLICATION_MANAGER:
                app_manager.execute()
            elif service == constants.SERVICE_DEPLOYER:
                deployer.execute()
            elif service == constants.SERVICE_MESSAGE_BUS:
                kafka.execute()
            elif service == constants.SERVICE_MODEL_MANAGER:
                model_manager.execute()
            elif service == constants.SERVICE_SCHEDULER:
                scheduler.execute()
            elif service == constants.SERVICE_SENSOR_MANAGER:
                sensor_manager.execute()
            else:
                raise Exception('Service Handler not found for {serviceName}'.format(serviceName=service))
            
            logging.debug('Platform Initilizer : Loading {serviceName} - Completed'.format(serviceName=service))
            serviceInitStatus[service]=constants.SUCCESS
        except:
            serviceInitStatus[service]=constants.FAILURE
            logging.error('Platform Initilizer : Failed Loading {serviceName} Check Platform initializer logs for more details'.format(serviceName=service))

        
    
    response['status']=200
    response['body']={
       'services_status': serviceInitStatus
    }
    return response


@app.route('/', methods=['GET'])
def info():
    return {'status':200,'statusMessage' :'Platform Initializer is Up and running. Please request to init endpoint with appropriate request'}

if __name__ == '__main__' :
    app.run(debug= True)