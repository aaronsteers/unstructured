import typing as t
from dataclasses import dataclass

import click

from unstructured.ingest.cli.base.src import BaseSrcCmd
from unstructured.ingest.cli.interfaces import (
    CliConfig,
)

CMD_NAME = "box"


@dataclass
class BoxCliConfig(CliConfig):
    box_app_config: t.Optional[str] = None

    @staticmethod
    def get_cli_options() -> t.List[click.Option]:
        return [
            click.Option(
                ["--box-app-config"],
                default=None,
                help="Path to Box app credentials as json file.",
            ),
        ]


def get_base_src_cmd() -> BaseSrcCmd:
    return BaseSrcCmd(cmd_name=CMD_NAME, cli_config=BoxCliConfig, is_fsspec=True)


def get_base_dest_cmd():
    from unstructured.ingest.cli.base.dest import BaseDestCmd

    return BaseDestCmd(cmd_name=CMD_NAME, cli_config=BoxCliConfig, is_fsspec=True)
