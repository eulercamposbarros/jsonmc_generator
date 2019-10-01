import pathlib
import json
import os
import requests
import click
from slugify import slugify
from dateutil.parser import parse

@click.group()
def cli():
    pass

@cli.command()
@click.argument('title')
@click.option('--key', envvar='OMDB_KEY')
def movies(title, key):
    if not key:
        click.echo(click.style('Please provide an OMDb API key', fg='red'))
    else:
        params = {
            't': title,
            'plot': 'full',
            'apikey': key
        }
        response = requests.get('http://www.omdbapi.com/', params=params)
        data = response.json()
        year = data.get('Year')
        if year:
            slug_title = slugify(data.get('Title'))
            file_name = "{}.json".format(slug_title)
            dir_path = pathlib.Path('jsonmc/movies/{year}'.format(year=year))
            dir_path.mkdir(parents=True, exist_ok=True)

            file_path = dir_path / file_name

            movie_info = {
                'name': data.get('Title'),
                'year': int(year),
                'runtime': int(data.get('Runtime', '0 min').replace(' min', '')),
                'categories': [g.lower() for g in data.get('Genre').split(", ")],
                'release-date': parse(data.get('Released')).strftime('%Y-%m-%d'),
                'director': data.get('Director'),
                'actors': data.get('Actors').split(", "),
                'storyline': data.get('Plot')
            }

            with open(file_path, 'w') as json_file:
                json.dump(movie_info, json_file, indent=4)
            click.echo(click.style('Movie in {}'.format(file_path), fg='green'))
        else:
            click.echo(click.style('No movies found!', fg='red'))

if __name__ == '__main__':
    cli()
