import docker

client = docker.from_env()

def showContainers():
    show_containers = []
    containers = client.containers.list()
    for container in containers:
        container_data = {}
        container_data['Id'] = container.short_id
        container_data['Name'] = container.name
        container_data['Status'] = container.status

        show_containers.append(container_data)

    return show_containers