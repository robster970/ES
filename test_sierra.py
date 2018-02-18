# test_capitalize.py
from sierra_importer import Importer


# sierra_importer tests
def test_file_attributes():
    working_directory = "/home/robster970/repo/e-mini/sierrafiles/"
    file_name = "ESH18.dly_BarData.txt"
    column_id = "TEST"
    assert Importer(working_directory, file_name, column_id)