from superduperdb.misc.annotations import requires_packages

requires_packages(['PIL', '10.2.0', None, 'pillow'])

from .encoder import pil_image

__all__ = ['pil_image']
