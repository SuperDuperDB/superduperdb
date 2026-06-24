import os

import pytest
import vcr

from superduper_twelvelabs import TwelveLabsPegasus, TwelveLabsTextEmbedding

CASSETTE_DIR = os.path.join(os.path.dirname(__file__), 'cassettes')


if os.getenv('TWELVELABS_API_KEY') is None:
    mp = pytest.MonkeyPatch()
    mp.setenv('TWELVELABS_API_KEY', 'tlk-TopSecret')


def test_default_shape():
    # No network: the Marengo embedding dimension is fixed at 512.
    embed = TwelveLabsTextEmbedding(identifier='marengo3.0')
    assert embed.shape == (512,)


@vcr.use_cassette(
    f'{CASSETTE_DIR}/test_embed_one.yaml',
    filter_headers=['x-api-key', 'authorization'],
)
def test_embed_one():
    embed = TwelveLabsTextEmbedding(identifier='marengo3.0')
    embed.setup()
    resp = embed.predict('a cat playing piano')

    assert len(resp) == embed.shape[0]
    assert isinstance(resp, list)
    assert all(isinstance(x, float) for x in resp)


@pytest.mark.skipif(
    os.getenv('TWELVELABS_API_KEY', 'tlk-TopSecret') == 'tlk-TopSecret',
    reason="Pegasus video analysis requires a live API key and a fetchable video.",
)
def test_pegasus_predict():
    model = TwelveLabsPegasus(
        identifier='pegasus1.5',
        prompt='Describe this video in one sentence.',
        predict_kwargs={'max_tokens': 512},
    )
    model.setup()
    resp = model.predict(
        'https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/'
        'Big_Buck_Bunny_720_10s_1MB.mp4'
    )
    assert isinstance(resp, str)
