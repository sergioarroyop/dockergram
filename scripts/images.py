import logging
import docker

client = docker.from_env()

def showImages(*status):
    show_images = []
    images = client.images.list()
    for image in images:
        image_data = {}
        if len(image.tags) != 0:
            image_data['Id'] = image.id
            image_data['Tags'] = image.tags[0]
            show_images.append(image_data)

    return show_images
