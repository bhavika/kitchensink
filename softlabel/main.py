import os
from torchvision.models import inception_v3
from keras.applications import VGG19, InceptionV3
from keras.models import Model


def main():
	print(inception_v3())
	base = InceptionV3(include_top=True, weights='imagenet', )
	print(base)


if __name__ == '__main__':
	main()