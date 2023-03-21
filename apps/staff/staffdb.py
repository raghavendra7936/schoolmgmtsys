from django.db import connection

class SchoolMgmtStaff:
    def GetAllStaffs():
        with connection.cursor() as cursor:
            cursor.execute("select * from staff_staff")
            columns = [col[0] for col in cursor.description]
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def AddStaff(newStaff):
        insertQuery = """insert into staff_staff(current_status, registration_number, surname, firstname, middle_name, gender, 
            date_of_birth, date_of_joining, mobile_number, address, remarks)
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(insertQuery, 
                [newStaff['current_status'], 
                newStaff['registration_number'],
                newStaff['surname'],
                newStaff['firstname'],
                newStaff['middle_name'],
                newStaff['gender'],
                newStaff['date_of_birth'],
                newStaff['date_of_joining'],
                newStaff['mobile_number'],
                newStaff['address'],
                newStaff['remarks']])
        return True

    def GetStaff(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from staff_staff where id = %s", [id])
            columns = [col[0] for col in cursor.description]
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def UpdateStaff(editStaff, pk):
        updateQuery = """update staff_staff set current_status = %s, 
            registration_number = %s, 
            surname = %s, 
            firstname = %s, 
            middle_name = %s, 
            gender = %s, 
            date_of_birth = %s,
            date_of_joining = %s, 
            mobile_number = %s, 
            address = %s, 
            remarks = %s
            where id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(updateQuery, 
                [editStaff['current_status'], 
                editStaff['registration_number'],
                editStaff['surname'],
                editStaff['firstname'],
                editStaff['middle_name'],
                editStaff['gender'],
                editStaff['date_of_birth'],
                editStaff['date_of_joining'],
                editStaff['mobile_number'],
                editStaff['address'],
                editStaff['remarks'],
                pk])
        return True
