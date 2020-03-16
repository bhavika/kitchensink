import csv
import pytest
from dagster import execute_pipeline, execute_solid, pipeline, solid


@solid
def hello_cereal(context):
	dataset_path = 'data-eng/cereal.csv'
	with open(dataset_path, 'r') as input:
		cereals = [row for row in csv.DictReader(input)]
	context.log.info('Found {n_cereals} cereals.'.format(n_cereals=len(cereals)))

	return cereals


@solid
def sort_by_calories(context, cereals):
	sorted_cereals = list(
		sorted(cereals, key=lambda cereal: cereal['calories'])
	)
	context.log.info(
		'Least caloric cereal: {least_caloric}'.format(
			least_caloric=sorted_cereals[0]['name']
		)
	)
	context.log.info(
		'Most caloric cereal: {most_caloric}'.format(
			most_caloric=sorted_cereals[-1]['name']
		)
	)


@pipeline
def hello_cereal__2solid_pipeline():
	sort_by_calories(hello_cereal())


if __name__ == '__main__':
	result = execute_pipeline(hello_cereal__2solid_pipeline)
	assert result.success
