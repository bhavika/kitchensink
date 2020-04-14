from dask.distributed import Client, progress
import os
import click
import dask.bag as db
import json
import geojson
import dask

def get_files(src):
    try:
        b = db.read_text(src).map(json.loads)
    except json.decoder.JSONDecodeError:
        print("bork")

    print(b.take(2))


@click.command()
@click.argument("src")
def start(src):
    import glob
    files = glob.glob(src)
    get_files(files)



if __name__ == '__main__':
    start()
