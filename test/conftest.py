from enum import Enum

import pytest
from sqlalchemy.orm.exc import NoResultFound

import fire.cli
from fire.api import FireDb
from fire.api.model import (
    func,
    Sag,
    Punkt,
    PunktGruppe,
    Observation,
    Sagsevent,
    SagseventInfo,
    Sagsinfo,
    Beregning,
    Koordinat,
    EventType,
    Srid,
    Boolean,
)
from fire.io.regneark import (
    arkdef,
    nyt_ark,
    basisrække,
)


class DummyFireDb(FireDb):
    """
    FireDb klasse der bruges i tests hvor databaseudtræk med
    API-funktioner mockes.
    """

    def __init__(self, connectionstring=None, debug=False):
        self._cache = {
            "punkt": {},
            "punktinfotype": {},
        }


persistent_firedb = FireDb(db="ci", debug=False)
fire.cli.override_firedb(persistent_firedb)


@pytest.fixture
def firedb():
    return persistent_firedb


@pytest.fixture
def dummydb():
    return DummyFireDb()


@pytest.fixture()
def sag(firedb):
    s0 = Sag()
    si0 = Sagsinfo(sag=s0, aktiv=Boolean.TRUE, behandler="yyy")
    firedb.session.add(si0)
    firedb.session.add(s0)
    firedb.session.flush()
    return s0


# @pytest.fixture()
# def sagsevent(firedb, sag):
#     e0 = Sagsevent(sag=sag, eventtype=EventType.KOMMENTAR)
#     firedb.session.add(e0)
#     return e0


@pytest.fixture()
def sagsevent(sagseventfabrik):
    return sagseventfabrik()


@pytest.fixture()
def sagseventfabrik(firedb, sag):
    """Sagseventfabrik til oprettelse af flere sagevents i samme test case."""

    def fabrik():
        e0 = Sagsevent(
            sag=sag,
            eventtype=EventType.KOMMENTAR,
            sagseventinfos=[SagseventInfo(beskrivelse="test")],
        )
        firedb.session.add(e0)
        return e0

    return fabrik


@pytest.fixture()
def punktfabrik(firedb, sagsevent: Sagsevent):
    """Punktfabrik til oprettelse af flere punkter i samme test case."""

    def fabrik():
        sagsevent.eventtype = EventType.PUNKT_OPRETTET
        p = Punkt(sagsevent=sagsevent)
        firedb.session.add(p)
        return p

    return fabrik


@pytest.fixture()
def punkt(punktfabrik):
    return punktfabrik()


@pytest.fixture()
def punktgruppe(firedb, sagsevent, punktfabrik):
    sagsevent.eventtype = EventType.PUNKTGRUPPE_MODIFICERET
    pg = PunktGruppe(
        sagsevent=sagsevent,
        navn=f"test-{fire.uuid()[0:9]}",
        jessenpunkt=punktfabrik(),
        punkter=[punktfabrik() for _ in range(5)],
    )
    return pg


@pytest.fixture()
def koordinat(firedb, sagsevent, punkt, srid):
    sagsevent.eventtype = EventType.KOORDINAT_BEREGNET
    k0 = Koordinat(
        sagsevent=sagsevent,
        punkt=punkt,
        srid=srid,
        x=0,
        y=0,
        z=0,
        sx=0,
        sy=0,
        sz=0,
    )
    firedb.session.add(k0)
    return k0


@pytest.fixture()
def observationstype(firedb):
    ot0 = firedb.hent_observationstype("nulobservation")
    return ot0


@pytest.fixture()
def observation(firedb, sagsevent, observationstype, punkt):
    sagsevent.eventtype = EventType.OBSERVATION_INDSAT
    o0 = Observation(
        sagsevent=sagsevent,
        observationstidspunkt=func.current_timestamp(),
        observationstype=observationstype,
        opstillingspunkt=punkt,
        antal=1,
    )
    firedb.session.add(o0)
    return o0


@pytest.fixture()
def observationer(firedb, sagsevent, observationstype, punkt):
    sagsevent.eventtype = EventType.OBSERVATION_INDSAT
    o0 = Observation(
        sagsevent=sagsevent,
        observationstidspunkt=func.current_timestamp(),
        observationstype=observationstype,
        opstillingspunkt=punkt,
    )
    o1 = Observation(
        sagsevent=sagsevent,
        observationstidspunkt=func.current_timestamp(),
        observationstype=observationstype,
        opstillingspunkt=punkt,
    )
    firedb.session.add(o0)
    firedb.session.add(o1)
    return [o0, o1]


@pytest.fixture()
def beregning(firedb, sagsevent, koordinat, observationer):
    sagsevent.eventtype = EventType.KOORDINAT_BEREGNET
    b0 = Beregning(
        sagsevent=sagsevent, observationer=observationer, koordinater=[koordinat]
    )
    firedb.session.add(b0)
    return b0


@pytest.fixture()
def srid(firedb):
    try:
        srid = firedb.hent_srid("DK:TEST")
    except NoResultFound:
        firedb.indset_srid(
            Srid(
                name="DK:TEST",
                beskrivelse="SRID til brug i test-suite",
                x="Easting",
                y="Northing",
                z="Højde",
            )
        )
        srid = firedb.hent_srid("DK:TEST")
    return srid


@pytest.fixture()
def punktinformationtype(firedb):
    pi = firedb.hent_punktinformationtype("ATTR:test")

    return pi


@pytest.fixture
def identer_gyldige():
    return (
        "125-03-09001",
        "125-03-09003",
    )


@pytest.fixture
def identer_ugyldige():
    return (
        "ikke-en-ident",
        "f-o-o-b-a-r",
    )


@pytest.fixture
def geojson_rectangle():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10.073776245117188, 56.0900440736966],
                            [10.286636352539062, 56.0900440736966],
                            [10.286636352539062, 56.224649602556184],
                            [10.073776245117188, 56.224649602556184],
                            [10.073776245117188, 56.0900440736966],
                        ]
                    ],
                },
            }
        ],
    }


@pytest.fixture
def ark_punktoversigt():
    return nyt_ark(arkdef.PUNKTOVERSIGT)


@pytest.fixture
def række_punktoversigt():
    return basisrække(arkdef.PUNKTOVERSIGT)


@pytest.fixture
def enumeration():
    class Enumeration(Enum):
        medlem1 = 1
        alias1 = 1
        medlem2 = 2
        alias2 = 2
        medlem3 = "test"
        alias3 = "test"
        medlem4 = "bob"
        alias4 = "bob"

    return Enumeration
