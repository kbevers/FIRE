Beregning uden sagsoprettelse i database
-----------------------------------------

.. code-block:: none

    > fire niv opret-sag beregning

    # Sig først nej, så ja

    > fire niv udtræk-observationer beregning <punkt1> <punkt2> ...

    # Åben regneark og angiv fastholdte punkter

    > fire niv regn beregning
    > fire niv regn beregning



.. code-block:: none

    > fire niv opret-sag beregning "Beregning uden at oprette sag i databasen"                                      [22:36:32]
    Sags/projekt-navn: beregning  (b3f0521a-c51f-432c-91b4-6d33ff7582a6)
    Sagsbehandler:     kevers
    Beskrivelse:
    Opretter ny sag i test-databasen - er du sikker?  (ja/NEJ):
    nej
    Opretter IKKE sag
    Opret sagsregneark alligevel? (ja/NEJ):
    ja
    Skriver sagsregneark 'beregning.xlsx'
    Filen 'beregning.xlsx' findes ikke.
    Skriver: {'Nyetablerede punkter', 'Filoversigt', 'Notater', 'Sagsgang', 'Parametre', 'Projektforside'}
    Til filen 'beregning.xlsx'


.. code-block:: none

    > fire niv udtræk-observationer beregning K-63-09451 K-63-00909 K-63-09145 K-63-09300 K-63-05436
    Klargør identer
    Søg i databasen efter punkter til hver ident
    Søg med punkterne som opstillingspunkt
    /Users/kevers/dev/FIRE/fire/api/firedb/hent.py:241: SAWarning: SELECT statement has a cartesian product between FROM element(s) "koordinat_1" and FROM element "observation".  Apply join condition(s) between each element to resolve.
    return query.all()
    Filtrér observationer
    Indsaml opstillingspunkter fra observationer
    Gem observationer og punkter i projekt-regnearket
    Check: Punktoversigt har alle punkter i Observationer[Fra]: Ja
    Skriver til /Users/kevers/dev/FIRE/shit/beregning.xlsx...
    Gem punkter som .geojson-fil...
    Skriver punkter til beregning-2022-02-17T223959.geojson ...

