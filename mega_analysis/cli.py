# -*- coding: utf-8 -*-

"""Console script to delete experiments."""
import sys
import click

@click.command()
@click.argument('semiology-term', type=str)
@click.argument('output-path', type=click.Path(dir_okay=False))
def main(semiology_term, output_path):
    from mega_analysis import get_scores
    get_scores(semiology_term, output_path=output_path)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    sys.exit(main())  # pragma: no cover
