import typing as t
from dataclasses import dataclass

from unstructured.ingest.pipeline.interfaces import DocFactoryNode


@dataclass
class DocFactory(DocFactoryNode):
    def run(self, *args, **kwargs) -> t.Iterable[dict]:
        docs = self.source_doc_connector.get_ingest_docs()
        return [doc.to_dict() for doc in docs]
