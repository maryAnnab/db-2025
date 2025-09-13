import uuid

from pydantic import BaseModel


class AircraftPart(BaseModel):
    id: uuid
    name: str
    # constraints

    # usage
    hours_since_overhaul: int
    flights_since_overhaul: int

    # max values
    max_flights: int
    max_hours: int

    parent_part_id: uuid



# subparts: list[uuid]
"""
create table subparts(
  part_id uuid references aircraft_parts(id),
  subpart_id uuid references aircraft_parts(id)
)

"""


