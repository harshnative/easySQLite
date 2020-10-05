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
        self.objSecurity.setSecurityLevel_toLow()
        self.connObj = None
        self.colNames = []
        self.tableName = None

    
    # function to enable to database encryption and to set password as well
    def setPassword(self , password , pin = 123456 , keysalt = "easySQLite"):
        self.objSecurity.setPassword_Pin_keySalt(password , pin , keysalt)
        self.security = True


    # function to set a own salt list for easySED module
    def setSaltList(self , saltList_containingSixStrings):
        self.objSecurity.setOwnSaltList(saltList_containingSixStrings)

    
    # function to set the database name
    def setDatabase(self, dataBaseName):
        self.connObj = sq.connect(dataBaseName)


    # table parameters - 
    # data types - INT TEXT REAL
    # content List = [ [nameOfCol , dataBaseType , 0 for NULL or 1 for not NULL] , similar more objects ]
    def setTable(self, tableName , contentList , raiseException = False):
        
        self.tableName = str(tableName)
        string = "CREATE TABLE " + self.tableName + " ("

        self.colNames.clear()

        string = string + "ID INT PRIMARY KEY     NOT NULL,"
        self.colNames.append("ID")

        for i in contentList:
            
            string = string + str(i[0]) + "    "

            self.colNames.append(str(i[0]))

            if(i[1] == "INT"):
                string = string + "INT" + "    "
            elif(i[1] == "REAL"):
                string = string + "REAL" + "    "
            else:
                string = string + "TEXT" + "    "

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
    def insertIntoTable(self, valuesList):

        key = self.returnLastKey() 

        if(key == None):
            key = 0

        else:
            key = key + 1

        string = "INSERT INTO " + self.tableName + " ("
        
        for i in  self.colNames:
            string = string + i + ","

        string = string[:-1] + " ) VALUES (" + str(key) + ","

        for i in valuesList:
            string = string + "'" + i + "'" + ","

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
    def printDataOfKey(self, key , errorMessage = "key could not be found"):

        string = "SELECT "

        for i in self.colNames:
            string = string + i + ","
        
        string = string[:-1] + " from " + self.tableName

        cursor = self.connObj.execute(string)

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
            print(tabulate(table, headers=self.colNames))
        else:
            print(errorMessage)


    
    # print entire data in a table
    def printData(self , errorMessage = "No data in table"):

        string = "SELECT "

        for i in self.colNames:
            string = string + i + ","
        
        string = string[:-1] + " from " + self.tableName

        cursor = self.connObj.execute(string)

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
            print(tabulate(table, headers=self.colNames))
        else:
            print(errorMessage)



    # return data of a particular key
    # returns none if not found
    def returnDataOfKey(self, key):

        string = "SELECT "

        for i in self.colNames:
            string = string + i + ","
        
        string = string[:-1] + " from " + self.tableName

        cursor = self.connObj.execute(string)

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
    def returnData(self):

        string = "SELECT "

        for i in self.colNames:
            string = string + i + ","
        
        string = string[:-1] + " from " + self.tableName

        cursor = self.connObj.execute(string)

        table = []

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
    def updateRow(self , toUpdate , value , key , valueIsText = True):

        string = "UPDATE " + self.tableName + " set " + str(toUpdate) + " = "

        if(valueIsText):
            string = string + "'" + value + "' "
        else:
            string = string + str(value) + " "

        string = string + "where ID = " + str(key)

        self.connObj.execute(string)
        self.connObj.commit()


    # function for deleting a row
    def deleteRow(self, key , updateId = False):

        string = "DELETE from " + self.tableName + " where ID = " + str(key) + ";"

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
                    self.updateRow("ID" , count , row[0] , False)
                
                count = count + 1

    





if __name__ == "__main__":
    
    obj = SQLiteConnect()

    obj.setDatabase("test.db")

    contentList = [["test1" , "TEXT" , 1] , ["test2" , "TEXT" , 1]]

    obj.setTable("testTable" , contentList)

    valuesList = ["hello" , "world"]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello1" , "world1"]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello3" , "world3"]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello4" , "world4"]

    obj.insertIntoTable(valuesList)

    valuesList = ["hello5" , "world45"]

    obj.insertIntoTable(valuesList)

    obj.printData()

    obj.updateRow("test1" , "hello69" , 3)

    print("\n\n")
    obj.printData()

    obj.deleteRow(2)

    print("\n\n")
    obj.printData()

    valuesList = ["hello55" , "world455"]

    obj.insertIntoTable(valuesList)

    print("\n\n")
    obj.printData()

    obj.deleteRow(4 , True)

    print("\n\n")
    obj.printData()

    
        


        



            

            














