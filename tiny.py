# -*- coding: utf-8 -*-

import click
import tinify
import os
import sys

tinify.key = os.environ['TINIFY_KEY']

@click.command()
@click.argument('input', nargs=-1, required=False)
def cli(input):
    """
        Tiny PNG CLI Tool \n
        takes single or multiple files and/or folders and minifies all png's and jpg's respectively
    """

    def update_progress(progress):
        barLength = 10
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if progress >= 1:
            progress = 1
            status = "✔ Done\r\n"
        block = int(round(barLength*progress))
        text = "\rSatus: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
        sys.stdout.write(text)
        sys.stdout.flush()

    click.echo("")

    if not input:
        input = (".")

    for folder in input:

        if os.path.isdir(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if (file.lower().endswith(".png")) or (file.lower().endswith(".jpg")) or (file.lower().endswith(".jpeg")):
                        click.echo("Image: %s" % file)
                        update_progress(0)
                        try:
                            img_path = os.path.join(root, file)
                            size = os.path.getsize(img_path)
                            new_img = tinify.from_file(img_path)
                            update_progress(.5)
                            new_img.to_file(img_path)
                            new_size = os.path.getsize(img_path)
                            one = size / 100
                            saved = size - new_size
                            percent = saved / one
                            update_progress(1)
                            click.echo("Saved: %s%% \n" % round(percent))
                            pass
                        except(tinify.AccountError):
                            click.echo("✘ Verify your API key and account limit. \n")
                        except(tinify.ClientError):
                            click.echo("✘ File could not be processed \n")
                            pass
                        except(tinify.ServerError):
                            click.echo("✘ Temporary issue with the Tinify API. \n")
                            pass
                        except(tinify.ConnectionError):
                            click.echo("✘ A network connection error occurred. \n")
                            pass
                        except(Exception):
                            click.echo("✘ Something went wrong \n")
                            pass

        elif os.path.isfile(folder):
            if (folder.lower().endswith(".png")) or (folder.lower().endswith(".jpg")) or (folder.lower().endswith(".jpeg")):
                click.echo(folder)
                update_progress(0)
                try:
                    size = os.path.getsize(folder)
                    new_img = tinify.from_file(folder)
                    update_progress(.5)
                    new_img.to_file(folder)
                    new_size = os.path.getsize(folder)
                    one = size / 100
                    saved = size - new_size
                    percent = saved / one
                    update_progress(1)
                    click.echo("Saved: %s%% \n" % round(percent))
                    pass
                except(tinify.AccountError):
                    click.echo("✘ Verify your API key and account limit. \n")
                except(tinify.ClientError):
                    click.echo("✘ File could not be processed \n")
                    pass
                except(tinify.ServerError):
                    click.echo("✘ Temporary issue with the Tinify API. \n")
                    pass
                except(tinify.ConnectionError):
                    click.echo("✘ A network connection error occurred. \n")
                    pass
                except(Exception):
                    click.echo("✘ Something went wrong \n")
                    pass

        else:
            click.echo("%s is not a file or folder.\n" % folder)