from db import getconnection
from datetime import datetime
from datetime import date

plans={"BASIC" :[499.00,10000],"PRO":[1499.00,50000],"SCALE":[3999.00,200000]}
con = getconnection()
cursor=con.cursor()

class Customer:

    def __init__(self,customer_id,sub_type,start_date,plan_code):
        self.customer_id=customer_id
        self.sub_type=sub_type
        self.start_date=start_date
        self.plan_code=plan_code
        self.end_date = None

def caluclate_price(days,version):
    return (int(plans[version][0])//30)*days

def caluclate_units(days,version):
    return plans[version][1] // 30 *days

def caluclate_days(obj):
    difference1=(obj.end_date-obj.start_date).days
    return difference1

try:
    seen=[]
    input=[]

    with open("input.csv","r") as file:
        for i in file.readlines():
            arr=i.split(",")

            if(len(arr)==4):
                cust_id=arr[0].strip()
                date1=arr[1].strip()
                date1=datetime.strptime(date1,"%Y-%m-%d").date()
                event=arr[2].strip()
                plan_code=arr[3].strip()

                obj1=Customer(cust_id,"start",date1,plan_code)

                if(cust_id in seen):
                    for j in input:
                        if(j.customer_id==cust_id and not j.end_date):
                            j.end_date=date1
                            break
                else:
                    seen.append(cust_id)

                input.append(obj1)

            elif(len(arr)==3):
                cust_id=arr[0].strip()
                date2=arr[1].strip()
                date2=datetime.strptime(date2,"%Y-%m-%d").date()

                for j in input:
                    if(j.customer_id==cust_id and not j.end_date):
                        j.end_date=date2

    output=[]

    for i in input:
        arr=[]
        arr.append(i.customer_id)
        arr.append(i.start_date)
        arr.append(i.plan_code)
        if(not i.end_date):
            date12=datetime.strptime("2026-09-30","%Y-%m-%d").date()
            i.end_date=date12

        arr.append(i.end_date)
        days=caluclate_days(i)
        arr.append(days)
        price=caluclate_price(days,i.plan_code)
        units=caluclate_units(days,i.plan_code)
        arr.append(units)
        arr.append(price)
        arr.append(days)
        output.append(arr)


    final_output = {}

    for i in output:
        if i[0] in final_output:
         final_output[i[0]].append([i[1], i[2], i[3], i[4], i[5], i[6]])
        else:
            final_output[i[0]] = [[i[1], i[2], i[3], i[4], i[5], i[6]]]

    for i in final_output:
        print("Customer ID:", i)
        
        for j in final_output[i]:
            print("Start Date:", j[0])
            print("Plan Code:", j[1])
            print("End Date:", j[2])
            print("Days:", j[3])
            print("Units:", j[4])
            print("Price:", j[5])
            print("-------------------")
    for i in output:
        cursor.execute("""
        INSERT INTO BillingRecords
        (customer_id, start_date, end_date, plan_code,
         total_days, units, price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        i[0],  
        i[1], 
        i[3], 
        i[2], 
        i[4], 
        i[5],
        i[6]
    ))
    cursor.commit()
    cursor.close()
    con.close()
    
except FileNotFoundError:
    print("the file dont exist")
