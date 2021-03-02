from mysql.connector import connect, Error

def execute(query, *args):
    """
    General method for executing queries on the database. Queries can be passed with a list of tuples for multiple
    INSERT statements. All non-INSERT queries should be passed preconfigured and
    ready to execute.

    Parameters
    ----------
    query : str
        The query to be executed
    args : list[tuple]
        OPTIONAL list of tuples to be inserted
        NOTE: only to be passed for INSERT statements

    Returns
    -------
    list[tuple]
        This list contains the query results, if any.
        NOTE: This will return None for all none-SELECT queries and SELECT queries that return no results.
    """

    standard_execution = True if len(args) < 1 else False
    try:
        with connect(
                host="localhost",
                user="root",
                password="Password1234",
                database="csaia_database",
        ) as connection:
            ids = []

            with connection.cursor() as cursor:
                if standard_execution:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if len(result) > 0:
                        return result
                else:
                    for arg in args[0]:
                        cursor.execute(query, arg)
                        ids.append(cursor.lastrowid)
                        
            connection.commit()

            return ids

    except Error as e:
        print(e)
