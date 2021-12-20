import click
import docker
import dockerpty

@click.command('provision')
def provision() -> None:
    '''
    provision a developer environment
    '''
    # client = docker.from_env()
    # container_obj = client.containers.run("ghcr.io/raiyanyahya/devenv/devenv:latest",stdin_open = True, tty = True, detach = True)
    # container_obj.id
    client = docker.Client()
    container = client.create_container(
    image='busybox:latest',
    stdin_open=True,
    tty=True,
    command='/bin/sh',
    )
    client.start(container)
    dockerpty.PseudoTerminal(client, container).start()