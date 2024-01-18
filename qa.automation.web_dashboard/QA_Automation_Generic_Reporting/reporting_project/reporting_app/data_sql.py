import pyodbc
from . import key

class SQL(object):
    def __init__(self,project_id,test_id_list):
        self.project_id = project_id
        test_id_list.sort()
        self.test_id_list = test_id_list
        cred = key.get_keys()
        username = cred.qac_db_username
        password = cred.qac_db_password
        connection_string = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=10.101.3.189;DATABASE=SoftwarePlanner;UID=%s;PWD=%s;' % (username, password)
        connection = pyodbc.connect(connection_string)
        self.cursor = connection.cursor()

    def get_test_title(self):
        test_list=[]
        for i in self.test_id_list:

            query  = "SELECT a.TestId, a.Title, b.Requirement, b.Comments "
            query += "FROM (SELECT TestId, Title FROM dbo.Tests WHERE TestId = {test_id} AND ProjId = {proj_id} ) a ".format(test_id=i, proj_id=self.project_id)
            query += "LEFT JOIN (SELECT FKId1 as FKId, Title as Requirement, Comments FROM dbo.TraceabilityLinks JOIN dbo.FunctionalSpecs "
            query += "ON FKId2=FunctSpecId WHERE EntityCode1='Tests' AND EntityCode2='FunctionalSpecs' "
            query += "UNION "
            query += "SELECT FKId2 as FKId, Title as Requirement, Comments FROM dbo.TraceabilityLinks JOIN dbo.FunctionalSpecs "
            query += "ON FKId1=FunctSpecId WHERE EntityCode2='Tests' AND EntityCode1='FunctionalSpecs' ) b "
            query += "ON a.TestId = b.FKId "


            self.cursor.execute(query)
            tests = self.cursor.fetchone()

            if tests:
                if tests.Comments:
                    tests.Comments = 'http://{url}'.format(url=tests.Comments.split('http://')[1].replace('">', ''))
                test_list.append(tests)

        return test_list
