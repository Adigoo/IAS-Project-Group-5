import docker
client = docker.from_env()
print(docker.__version__)
print(':::::::::::::::::::::::::::::::::::::')
image = client.images.build(path = '.',tag='karthikeyanvalidation')
print(image)

print('Composing containers')
container = client.api.create_container(
    name='AutomatedContainer_5', #Dynamically creating Docker COntainers
    command='python3 main.py',
    image='karthikeyanvalidation',
    ports=[ 5000], #Internal Port mapping
    host_config=client.api.create_host_config(port_bindings={
        5000: 8005}) # External to internal port mapping
) 
print(container)
client.api.start(container=container.get('Id'))