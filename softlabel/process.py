from keras.applications import InceptionV3
from keras.models import Model
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from softlabel.image import Image
from softlabel.constants import vector_dir
import os
import numpy as np
from softlabel.logging import get_structured_logger
from logging.config import fileConfig

fileConfig("logging.ini")

log = get_structured_logger(__name__)


def image_iter(image_list):
    for idx, i in enumerate(image_list):
        try:
            image = Image(i)
            yield image
        except Exception as e:
            log.warn("Image could not be processed.", image=i, exception=e)


def vectorize_images(image_list, **kwargs):
    image_vectors = []
    n_images = len(image_list)

    base = InceptionV3(include_top=True, weights="imagenet",)
    model = Model(inputs=base.input, outputs=base.get_layer("avg_pool").output)

    if not os.path.exists(vector_dir):
        os.makedirs(vector_dir)

    for idx, i in enumerate(image_iter(image_list)):
        vector_path = os.path.join(vector_dir, os.path.basename(i.path) + ".npy")
        if os.path.exists(vector_path) and kwargs["use_cache"]:
            vector = np.load(vector_path)

        img = preprocess_input(img_to_array(i.original.resize((299, 299))))
        vector = model.predict(np.expand_dims(img, 0)).squeeze()
        np.save(vector_path, vector)

        image_vectors.append(vector)

        log.info(
            "[vectorize_images] Vectorized image. ", i=(idx + 1), n_images=n_images
        )

    return np.array(image_vectors)
