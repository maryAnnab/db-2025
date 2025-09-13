from db_2025.u2.migrations.model import Migration

migrations = [
    Migration(
        start_version=1,
        produces_version=2,
        description='create initial table users',
        up_sql="""
        
CREATE TABLE aircraft_parts (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    hours_since_overhaul INTEGER NOT NULL DEFAULT 0,
    flights_since_overhaul INTEGER NOT NULL DEFAULT 0,
    max_flights INTEGER NOT NULL,
    max_hours INTEGER NOT NULL,
    parent_part_id UUID,
    
    CONSTRAINT fk_parent_part 
        FOREIGN KEY (parent_part_id) 
        REFERENCES aircraft_parts(id) 
        ON DELETE CASCADE
);

    """,
        down_sql="""
        drop table aircraft_parts;
        """,
    ),
    Migration(start_version=2, produces_version=3, description='create tables for aircraft and flights',
              up_sql="""
CREATE TABLE airport (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    country_alpha_3 CHAR(3) NOT NULL,
    iata_code CHAR(3),
    icao_code CHAR(4),
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL
);

CREATE TABLE aircraft (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    msn TEXT NOT NULL,
    icao_code CHAR(4) NOT NULL,
    original_manufacturer TEXT NOT NULL,
    registration TEXT NOT NULL,
    country_reg CHAR(3) NOT NULL,
    age INTEGER NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE flight (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aircraft_id UUID NOT NULL REFERENCES aircraft(id) ON DELETE CASCADE ON UPDATE CASCADE,
    call_sign TEXT NOT NULL,
    departure_ts TIMESTAMP NOT NULL,
    departure_airport_id UUID REFERENCES airport(id) ON DELETE CASCADE ON UPDATE CASCADE,
    landing_ts TIMESTAMP NOT NULL,
    destination_airport_id UUID REFERENCES airport(id) ON DELETE CASCADE ON UPDATE CASCADE,
    flight_hours NUMERIC(6,1) NOT NULL
);
              
              """,
              down_sql="""
DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS airport;
DROP TABLE IF EXISTS aircraft;
              """),
]

