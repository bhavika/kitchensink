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
import multiprocessing
from hdbscan import HDBSCAN
from collections import defaultdict, Counter
from sklearn.metrics import pairwise_distances_argmin_min
from umap import UMAP

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


def get_umap_projection(**kwargs):
    """Get the x,y positions of images passed through a umap projection"""
    print(" * creating UMAP layout")

    model = UMAP(
        n_neighbors=kwargs["n_neighbors"],
        min_dist=kwargs["min_dist"],
        metric=kwargs["metric"],
    )
    z = model.fit_transform(kwargs["vecs"])

    print(z)


def cluster(**kwargs):
    """Return the stable clusters from the condensed tree of connected components from the density graph"""
    print(
        " * HDBSCAN clustering data with "
        + str(multiprocessing.cpu_count())
        + " cores..."
    )
    config = {
        "min_cluster_size": kwargs["min_cluster_size"],
        "cluster_selection_epsilon": 0.01,
        "min_samples": 1,
        "core_dist_n_jobs": multiprocessing.cpu_count(),
    }
    z = HDBSCAN(**config).fit(kwargs["vecs"])
    # find the centroids for each cluster

    print(z)

    # d = defaultdict(list)
    # for idx, i in enumerate(z.labels_):
    #   d[i].append(kwargs['vecs'][idx])
    # centroids = []
    # for i in d:
    #   x, y = np.array(d[i]).T
    #   centroids.append(np.array([np.sum(x)/len(x), np.sum(y)/len(y)]))
    # closest, _ = pairwise_distances_argmin_min(centroids, kwargs['vecs'])
    # closest = set(closest)
    # print(' * found', len(closest), 'clusters')
    # paths = [kwargs['image_paths'][i] for i in closest]
    # data = [{
    #   'img': paths[idx],
    #   'label': 'Cluster {}'.format(idx+1),
    # } for idx,i in enumerate(closest)]
    #
