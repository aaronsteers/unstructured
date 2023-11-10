import typing as t
from dataclasses import dataclass

import click

from unstructured.ingest.cli.base.src import BaseSrcCmd
from unstructured.ingest.cli.interfaces import (
    CliConfig,
)

CMD_NAME = "dropbox"


@dataclass
class DropboxCliConfig(CliConfig):
    token: str

    @staticmethod
    def get_cli_options() -> t.List[click.Option]:
        return [
            click.Option(
                ["--token"],
                required=True,
                help="Dropbox access token.",
            ),
        ]


def get_base_src_cmd() -> BaseSrcCmd:
    return BaseSrcCmd(
        cmd_name=CMD_NAME, cli_config=DropboxCliConfig, is_fsspec=True
    )


def get_base_dest_cmd():
    from unstructured.ingest.cli.base.dest import BaseDestCmd

    return BaseDestCmd(
        cmd_name=CMD_NAME, cli_config=DropboxCliConfig, is_fsspec=True
    )
