import typer

app = typer.Typer()

@app.command()
def greet():
    """
    Greets a person
    """
    typer.echo(f"greet function")

@app.command()
def farewell():
    """
    Says a general farewell.
    """
    typer.echo("farewell function")

if __name__ == "__main__":
    app()
