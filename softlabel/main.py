import os
import click
import glob2
from softlabel.process import vectorize_images, image_iter, get_umap_projection, cluster
from softlabel.logging import get_structured_logger
from logging.config import fileConfig
import uuid

fileConfig("logging.ini")

log = get_structured_logger(__name__)

config = {
    "images": None,
    "metadata": None,
    "out_dir": "output",
    "use_cache": True,
    "encoding": "utf8",
    "min_cluster_size": 20,
    "atlas_size": 2048,
    "cell_size": 32,
    "lod_cell_height": 128,
    "n_neighbors": 6,
    "min_dist": 0.001,
    "metric": "correlation",
    "pointgrid_fill": 0.05,
    "square_cells": False,
    "gzip": False,
    "plot_id": str(uuid.uuid1()),
}


def filter_images(image_list):

    filtered_images = []

    for i in image_iter(image_list):
        w, h = i.original.size

        if h == 0 or w == 0:
            log.warn(
                "[filter images] Skipping image because it has height or width 0",
                image=i.path,
            )
            continue

        try:
            resized = i.resize_to_max(n=config["lod_cell_height"])
        except ValueError:
            log.warn(
                "[filter images] Skipped image because it has height or width 0 when resized",
                image=i.path,
            )
            continue

        # remove images that are too wide for the atlas
        if (w / h) > (config["atlas_size"] / config["cell_size"]):
            log.warn(
                "[filter images] Skipped image because its dimensions are oblong.",
                image=i.path,
            )
            continue
        filtered_images.append(i.path)
    return filtered_images


@click.command()
@click.argument("images")
@click.argument("output", default=os.getcwd())
@click.argument("use_cache", default=False)
@click.argument("n_neighbours", default=15)
def main(images, output, use_cache, n_neighbours):
    image_list = sorted(glob2.glob(images, recursive=True))

    kwargs = {}
    kwargs["output"] = output
    kwargs["use_cache"] = use_cache

    image_list = filter_images(image_list)
    vectors = vectorize_images(image_list, **kwargs)

    kwargs["vectors"] = vectors
    kwargs["n_neighbours"] = n_neighbours
    kwargs["min_dist"] = config["min_dist"]
    kwargs["metric"] = config["metric"]
    get_umap_projection(kwargs)


if __name__ == "__main__":
    main()
