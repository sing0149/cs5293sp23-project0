from project0.project0 import fetchincidents, createdb, extractincidents, populatedb, status
import pytest
import sys
from io import StringIO


def test_fetchincidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2023-02/2023-02-01_daily_incident_summary.pdf"
    binary_data = fetchincidents(url)
    assert isinstance(binary_data, bytes)
    assert len(binary_data) > 0


def test_extractincidents():
    binary_data = fetchincidents("https://www.normanok.gov/sites/default/files/documents/2023-02/2023-02-01_daily_incident_summary.pdf")
    processed_data = extractincidents(binary_data)
    assert isinstance(processed_data, list)
    assert len(processed_data) >= 0
    for data in processed_data:
        assert isinstance(data, list)
        assert len(data) == 5


def test_createdb():
    db = createdb()
    assert db is not None
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "incidents"


def test_populatedb():
    db = createdb()
    processed_data = [['02/25/2022 23:52', '2022-00005172', '2200 NW 56TH ST', '911 CALL / GENERA', 'OK0190300'],
                      ['02/26/2022 00:26', '2022-00005173', '928 12TH AVE NE', 'NOISE VIOLATION', 'OK0190300']]
    populatedb(db, processed_data)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM incidents WHERE incident_number='2022-00005172'")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == '02/25/2022 23:52'
    assert result[1] == '2022-00005172'
    assert result[2] == '2200 NW 56TH ST'
    assert result[3] == '911 CALL / GENERA'
    assert result[4] == 'OK0190300'


def test_status():
    db = createdb()
    processed_data = [['02/25/2022 23:52', '2022-00005172', '2200 NW 56TH ST', '911 CALL / GENERA', 'OK0190300'],
                      ['02/26/2022 00:26', '2022-00005173', '928 12TH AVE NE', 'NOISE VIOLATION', 'OK0190300'],
                      ['02/26/2022 00:30', '2022-00005174', '1016 MCGEE DR', '911 HANG UP / MISD', 'OK0190300']]
    populatedb(db, processed_data)
    captured_output = StringIO()
    sys.stdout = captured_output
    status
