#!/usr/bin/env python3
import os
import mysql.connector
import re
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='employees'
)

cursor = mydb.cursor()
cursor.execute("create table if not exists employees (id int AUTO_INCREMENT PRIMARY KEY,office_name varchar(50),full_name varchar(150) , salary int , email varchar(50) , isManager varchar(10) , health_rate int)")

class Person:
    full_name = None
    money = None
    sleep_mood = None
    healthRate = 0

    def sleep(self,hours):
            self.sleep_mood = "happy"
            if hours >7:
                self.sleep_mood = "lazy"
            elif hours < 7:
                self.sleep_mood = "tired"
               
    def eat(self , meals):
            if meals == 3:
                self.healthRate = 100
            elif meals == 2 :
                self.healthRate = 75
            elif meals == 1:
                self.healthRate = 50  
    def buy(self , item):
        self.money = self.money -10
        

class Employee(Person):
        
        email = None
        salary= 1000
        isManager = None  
        workMood = None     
        def work(self,hours):
            if hours == 8:
                self.workMood = "happy"
            elif hours < 8:
                self.workMood = "lazy"
            elif hours > 8:
                self.workMood = "tired"
        def sendEmail(self ,to , subject , body , receiverName):
            current_dir = os.path.dirname(os.path.abspath(__file__)) 
            filename = os.path.join(current_dir, f'{to}{receiverName}.txt')
            f = open(filename, "x")
            file = open(filename , "w")
            file.write(f"to : {to} \n \n subject: {subject} \n body :{body} \n \n Reciver Name :{receiverName}")
            print("Your mail sent successfully ")
        
class office:
    name = None
    officeEmployees = []
    # def __init__(self, name):
    #     self.name = name
    @staticmethod
    def get_all_employee():
        cursor.execute("select * from employees")
        rows = cursor.fetchall()
        
        for row in rows:
           if row[5]=="no": 
                print(f"ID: {row[0]}, officeName : {row[1]} ,Name : {row[2]}, Salary : {row[3]} , Email : {row[4]} , isManager : {row[5]} , HealthRate : {row[6]}")
           else:
                 print(f"ID: {row[0]}, officeName : {row[1]} ,Name : {row[2]}, Email : {row[4]} , isManager : {row[5]} , HealthRate : {row[6]}")

        
      
    @staticmethod   
    def get_employee(EmployeeID) :
       cursor.execute(f"select * from employees where id = {EmployeeID}")
       rows = cursor.fetchall()
       for row in rows:
           print(f"ID: {row[0]}, Name : {row[1]}, Salary : {row[2]} , Email : {row[3]} , isManager : {row[4]} , HealthRate : {row[5]}")
    @classmethod   
    def hire(self,employe):
        self.officeEmployees.append(employe)
        cursor.execute(f"insert into employees (full_name , office_name ,salary , email , isManager , health_rate) values ('{employe.full_name}' ,'{self.name}' ,{employe.salary} , '{employe.email}' , '{employe.isManager}' , {employe.healthRate})")
        mydb.commit()
      
    @classmethod   
    def fire(self,EmployeeID):
        try:
           del self.officeEmployees[int(EmployeeID)]
        except:
            print("not found")   
        cursor.execute(f"delete from employees where id = {EmployeeID}")  
        mydb.commit()         



            
def displayMenue():
    print("1- Hire a  New Employee")
    print("2-fire an Employee")
    print("3-get all employees")
    print("4-get an Employee")
    print("5-Send Email")
    print("6-quit")
    
def menueActions():
    flag = 1 
    # officeobj = office() 
    employee = Employee();
    while (flag == 1) : 
        displayMenue()
        choice = input("Enter Your Choice: ")
        if choice == "1":
            office.name = input("Enter The name of your office: ")
            employee = addEmployee()
            office.hire(employee)
        elif choice == "2":
            EmployeeID = input("Enter the ID of the Emloyee You Want to delete : ")
            office.fire(EmployeeID)   
        elif choice == "3" :
              office.get_all_employee()   
        elif choice == "4":
             EmployeeID = input("Enter the ID of the Emloyee You Want to review : ")
             office.get_employee(EmployeeID)
        elif choice == "5":
            receiverName = input("enter The Reciver Name : ")
            to = input("Enter The Reciver email : ")
            subject = input("Enter The subject of the email : ")
            body = input("Write Your Email : ")
            employee.sendEmail(to , subject , body ,receiverName)

        elif choice == "6" :
            mydb.close()
            flag = 0
        else :
            print("Please Enter a valid choice")    

def validation(email):      
            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
            if (re.search(regex, email)):
                return True    
            else:
                print("please enter a valid Email")
                return False
def addEmployee():
    employe = Employee();
    officeObj= office()
    employe.full_name = input("The Name of the Employee ")
    employe.salary =0
    employe.email = "" 
    employe.isManager=input("is This employment is a manager (Yes/NO)")
    sleepHours= int(input("Enter the hour of sleeping"))
    numberOfMeals=int(input("Enter the number of meals by day (1/2/3)"))
    employe.sleep(sleepHours)
    employe.eat(numberOfMeals)
    while True:  
        if employe.salary < 1000:
              employe.salary =int( input("The Salary of the Employee (please Enter a value > 1000): "))
        else :
            break;
    
    while True:

            if (validation(employe.email)):
                break    
            else:
                 employe.email = input("The Email of the employee :")

   
    return employe
               
menueActions()

