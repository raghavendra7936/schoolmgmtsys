from django.db import connection

class SchoolMgmtCommon:
    def GetAllClassGrades():
        with connection.cursor() as cursor:
            cursor.execute("select * from common_classgrade")
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def GetClassGrade(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from common_classgrade where id = %s", [id])
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def AddClassGrade(grade):
        with connection.cursor() as cursor:
            cursor.execute("insert into common_classgrade(grade) values(%s)", [grade])
        return True
    
    def GetAllAcadYears():
        with connection.cursor() as cursor:
            cursor.execute("select * from common_academicyear")
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def GetAcademicYear(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from common_academicyear where id = %s", [id])
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result


    def AddAcademicYear(ay, isCurrent):
        with connection.cursor() as cursor:
            cursor.execute("insert into common_academicyear(academicyear, current) values(%s, %s)", [ay, isCurrent])
        return True

    def GetAllClassSections():
        with connection.cursor() as cursor:
            cursor.execute("select * from common_classsection")
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result
    
    def GetClassSection(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from common_classsection where id = %s", [id])
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result
        
    def AddClassSection(sectionname):
        with connection.cursor() as cursor:
                cursor.execute("insert into common_classsection(sectionname) values(%s)", [sectionname])
        return True


    def GetAllSubjects():
        with connection.cursor() as cursor:
            cursor.execute("select * from common_subject")
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def GetSubject(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from common_subject where id = %s", [id])
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def AddSubject(subjectname):
        with connection.cursor() as cursor:
                cursor.execute("insert into common_subject(name) values(%s)", [subjectname])
        return True

    def GetAllTestCycles():
        with connection.cursor() as cursor:
            cursor.execute("select * from common_testcycle")
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result

    def AddTestCycle(cyclename):
        with connection.cursor() as cursor:
                cursor.execute("insert into common_testcycle(name) values(%s)", [cyclename])
        return True

    def GetTestCycle(id):
        with connection.cursor() as cursor:
            cursor.execute("select * from common_testcycle where id = %s", [id])
            columns = [col[0] for col in cursor.description]            
            result = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return result