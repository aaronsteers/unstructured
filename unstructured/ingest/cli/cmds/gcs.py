import typing as t
from dataclasses import dataclass

import click

from unstructured.ingest.cli.base.src import BaseSrcCmd
from unstructured.ingest.cli.interfaces import (
    CliConfig,
    FileOrJson,
)

CMD_NAME = "gcs"


@dataclass
class GcsCliConfig(CliConfig):
    service_account_key: t.Optional[t.Union[dict, str]] = None

    @staticmethod
    def get_cli_options() -> t.List[click.Option]:
        return [
            click.Option(
                ["--service-account-key"],
                default=None,
                type=FileOrJson(),
                help="Either the file path of the credentials file to use or a json string of "
                "those values to use for authentication",
            ),
        ]


def get_base_src_cmd() -> BaseSrcCmd:
    return BaseSrcCmd(cmd_name=CMD_NAME, cli_config=GcsCliConfig, is_fsspec=True)


def get_base_dest_cmd():
    from unstructured.ingest.cli.base.dest import BaseDestCmd

    return BaseDestCmd(cmd_name=CMD_NAME, cli_config=GcsCliConfig, is_fsspec=True)
