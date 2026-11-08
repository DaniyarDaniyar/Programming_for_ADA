from db import get_connection
from queries import (
    delete_appointment_diagnosis,
    run_select_queries,
    update_patient,
)


def main():
    with get_connection() as connection:
        run_select_queries(connection)
        update_patient(connection)
        delete_appointment_diagnosis(connection)


if __name__ == "__main__":
    main()
