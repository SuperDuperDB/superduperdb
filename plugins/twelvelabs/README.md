<!-- Auto-generated content start -->
# superduper_twelvelabs

Superduper allows users to work with TwelveLabs video understanding and multimodal embedding models (Pegasus and Marengo).

## Installation

```bash
pip install superduper_twelvelabs
```

## API


- [Code](https://github.com/superduper-io/superduper/tree/main/plugins/twelvelabs)
- [API-docs](/docs/api/plugins/superduper_twelvelabs)

| Class | Description |
|---|---|
| `superduper_twelvelabs.model.TwelveLabsTextEmbedding` | Marengo text embedding predictor. |
| `superduper_twelvelabs.model.TwelveLabsPegasus` | Pegasus video understanding predictor. |


## Examples

### TwelveLabsTextEmbedding

```python
from superduper_twelvelabs import TwelveLabsTextEmbedding
model = TwelveLabsTextEmbedding(identifier='marengo3.0')
model.predict('a cat playing piano')
```

### TwelveLabsPegasus

```python
from superduper_twelvelabs import TwelveLabsPegasus
model = TwelveLabsPegasus(
    identifier='pegasus1.5',
    prompt='Describe this video.',
    predict_kwargs={'max_tokens': 512},
)
model.predict('https://example.com/sample.mp4')
```


<!-- Auto-generated content end -->

<!-- Add your additional content below -->

## Authentication

Set your API key in the environment (recommended), or pass it explicitly via `api_key=`:

```bash
export TWELVELABS_API_KEY=<your-key>
```

You can grab a free API key at https://twelvelabs.io — there is a generous free tier.
