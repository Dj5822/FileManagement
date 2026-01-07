import typer

from .extend import app as extend
from .merge import app as merge
from .rename import app as rename

app = typer.Typer()

app.add_typer(extend)
app.add_typer(merge)
app.add_typer(rename)
