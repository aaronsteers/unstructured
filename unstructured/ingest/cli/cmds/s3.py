import typing as t
from dataclasses import dataclass

import click

from unstructured.ingest.cli.base.src import BaseSrcCmd
from unstructured.ingest.cli.interfaces import (
    CliConfig,
)

CMD_NAME = "s3"


@dataclass
class S3CliConfig(CliConfig):
    anonymous: bool = False
    endpoint_url: t.Optional[str] = None

    @staticmethod
    def get_cli_options() -> t.List[click.Option]:
        return [
            click.Option(
                ["--anonymous"],
                is_flag=True,
                default=False,
                help="Connect to s3 without local AWS credentials.",
            ),
            click.Option(
                ["--endpoint-url"],
                type=str,
                default=None,
                help="Use this endpoint_url, if specified. Needed for "
                "connecting to non-AWS S3 buckets.",
            ),
        ]


def get_base_src_cmd():
    return BaseSrcCmd(cmd_name=CMD_NAME, cli_config=S3CliConfig, is_fsspec=True)


def get_base_dest_cmd():
    from unstructured.ingest.cli.base.dest import BaseDestCmd

    return BaseDestCmd(cmd_name=CMD_NAME, cli_config=S3CliConfig, is_fsspec=True)
