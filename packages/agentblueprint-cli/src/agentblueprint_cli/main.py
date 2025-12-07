"""
AgentBlueprint CLI entrypoint.
"""
import click
from agentblueprint_cli.commands.run import run
from agentblueprint_cli.commands.init import init
from agentblueprint_cli.commands.tools import tools
from agentblueprint_cli.commands.docker import docker

@click.group()
@click.version_option()
def cli():
    """AgentBlueprint CLI tool."""
    pass

cli.add_command(run)
cli.add_command(init)
cli.add_command(tools)
cli.add_command(docker)


if __name__ == "__main__":
    cli()
