from django.db import connection

class SchoolMgmtStudent:
    def GetAllStudents():
        with connection.cursor() as cursor:
            cursor.execute("select * from student_student")
            columns = [col[0] for col in cursor.description]
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result


    def AddStudent(newStudent):
        insertQuery = """insert into student_student(current_status, registration_number, surname, firstname, middle_name, gender, 
            date_of_birth, current_class_id, current_section_id, date_of_admission, parent_mobile_number, address, remarks)
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(insertQuery, 
                [newStudent['current_status'], 
                newStudent['registration_number'],
                newStudent['surname'],
                newStudent['firstname'],
                newStudent['middle_name'],
                newStudent['gender'],
                newStudent['date_of_birth'],
                newStudent['current_class'],
                newStudent['current_section'],
                newStudent['date_of_admission'],
                newStudent['parent_mobile_number'],
                newStudent['address'],
                newStudent['remarks']])
        return True

    def UpdateStudent(editStudent, pk):
        updateQuery = """update student_student set current_status = %s, 
            registration_number = %s, 
            surname = %s, 
            firstname = %s, 
            middle_name = %s, 
            gender = %s, 
            date_of_birth = %s,
            current_class_id = %s, 
            current_section_id = %s, 
            date_of_admission = %s, 
            parent_mobile_number = %s, 
            address = %s, 
            remarks = %s
            where id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(updateQuery, 
                [editStudent['current_status'], 
                editStudent['registration_number'],
                editStudent['surname'],
                editStudent['firstname'],
                editStudent['middle_name'],
                editStudent['gender'],
                editStudent['date_of_birth'],
                editStudent['current_class'],
                editStudent['current_section'],
                editStudent['date_of_admission'],
                editStudent['parent_mobile_number'],
                editStudent['address'],
                editStudent['remarks'],
                pk])
        return True

    def GetStudent(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from student_student where id = %s", [id])
            columns = [col[0] for col in cursor.description]
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result        
