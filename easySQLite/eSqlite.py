import SED
import sqlite3 as sq
from tabulate import tabulate


class eSQLiteGlobalMethods:

    @classmethod
    def isSubString(cls , string, subString):
        string = str(string)
        subString = str(subString)

        lengthOfSubString = len(subString)
        try:
            for i, j in enumerate(string):
                if(j == subString[0]):
                    if(subString == string[i:i+lengthOfSubString]):
                        return True
                    else:
                        pass
            return False
        except Exception:
            return False




class SQLiteConnect:

    def __init__(self):
        self.security = False
        self.objSecurity = SED.ED()

        self.connObj = None
        self.dataBaseName = None

        self.colNames = []
        self.colList = []
        self.tableName = None

    
    # function to enable to database encryption and to set password as well
    # def setPassword(self , password , pin = 123456 , keysalt = "easySQLite"):
    #     self.objSecurity.setPassword_Pin_keySalt(password , pin , keysalt)
    #     self.security = True

    #     contentList = [["PASS" , "TEXT" , 1]]
    #     table = self.tableName
    #     self.createTable("letscodeofficial.com" , contentList , raiseException)
    #     valuesList = []
    #     valuesList.append(self.objSecurity.returnEncryptedPassword(password))
    #     self.insertIntoTable(valuesList)
    #     self.tableName = table




    
    # function to set the database name
    def setDatabase(self, dataBaseName):
        self.connObj = sq.connect(dataBaseName)
        self.dataBaseName = dataBaseName

    
    # function to get the database name
    def getDatabase(self):
        return self.dataBaseName


    # table parameters - 
    # data types - INT TEXT REAL
    # content List = [ [nameOfCol , dataBaseType , 0 for NULL or 1 for not NULL] , similar more objects ]
    def createTable(self, tableName , contentList , raiseException = False):
        
        self.tableName = str(tableName)
        string = "CREATE TABLE " + self.tableName + " ("

        self.colNames.clear()

        string = string + "ID INT PRIMARY KEY     NOT NULL,"
        self.colNames.append("ID")

        self.colList.clear()

        for i in contentList:
            
            string = string + str(i[0]) + "    "

            self.colNames.append(str(i[0]))

            if(i[1] == "INT"):
                string = string + "INT" + "    "
                self.colList.append([str(i[0]) , "INT"])
            elif(i[1] == "REAL"):
                string = string + "REAL" + "    "
                self.colList.append([str(i[0]) , "REAL"])
            else:
                string = string + "TEXT" + "    "
                self.colList.append([str(i[0]) , "TEXT"])

            try:
                if(int(i[2]) == 1):
                    string = string + "NOT NULL,"
                else:
                    string = string + ","
            except IndexError:
                string = string + ","
        
        string = string[:-1] + ");"

        if(raiseException):
            self.connObj.execute(string)

        else:
            try:
                self.connObj.execute(string)
            except Exception:
                pass
            

        
    
    # fucntion to insert data into table
    def insertIntoTable(self, valuesList , keyPass = None , tableName = None):

        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        if(keyPass == None):
            key = self.returnLastKey() 

            if(key == None):
                key = 0

            else:
                key = key + 1

        else:
            key = int(keyPass)

        string = "INSERT INTO " + tableName + " ("
        
        for i in  self.colNames:
            string = string + i + ","

        string = string[:-1] + " ) VALUES (" + str(key) + ","

        tempCount = 0

        for i in valuesList:
            if((self.colList[tempCount][1] == "INT") or (self.colList[tempCount] == "REAL")):
                string = string + str(i) + ","
            else:
                string = string + "'" + i + "'" + ","

            tempCount += 1

        string = string[:-1] + " )"


        self.connObj.execute(string)
        self.connObj.commit()


    # function to return the last ID
    def returnLastKey(self):

        string = "SELECT "

        id = None

        for i in self.colNames:
            string = string + i + ","
        
        string = string[:-1] + " from " + self.tableName

        cursor = self.connObj.execute(string)

        for row in cursor:
            id = int(row[0])

        return id

    
    # print data of a particular key
    def printDataOfKey(self, key , errorMessage = "key could not be found" , tableName = None):

        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        cursor = self.connObj.execute('select * from ' + tableName)

        colList = list(map(lambda x: x[0], cursor.description))

        table = []
        found = False

        for row in cursor:
            tempTable = []
            
            if(int(row[0] == key)):
                count = 0
                for i in self.colNames:
                    tempTable.append(row[count])
                    count += 1
                found = True
        
            table.append(tempTable)

        if(found):
            print(tabulate(table, headers=colList))
        else:
            print(errorMessage)


    
    # print entire data in a table
    def printData(self , errorMessage = "No data in table" , tableName = None):

        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        cursor = self.connObj.execute('select * from ' + tableName)

        colList = list(map(lambda x: x[0], cursor.description))

        table = []
        found = False

        for row in cursor:
            tempTable = []
        
            count = 0
            for i in self.colNames:
                tempTable.append(row[count])
                count += 1
            found = True
        
            table.append(tempTable)

        if(found):
            print(tabulate(table, headers=colList))
        else:
            print(errorMessage)



    # return data of a particular key
    # returns none if not found
    def returnDataOfKey(self, key , tableName = None):

        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        cursor = self.connObj.execute('select * from ' + tableName)

        table = []

        for row in cursor:
            tempTable = []
            
            if(int(row[0] == key)):
                count = 0
                for i in self.colNames:
                    tempTable.append(row[count])
                    count += 1
        
            table.append(tempTable)

        if(len(table) > 0):
            return table
        else:
            return None


    
    # return entire data in a table
    # returns None if no data is present
    def returnData(self , tableName = None):

        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        cursor = self.connObj.execute('select * from ' + tableName)

        colList = list(map(lambda x: x[0], cursor.description))

        table = []

        table.append(colList)

        for row in cursor:
            tempTable = []
        
            count = 0
            for i in self.colNames:
                tempTable.append(row[count])
                count += 1
        
            table.append(tempTable)

        if(len(table) > 0):
            return table
        else:
            return None



    # function for updating a col data in row
    def updateRow(self , colName , value , key , tableName = None):

        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        string = "UPDATE " + tableName + " set " + str(colName) + " = "

        cor = self.connObj.execute("PRAGMA table_info(" + tableName + ")")

        valueIsText = False

        for i in cor:
            if(i[1] == colName):
                if(i[2] == 'TEXT'):
                    valueIsText = True

        if(valueIsText):
            string = string + "'" + value + "' "
        else:
            string = string + str(value) + " "

        string = string + "where ID = " + str(key)

        self.connObj.execute(string)
        self.connObj.commit()


    # function for deleting a row
    def deleteRow(self, key , updateId = False , tableName = None):

        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        string = "DELETE from " + tableName + " where ID = " + str(key) + ";"

        self.connObj.execute(string)
        self.connObj.commit()

        if(updateId):
            string = "SELECT "

            for i in self.colNames:
                string = string + i + ","
            
            string = string[:-1] + " from " + self.tableName

            cursor = self.connObj.execute(string)

            count = 0

            for row in cursor:
                if(int(row[0]) == count):
                    pass
                else:
                    self.updateRow("ID" , count , row[0] , tableName)
                
                count = count + 1


    # function to upadte the entire row corresponding to a key
    def updateEntireRow(self , valuesList , key , tableName = None):

        if(tableName == None):
            if(self.tableName == None):
                raise Exception("either pass a table name or create that table using createTable function")
            else:
                tableName = self.tableName

        key = int(key)

        count = 1

        cursor = self.connObj.execute('select * from ' + tableName)

        colList = list(map(lambda x: x[0], cursor.description))

        for i in valuesList:
            self.updateRow(colList[count] , i , key , tableName)
            count = count + 1 


    




# for testing purpose
if __name__ == "__main__":
    
    obj = SQLiteConnect()

    obj.setDatabase("test.db")

    contentList = [["test1" , "TEXT" , 1] , ["test2" , "TEXT" , 1] , ["test3" , "INT" , 1]]

    obj.createTable("testTable" , contentList)

    valuesList = ["hello" , "world" , 123]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello1" , "world1" , 456]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello3" , "world3" , 789]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello4" , "world4" , 1234]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello5" , "world45" , 5678]

    obj.insertIntoTable(valuesList)

    obj.printData()

    obj.updateRow("test1" , "hello69" , 3)

    print("\n\n")
    obj.printData()

    obj.deleteRow(2)

    print("\n\n")
    obj.printData()

    valuesList = ["hello55" , "world455" , 91234]

    obj.insertIntoTable(valuesList)

    print("\n\n")
    obj.printData()

    obj.deleteRow(4 , True)

    print("\n\n")
    obj.printData()

    valuesList = ["hello555" , "world4555" , 456789]
    obj.updateEntireRow(valuesList , 2)

    print("\n\n")
    obj.printData()

    
        


        



            

            














