# crud stands for create read update and delete model w.r.t databases
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="hello1234"
)

connection.autocommit = True
def login_(email, password):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email=%s
        AND password=%s
        """,
        (email, password)
    )
    user = cursor.fetchone()

    cursor.close()

    return user is not None


def register_(email, password):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    if cursor.fetchone():
        cursor.close()
        return False

    cursor.execute(
        """
        INSERT INTO users(email,password)
        VALUES(%s,%s)
        """,
        (email, password)
    )

    cursor.close()

    return True


def clock_out_(email, clock_in, clock_out):
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO timelog(email, clock_in, clock_out)
        VALUES(%s,%s,%s)
        """,
        (email, clock_in, clock_out)
    )

    cursor.close()

    return True