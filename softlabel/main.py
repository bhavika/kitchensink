import os
import click
import glob2
from softlabel.process import vectorize_images, image_iter


@click.command()
@click.argument("images")
@click.argument("output", default=os.getcwd())
@click.argument("--use_cache", default=False)
def main(images, output, use_cache):
	image_list = sorted(glob2.glob(images))

	kwargs = {}
	kwargs['output'] = output
	kwargs['use_cache'] = use_cache

	vectorize_images(image_list, **kwargs)

if __name__ == "__main__":
    main()
