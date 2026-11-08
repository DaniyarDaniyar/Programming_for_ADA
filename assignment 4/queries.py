QUERIES = {
    "simple_1": """
        SELECT first_name, last_name, gender, blood_type, phone, address
        FROM patients
        WHERE gender = 'Female'
    """,
    "simple_2": """
        SELECT first_name, last_name, hire_date, phone, email
        FROM doctors
        WHERE hire_date >= DATE '2020-01-01'
    """,
    "join_2_tables_1": """
        SELECT p.first_name, p.last_name, p.phone,
               r.registration_date, r.allergies,
               r.chronic_conditions, r.emergency_contact
        FROM patients AS p
        JOIN patient_medical_records AS r ON r.patient_id = p.patient_id
    """,
    "join_2_tables_2": """
        SELECT d.first_name, d.last_name, s.name AS specialization,
               d.phone, d.email, d.hire_date
        FROM doctors AS d
        JOIN specializations AS s
          ON s.specialization_id = d.specialization_id
    """,
    "join_3_tables_1": """
        SELECT p.first_name || ' ' || p.last_name AS patient,
               d.first_name || ' ' || d.last_name AS doctor,
               a.appointment_date, a.appointment_time,
               a.reason, a.status, a.notes
        FROM appointments AS a
        JOIN patients AS p ON p.patient_id = a.patient_id
        JOIN doctors AS d ON d.doctor_id = a.doctor_id
    """,
    "join_3_tables_2": """
        SELECT d.first_name || ' ' || d.last_name AS doctor,
               s.name AS specialization, dd.position, dd.start_date,
               dep.name AS department
        FROM doctors AS d
        JOIN specializations AS s
          ON s.specialization_id = d.specialization_id
        JOIN doctor_departments AS dd ON dd.doctor_id = d.doctor_id
        JOIN departments AS dep ON dep.department_id = dd.department_id
    """,
    "group_by_1": """
        SELECT s.name AS specialization, COUNT(a.appointment_id) AS appointments
        FROM specializations AS s
        JOIN doctors AS d ON d.specialization_id = s.specialization_id
        JOIN appointments AS a ON a.doctor_id = d.doctor_id
        GROUP BY s.specialization_id, s.name
    """,
    "group_by_2": """
        SELECT dep.name AS department, d.last_name AS doctor,
               COUNT(dd.doctor_id) AS assignments
        FROM departments AS dep
        JOIN doctor_departments AS dd ON dd.department_id = dep.department_id
        JOIN doctors AS d ON d.doctor_id = dd.doctor_id
        GROUP BY dep.department_id, dep.name, d.doctor_id, d.last_name
    """,
    "having_1": """
        SELECT d.first_name || ' ' || d.last_name AS doctor,
               COUNT(a.appointment_id) AS total
        FROM doctors AS d
        JOIN appointments AS a ON a.doctor_id = d.doctor_id
        JOIN patients AS p ON p.patient_id = a.patient_id
        GROUP BY d.doctor_id, d.first_name, d.last_name
        HAVING COUNT(a.appointment_id) >= 1
    """,
    "having_2": """
        SELECT s.name AS specialization, COUNT(d.doctor_id) AS doctors
        FROM specializations AS s
        JOIN doctors AS d ON d.specialization_id = s.specialization_id
        JOIN doctor_departments AS dd ON dd.doctor_id = d.doctor_id
        GROUP BY s.specialization_id, s.name
        HAVING COUNT(DISTINCT d.doctor_id) > 0
    """,
    "order_by_1": """
        SELECT p.last_name AS patient, a.appointment_date, a.status
        FROM patients AS p
        JOIN appointments AS a ON a.patient_id = p.patient_id
        ORDER BY a.appointment_date DESC, p.last_name ASC
    """,
    "order_by_2": """
        SELECT d.last_name AS doctor, s.name AS specialization, d.hire_date
        FROM doctors AS d
        JOIN specializations AS s
          ON s.specialization_id = d.specialization_id
        ORDER BY d.hire_date ASC, s.name ASC
    """,
    "comparison_1": """
        SELECT first_name, last_name, date_of_birth, gender, blood_type
        FROM patients
        WHERE date_of_birth < DATE '1990-01-01'
    """,
    "comparison_2": """
        SELECT p.first_name || ' ' || p.last_name AS patient,
               d.first_name || ' ' || d.last_name AS doctor,
               a.appointment_date, a.status
        FROM appointments AS a
        JOIN patients AS p ON p.patient_id = a.patient_id
        JOIN doctors AS d ON d.doctor_id = a.doctor_id
        WHERE a.appointment_date >= DATE '2025-01-15'
          AND a.status <> 'Cancelled'
    """,
    "in_1": """
        SELECT first_name, last_name, blood_type, phone, address
        FROM patients
        WHERE blood_type IN ('A+', 'B+', 'O+')
    """,
    "in_2": """
        SELECT p.first_name || ' ' || p.last_name AS patient,
               d.first_name || ' ' || d.last_name AS doctor,
               appointments.appointment_date, appointments.status
        FROM appointments
        JOIN patients AS p ON p.patient_id = appointments.patient_id
        JOIN doctors AS d ON d.doctor_id = appointments.doctor_id
        WHERE appointments.status IN ('Scheduled', 'Completed')
    """,
    "exists_1": """
        SELECT d.first_name, d.last_name, s.name AS specialization
        FROM doctors AS d
        JOIN specializations AS s
          ON s.specialization_id = d.specialization_id
        WHERE EXISTS (
            SELECT 1 FROM appointments AS a
            WHERE a.doctor_id = d.doctor_id
        )
    """,
    "exists_2": """
        SELECT p.first_name, p.last_name, r.allergies,
               r.chronic_conditions
        FROM patients AS p
        JOIN patient_medical_records AS r ON r.patient_id = p.patient_id
        WHERE EXISTS (
            SELECT 1
            FROM patient_medical_records AS r
            WHERE r.patient_id = p.patient_id
              AND r.allergies <> 'None'
        )
    """,
    "not_exists_1": """
        SELECT p.first_name, p.last_name, p.phone, p.address
        FROM patients AS p
        WHERE NOT EXISTS (
            SELECT 1 FROM appointments AS a
            WHERE a.patient_id = p.patient_id
        )
    """,
    "not_exists_2": """
        SELECT s.name, s.description
        FROM specializations AS s
        WHERE NOT EXISTS (
            SELECT 1
            FROM doctors AS d
            WHERE d.specialization_id = s.specialization_id
        )
    """,
    "aggregate_1": """
        SELECT COUNT(*) AS patient_count,
               MIN(date_of_birth) AS oldest_birth_date,
               MAX(date_of_birth) AS newest_birth_date
        FROM patients
    """,
    "aggregate_2": """
        SELECT COUNT(*) AS appointment_count,
               MIN(appointment_date) AS first_appointment,
               MAX(appointment_date) AS last_appointment
        FROM appointments
    """,
}


def run_select_queries(connection):
    with connection.cursor() as cursor:
        for name, query in QUERIES.items():
            cursor.execute(query)
            print(f"\n--- {name} ---")
            columns = [column.name for column in cursor.description]
            print(" | ".join(columns))
            for row in cursor.fetchall():
                print(" | ".join(str(value) for value in row))


def update_patient(connection):
    query = """
        UPDATE patients
        SET address = %s
        WHERE patient_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, ("Updated address 1", 1))
        print(f"Updated rows: {cursor.rowcount}")


def delete_appointment_diagnosis(connection):
    query = """
        DELETE FROM appointment_diagnoses
        WHERE appointment_id = (
            SELECT MAX(appointment_id) FROM appointments
        )
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        print(f"Deleted rows: {cursor.rowcount}")
