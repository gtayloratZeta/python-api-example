import os 
from pyairtable import Api

API_TOKEN = os.environ.get('AIRTABLE_TOKEN')

BASE_ID = 'appi1uzlLKn1TEKSw'
TABLE_ID = 'tblvMMAVHo901m2Ra'

api = Api(API_TOKEN)

table = api.table(BASE_ID, TABLE_ID)

def get_all_records(count=None, sort=None):
    """
    Retreives all records from a database table, optionally sorting them by the
    'Rating' column in ascending or descending order, and limiting the result to
    a specified number of records.

    Args:
        count (int | None): Optional. When specified, it limits the number of
            records returned from the database to the specified count.
        sort (str | None): Optional. It accepts either 'ASC' or 'DESC' as valid
            values to sort the records. If 'ASC', the records are sorted in ascending
            order by the 'Rating' column. If 'DESC', the records are sorted in
            descending order by the 'Rating' column.

    Returns:
        List[Dict[str,Any]]: A list of dictionaries representing database table records.

    """
    sort_param = []
    if sort and sort.upper()=='DESC':
        sort_param = ['-Rating']
    elif sort and sort.upper()=='ASC':
        sort_param = ['Rating']

    return table.all(max_records=count, sort=sort_param)

def get_record_id(name):
    return table.first(formula=f"Book='{name}'")['id']

def update_record(record_id, data):
    """
    Updates a database record with the specified `record_id` by applying the
    provided `data` to it. It uses the `table.update` method, presumably part of
    an object-relational mapping (ORM) system, to perform the update operation.

    Args:
        record_id (int): Used to specify the unique identifier of the record in
            the database that needs to be updated.
        data (Dict[str, Any]): Passed to the `table.update` method to update the
            record with the specified `record_id`.

    Returns:
        bool: True, indicating successful execution of the function.

    """
    table.update(record_id, data)

    return True

def add_record(data):
    """
    Checks if a dictionary contains 'Book' and 'Rating' keys. If present, it creates
    a table with the provided data and returns True, indicating a successful
    operation. Otherwise, it returns False.

    Args:
        data (Dict[str, str | int]): Expected to contain at least two key-value
            pairs: 'Book' and 'Rating'.

    Returns:
        bool: True if the record is successfully added to the database and False
        otherwise, specifically when the required keys 'Book' or 'Rating' are
        missing from the data.

    """
    # require data contains a "Book" key and a "Rating" key (data is a dict)
    if 'Book' not in data or 'Rating' not in data:
        return False

    table.create(data)
    return True

if __name__ == '__main__':
    ## Show getting certain records
    print("Show getting certain records")
    print(table.all(formula="Rating < 5", sort=['-Rating']))

    ## Show getting a single record
    print("Show getting a single record")

    # Replace a record
    print("Replace a record")
    name = "Test Message"
    record_id = table.first(formula=f"Book='{name}'")['id']
    table.update(record_id, {"Rating": 5})

    ## Show all records
    print("All records!")
    print(table.all())