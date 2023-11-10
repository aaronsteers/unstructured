from unstructured.ingest.cli.base.src import BaseSrcCmd

CMD_NAME = "fsspec"


def get_base_src_cmd() -> BaseSrcCmd:
    return BaseSrcCmd(cmd_name=CMD_NAME, is_fsspec=True)


def get_base_dest_cmd():
    from unstructured.ingest.cli.base.dest import BaseDestCmd

    return BaseDestCmd(cmd_name=CMD_NAME, is_fsspec=True)
