from .model import OpenAIChatCompletion, OpenAIEmbedding
from importlib.metadata import version as _version, PackageNotFoundError

try:
    __version__ = _version("superduper_openai")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ('OpenAIChatCompletion', 'OpenAIEmbedding')
