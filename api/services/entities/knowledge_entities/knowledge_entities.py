from typing import Literal, Optional, Union

from pydantic import BaseModel
from enum import Enum

class ParentMode(str, Enum):
    FULL_DOC = "full-doc"
    PARAGRAPH = "paragraph"

class NotionPage(BaseModel):
    page_id: str
    page_name: str
    page_icon: str

class NotionInfo(BaseModel):
    workspace_id: str
    pages: list[NotionPage]

class WebsiteInfo(BaseModel):
    provider: str
    job_id: str
    urls: list[str]
    only_main_content: bool

class FileInfo(BaseModel):
    file_ids: list[str]

class InfoList(BaseModel):
    data_source_type: Literal["upload_file", "notion_import", "website_crawl"]
    notion_info_list: Optional[list[NotionInfo]] = None
    file_info_list: Optional[FileInfo] = None
    website_info_list: Optional[WebsiteInfo] = None

class DataSource(BaseModel):
    info_list: InfoList

class PreProcessingRule(BaseModel):
    id: str
    enabled: bool

class Segmentation(BaseModel):
    separator: str = "\n"
    max_tokens: int
    chunk_overlap: int = 0

class Rule(BaseModel):
    pre_processing_rules: Optional[list[PreProcessingRule]] = None
    segmentation: Optional[Segmentation] = None
    parent_mode: Optional[Literal["full-doc", "paragraph"]] = None
    subchunk_segmentation: Optional[Segmentation] = None

class ProcessRule(BaseModel):
    mode: Literal["automatic", "custom", "hierarchical"]
    rules: Optional[Rule] = None


class RerankingModel(BaseModel):
    reranking_provider_name: str
    reranking_model_name: str

class RetrievalModel(BaseModel):
    search_method: Literal["hybrid_search", "semantic_search", "full_text_search"]
    reranking_enable: bool
    reranking_model: Optional[RerankingModel] = None
    top_k: int
    score_threshold_enabled: bool
    score_threshold: Optional[float] = None

class KnowledgeConfig(BaseModel):
    original_document_id: Optional[str] = None
    duplicate: bool = True
    indexing_technique: Literal["high_quality", "economy"]
    data_source: DataSource
    process_rule: Optional[ProcessRule] = None
    retrieval_model: RetrievalModel
    doc_form: str = "text_model"
    doc_language: str = "English"
    embedding_model: Optional[str] = None
    embedding_model_provider: Optional[str] = None