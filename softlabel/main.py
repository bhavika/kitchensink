import os
import click
import glob2
from softlabel.process import vectorize_images


def find_images(images):
    image_list = sorted(glob2.glob(images))
    return image_list


@click.command()
@click.argument("images")
@click.argument("output", default=os.getcwd())
def main(images):
    pass


if __name__ == "__main__":
    main()
