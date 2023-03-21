from django.db import connection

class SchoolMgmtResult:
    def GetStudentTestCycleResult(stid, tcid, acyear):
        with connection.cursor() as cursor:
            cursor.execute("""select * from result_result 
            where student_id = %s and testcycle_id = %s 
            and academicyear_id = %s""", [stid,tcid, acyear])
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def GetSingleTCResult(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from result_result where id=%s", [id])
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def AddTestCycleResult(tcresult):
        insertQuery = """insert into result_result (student_id, academicyear_id, current_class_id, subject_id, 
        testcycle_id, max_marks, student_score )
        values(%s,%s,%s,%s,%s,%s,%s)
        """

        with connection.cursor() as cursor:
            cursor.execute(insertQuery,
            [tcresult['studentid'],
            tcresult['academicyear'],
            tcresult['current_class'],
            tcresult['subject'],
            tcresult['testcycle'],
            tcresult['max_marks'],
            tcresult['student_score']
            ])
        return True

