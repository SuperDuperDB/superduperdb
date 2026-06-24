import os
import typing as t

from superduper.base.query_dataset import QueryDataset
from superduper.components.model import APIBaseModel
from superduper.misc.retry import Retry
from twelvelabs import TwelveLabs
from twelvelabs.core.api_error import ApiError
from twelvelabs.types.video_context import VideoContext_Url

retry = Retry(exception_types=(ApiError,))

KEY_NAME = 'TWELVELABS_API_KEY'


class _TwelveLabs(APIBaseModel):
    """TwelveLabs base predictor.

    :param api_key: The TwelveLabs API key. If not provided, it is read from
        the ``TWELVELABS_API_KEY`` environment variable.
    """

    api_key: t.Optional[str] = None

    def setup(self):
        """Initialize the TwelveLabs client."""
        super().setup()
        self.client = TwelveLabs(api_key=self.api_key or os.environ[KEY_NAME])


class TwelveLabsTextEmbedding(_TwelveLabs):
    """Marengo text embedding predictor.

    Embeds text into the same multimodal vector space as TwelveLabs video
    embeddings, so text queries can be matched against indexed video content.

    :param model: The Marengo model to use, e.g. ``'marengo3.0'``.
    :param shape: The shape of the embedding as a ``tuple``. If not provided,
        it is inferred by sending a short query to the API.

    Example:
    -------
    >>> from superduper_twelvelabs import TwelveLabsTextEmbedding
    >>> model = TwelveLabsTextEmbedding(identifier='marengo3.0')
    >>> model.predict('a cat playing piano')

    """

    model: t.Optional[str] = 'marengo3.0'
    shape: t.Optional[t.Sequence[int]] = None
    signature: str = 'singleton'

    def postinit(self):
        """Post-initialization method."""
        super().postinit()
        if self.shape is None:
            self.shape = (512,)

    @retry
    def predict(self, X: str):
        """Embed a single text string.

        :param X: The text to embed.
        """
        response = self.client.embed.create(model_name=self.model, text=X)
        return response.text_embedding.segments[0].float_


class TwelveLabsPegasus(_TwelveLabs):
    """Pegasus video understanding predictor.

    Generates text (descriptions, summaries, answers) from a video given a
    prompt. The input is a publicly accessible video URL that TwelveLabs
    fetches server-side.

    :param model: The Pegasus model to use, e.g. ``'pegasus1.5'``.
    :param prompt: The prompt sent with every video, e.g.
        ``'Describe this video.'``.

    Example:
    -------
    >>> from superduper_twelvelabs import TwelveLabsPegasus
    >>> model = TwelveLabsPegasus(
    >>>     identifier='pegasus1.5',
    >>>     prompt='Describe this video.',
    >>>     predict_kwargs={'max_tokens': 512},
    >>> )
    >>> model.predict('https://example.com/sample.mp4')

    """

    model: t.Optional[str] = 'pegasus1.5'
    prompt: str = 'Describe this video.'

    @retry
    def predict(self, X: str, **kwargs):
        """Analyse a single video URL with Pegasus.

        :param X: A publicly accessible URL of the video to analyse.
        :param kwargs: Extra keyword arguments forwarded to ``analyze``.
        """
        response = self.client.analyze(
            model_name=self.model,
            video=VideoContext_Url(url=X),
            prompt=self.prompt,
            **{**self.predict_kwargs, **kwargs},
        )
        return response.data

    def predict_batches(self, dataset: t.Union[t.List, QueryDataset]) -> t.List:
        """Analyse a series of video URLs.

        :param dataset: The dataset of video URLs to analyse.
        """
        return [self.predict(dataset[i]) for i in range(len(dataset))]
