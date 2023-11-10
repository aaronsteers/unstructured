import typing as t
from dataclasses import dataclass

import click

from unstructured.ingest.cli.base.src import BaseSrcCmd
from unstructured.ingest.cli.interfaces import (
    CliConfig,
)

CMD_NAME = "azure"


@dataclass
class AzureCliConfig(CliConfig):
    account_id: t.Optional[str] = None
    account_name: t.Optional[str] = None
    connection_string: t.Optional[str] = None

    @staticmethod
    def get_cli_options() -> t.List[click.Option]:
        return [
            click.Option(
                ["--account-key"],
                default=None,
                help="Azure Blob Storage or DataLake account key (not required if "
                "`azure_account_name` is public).",
            ),
            click.Option(
                ["--account-name"],
                default=None,
                help="Azure Blob Storage or DataLake account name.",
            ),
            click.Option(
                ["--connection-string"],
                default=None,
                help="Azure Blob Storage or DataLake connection string.",
            ),
        ]


def get_base_src_cmd() -> BaseSrcCmd:
    return BaseSrcCmd(cmd_name=CMD_NAME, cli_config=AzureCliConfig, is_fsspec=True)


def get_base_dest_cmd():
    from unstructured.ingest.cli.base.dest import BaseDestCmd

    return BaseDestCmd(
        cmd_name=CMD_NAME, cli_config=AzureCliConfig, is_fsspec=True
    )
