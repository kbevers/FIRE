import os
import os.path
from io import BytesIO
from zipfile import ZipFile

import click
import pandas as pd
import sys

from fire import uuid
import fire.cli

from fire.api.model import (
    Sagsevent,
    SagseventInfo,
    SagseventInfoMateriale,
    EventType,
)


from . import (
    ARKDEF_PARAM,
    ARKDEF_FILOVERSIGT,
    find_faneblad,
    find_sag,
    niv,
    bekræft,
)


@niv.command()
@fire.cli.default_options()
@click.argument(
    "projektnavn",
    nargs=1,
    type=str,
)
def luk_sag(projektnavn: str, **kwargs) -> None:
    """Luk sag i databasen"""
    sag = find_sag(projektnavn)

    # Find sagsmateriale og zip det for let indlæsning i databasen
    sagsmaterialer = [f"{projektnavn}.xlsx"]
    filoversigt = find_faneblad(projektnavn, "Filoversigt", ARKDEF_FILOVERSIGT)
    sagsmaterialer.extend(list(filoversigt["Filnavn"]))
    zipped = BytesIO()
    with ZipFile(zipped, "w") as zipobj:
        for fil in sagsmaterialer:
            zipobj.write(fil)

    # Tilføj materiale til sagsevent
    sagsevent = Sagsevent(
        sag=sag,
        eventtype=EventType.KOMMENTAR,
        sagseventinfos=[
            SagseventInfo(
                beskrivelse=f"Sagsmateriale for {projektnavn}",
                materialer=[SagseventInfoMateriale(materiale=zipped.getvalue())],
            ),
        ],
    )
    fire.cli.firedb.indset_sagsevent(sagsevent, commit=False)

    fire.cli.firedb.luk_sag(sag, commit=False)
    try:
        # Indsæt alle objekter i denne session
        fire.cli.firedb.session.flush()
    except:
        # rul tilbage hvis databasen smider en exception
        fire.cli.firedb.session.rollback()
        fire.cli.print(
            f"Der opstod en fejl - sag {sag.id} for '{projektnavn}' IKKE lukket!"
        )
    else:
        spørgsmål = click.style(
            "Er du sikker på at du vil lukke sagen {projektnavn}?", bg="red", fg="white"
        )
        if bekræft(spørgsmål):
            fire.cli.firedb.session.commit()
            fire.cli.print(f"Sag {sag.id} for '{projektnavn}' lukket!")
        else:
            fire.cli.firedb.session.rollback()
            fire.cli.print(f"Sag {sag.id} for '{projektnavn}' IKKE lukket!")
