"""Define the measure models."""
from statistics import mean

from pydantic import dataclasses


@dataclasses.dataclass
class City:
    """Define the city model."""

    name: str
    country: str
    population: int
    rating: int
    state: str = str()

    def as_short_code_dict(self):
        """
        Convert a City to a dict using short code fields.

        Example:
            >>> c = City("Portland", "USA", 645291, 54, "OR")
            >>> c.as_short_code_dict()
            {'ci': 'Portland', 'co': 'USA', 'po': 645291, 'score': 54, 'st': 'OR'}

        """

        return {
            "ci": self.name,
            "co": self.country,
            "po": self.population,
            "score": self.rating,
            "st": self.state,
        }


@dataclasses.dataclass
class NetworkAnalysis:
    """Define the Network Analysis model."""

    neighborhood: int = 0
    opportunity: int = 0
    essential_services: int = 0
    recreation: int = 0
    retail: int = 0
    transit: int = 0

    def score(self):
        """
        Return the Network Analysis score.

        The score is the rounded mean value of the sum of all the fields.

        Example:
            >>> na = NetworkAnalysis(
                neighborhood=55,
                opportunity=51,
                essential_services=53,
                recreation=58,
                retail=57,
                transit=34,
                )
            >>> na.score()
            51

        """
        return round(mean(getattr(self, field) for field in self.__dataclass_fields__))

    def as_short_code_dict(self):
        """
        Convert a Network Analysis to a dict using short code fields.

        Example:
            >>> na = NetworkAnalysis(
                neighborhood=55,
                opportunity=51,
                essential_services=53,
                recreation=58,
                retail=57,
                transit=34,
                )
            >>> na.as_short_code_dict()
            {'nh': 55, 'op': 51, 'es': 53, 'rec': 58, 'ret': 57, 'tr': 34}

        """
        return {
            "nh": self.neighborhood,
            "op": self.opportunity,
            "es": self.essential_services,
            "rec": self.recreation,
            "ret": self.retail,
            "tr": self.transit,
        }


@dataclasses.dataclass
class CommunitySurvey:
    """Define the Community Survey model."""

    awareness: int = 0
    network: int = 0
    safety: int = 0
    ridership: int = 0

    def score(self):
        """
        Return the Community Survey score.

        The score is the rounded mean value of the sum of all the fields.

        Example:
            >>> cs = CommunitySurvey(
                awareness=63,
                network=68,
                safety=46,
                ridership=78,
                )
            >>> cs.score()
            64

        """
        return round(mean(getattr(self, field) for field in self.__dataclass_fields__))

    def as_short_code_dict(self):
        """
        Convert a Community Survey to a dict using short code fields.

        Example:
            >>> cs = CommunitySurvey(
                awareness=63,
                network=68,
                safety=46,
                ridership=78,
                )
            >>> cs.as_short_code_dict()
            {'aw': 63, 'nw': 68, 'sf': 46, 'rs': 78}

        """
        return {
            "aw": self.awareness,
            "nw": self.network,
            "sf": self.safety,
            "rs": self.ridership,
        }


@dataclasses.dataclass
class ProtectedInfrastructure:
    """Define the Protected Infrastructure model."""

    lanes: int = 0
    off_street_paths: int = 0

    def mileage(self):
        """
        Return the Protected Infrastructure mileage.

        The mileage is the sum of all the fields.

        Example:
            >>> pi = ProtectedInfrastructure(
                lanes=10,
                off_street_paths=20,
             )
            >>> pi.mileage()
            30

        """
        return sum(getattr(self, field) for field in self.__dataclass_fields__)

    def as_short_code_dict(self):
        """
        Convert a Protected Infrastructure to a dict using short code fields.

        Example:
            >>> pi = ProtectedInfrastructure(
                lanes=10,
                off_street_paths=20,
                )
            >>> pi.as_short_code_dict()
            {'la': 10, 'osp': 20}

        """
        return {
            "la": self.lanes,
            "osp": self.off_street_paths,
        }


@dataclasses.dataclass
class UnprotectedInfrastructure:
    """Define the Unprotected Infrastructure model."""

    low_stress_lanes: int = 0
    low_stress_buffered_lanes: int = 0

    def mileage(self):
        """
        Return the Protected Infrastructure mileage.

        The mileage is the sum of all the fields.

        Example:
            >>> ui = UnprotectedInfrastructure(
                low_stress_lanes=35,
                low_stress_buffered_lanes=5,
                )
            >>> ui.mileage()
            40

        """
        return sum(getattr(self, field) for field in self.__dataclass_fields__)

    def as_short_code_dict(self):
        """
        Convert a Unprotected Infrastructure to a dict using short code fields.

        Example:
            >>> ui = UnprotectedInfrastructure(
                low_stress_lanes=35,
                low_stress_buffered_lanes=5,
                )
            >>> ui.as_short_code_dict()
            {'lsl': 35, 'lsbl': 5}

        """
        return {
            "lsl": self.low_stress_lanes,
            "lsbl": self.low_stress_buffered_lanes,
        }


@dataclasses.dataclass
class Infrastructure:
    """Define Infrastructure model."""

    protected: ProtectedInfrastructure
    unprotected: UnprotectedInfrastructure

    def mileage(self):
        """
        Return the Protected Infrastructure mileage.

        The mileage is the sum of all the fields.

        Example:
            >>> i = Infrastructure(
                ProtectedInfrastructure(
                    lanes=10,
                    off_street_paths=20,
                ),
                UnprotectedInfrastructure(
                    low_stress_lanes=35,
                    low_stress_buffered_lanes=5,
                ),
                )
            >>> i.mileage()
            70

        """
        return sum([self.protected.mileage(), self.unprotected.mileage()])

    def as_short_code_dict(self):
        """
        Convert an Infrastructure to a dict using short code fields.

        Example:
            >>> i = Infrastructure(
                ProtectedInfrastructure(
                    lanes=10,
                    off_street_paths=20,
                ),
                UnprotectedInfrastructure(
                    low_stress_lanes=35,
                    low_stress_buffered_lanes=5,
                ),
                )
            >>> i.as_short_code_dict()
            {'pi': {'la': 10, 'osp': 20}, 'ui': {'lsl': 35, 'lsbl': 5}}

        """
        return {
            "pi": self.protected.as_short_code_dict(),
            "ui": self.unprotected.as_short_code_dict(),
        }


@dataclasses.dataclass
class ScoreCard:
    """Define Score Card model."""

    city: City
    network_analysis: NetworkAnalysis
    community_survey: CommunitySurvey
    infrastructure: Infrastructure

    def as_short_code_dict(self):
        """
        Convert a Score Card to a dict using short code fields.

        Example:
            >>> s = ScoreCard(
                    City("Portland", "USA", 645291, 54, "OR"),
                    NetworkAnalysis(
                        neighborhood=55,
                        opportunity=51,
                        essential_services=53,
                        recreation=58,
                        retail=57,
                        transit=34,
                    ),
                    CommunitySurvey(
                        awareness=63,
                        network=68,
                        safety=46,
                        ridership=78,
                    ),
                    Infrastructure(
                        ProtectedInfrastructure(
                            lanes=10,
                            off_street_paths=20,
                        ),
                        UnprotectedInfrastructure(
                            low_stress_lanes=35,
                            low_stress_buffered_lanes=5,
                        ),
                    )
                )
            >>> s.as_short_code_dict()
            {'ci': 'Portland', 'co': 'USA', 'po': 645291, 'score': 54, 'st': 'OR',
            'nh': 55, 'op': 51, 'es': 53, 'rec': 58, 'ret': 57, 'tr': 34, 'aw': 63,
            'nw': 68, 'sf': 46, 'rs': 78, 'pi': {'la': 10, 'osp': 20},
            'ui': {'lsl': 35, 'lsbl': 5}}

        """
        return {
            **self.city.as_short_code_dict(),
            **self.network_analysis.as_short_code_dict(),
            **self.community_survey.as_short_code_dict(),
            **self.infrastructure.as_short_code_dict(),
        }
