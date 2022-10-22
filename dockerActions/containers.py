import docker

client = docker.from_env()

def showContainers(*status):
    show_containers = []
    containers = client.containers.list()
    for container in containers:
        container_data = {}
        container_data['Id'] = container.short_id
        container_data['Name'] = container.name
        container_data['Status'] = container.status

        show_containers.append(container_data)

    return show_containers

def showLogs(name):
    container_logs = ""
    container = client.containers.get(name)
    container_logs = container.logs().decode("utf-8")

    return container_logs

def stopContainer(name):
    container = client.containers.get(name)
    stop_container = container.stop()

    return stop_container
