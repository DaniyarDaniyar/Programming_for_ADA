from datetime import date, time, timedelta

from db import get_connection


ROW_COUNT = 100


def insert_and_return_ids(cursor, query, rows):
    ids = []
    for row in rows:
        ids.append(cursor.execute(query, row).fetchone()[0])
    return ids


def generate_data():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            specialization_ids = insert_and_return_ids(
                cursor,
                """
                INSERT INTO specializations (name, description)
                VALUES (%s, %s)
                RETURNING specialization_id
                """,
                [
                    (
                        f"Specialization {index}",
                        f"Medical specialization number {index}",
                    )
                    for index in range(1, ROW_COUNT + 1)
                ],
            )

            department_ids = insert_and_return_ids(
                cursor,
                """
                INSERT INTO departments (name, floor, phone)
                VALUES (%s, %s, %s)
                RETURNING department_id
                """,
                [
                    (
                        f"Department {index}",
                        (index - 1) % 10 + 1,
                        f"+7701000{index:04d}",
                    )
                    for index in range(1, ROW_COUNT + 1)
                ],
            )

            patient_ids = insert_and_return_ids(
                cursor,
                """
                INSERT INTO patients (
                    first_name, last_name, date_of_birth, gender, phone,
                    address, blood_type, insurance_number
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING patient_id
                """,
                [
                    (
                        f"Patient{index}",
                        f"Lastname{index}",
                        date(1970, 1, 1) + timedelta(days=index * 100),
                        "Male" if index % 2 else "Female",
                        f"+7702000{index:04d}",
                        f"{index} Main Street",
                        ("A+", "A-", "B+", "B-", "AB+", "O+")[index % 6],
                        f"INS-{index:06d}",
                    )
                    for index in range(1, ROW_COUNT + 1)
                ],
            )

            insert_and_return_ids(
                cursor,
                """
                INSERT INTO patient_medical_records (
                    patient_id, registration_date, allergies,
                    chronic_conditions, emergency_contact
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING medical_record_id
                """,
                [
                    (
                        patient_id,
                        date(2024, 1, 1) + timedelta(days=index),
                        "None" if index % 3 else "Pollen",
                        "None" if index % 4 else "Asthma",
                        f"+7703000{index:04d}",
                    )
                    for index, patient_id in enumerate(patient_ids, start=1)
                ],
            )

            doctor_ids = insert_and_return_ids(
                cursor,
                """
                INSERT INTO doctors (
                    first_name, last_name, specialization_id, phone,
                    email, license_number, hire_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING doctor_id
                """,
                [
                    (
                        f"Doctor{index}",
                        f"Lastname{index}",
                        specialization_ids[index - 1],
                        f"+7704000{index:04d}",
                        f"doctor{index}@hospital.example",
                        f"LIC-{index:06d}",
                        date(2015, 1, 1) + timedelta(days=index * 30),
                    )
                    for index in range(1, ROW_COUNT + 1)
                ],
            )

            cursor.executemany(
                """
                INSERT INTO doctor_departments (
                    doctor_id, department_id, position, start_date
                )
                VALUES (%s, %s, %s, %s)
                """,
                [
                    (
                        doctor_id,
                        department_ids[index - 1],
                        "Physician" if index % 3 else "Head physician",
                        date(2016, 1, 1) + timedelta(days=index * 20),
                    )
                    for index, doctor_id in enumerate(doctor_ids, start=1)
                ],
            )

            diagnosis_ids = insert_and_return_ids(
                cursor,
                """
                INSERT INTO diagnoses (name, description)
                VALUES (%s, %s)
                RETURNING diagnosis_id
                """,
                [
                    (
                        f"Diagnosis {index}",
                        f"Diagnosis description {index}",
                    )
                    for index in range(1, ROW_COUNT + 1)
                ],
            )

            appointment_ids = insert_and_return_ids(
                cursor,
                """
                INSERT INTO appointments (
                    patient_id, doctor_id, appointment_date,
                    appointment_time, reason, status, notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING appointment_id
                """,
                [
                    (
                        patient_ids[index - 1],
                        doctor_ids[index - 1],
                        date(2025, 1, 1) + timedelta(days=index),
                        time(9 + index % 8, 0),
                        f"Routine consultation {index}",
                        ("Scheduled", "Completed", "Cancelled")[index % 3],
                        f"Appointment notes {index}",
                    )
                    for index in range(1, ROW_COUNT + 1)
                ],
            )

            cursor.executemany(
                """
                INSERT INTO appointment_diagnoses (
                    appointment_id, diagnosis_id, diagnosis_type
                )
                VALUES (%s, %s, %s)
                """,
                [
                    (
                        appointment_id,
                        diagnosis_ids[index - 1],
                        "Primary" if index % 2 else "Secondary",
                    )
                    for index, appointment_id in enumerate(appointment_ids, start=1)
                ],
            )


if __name__ == "__main__":
    generate_data()
    print("Inserted 100 rows into each table.")