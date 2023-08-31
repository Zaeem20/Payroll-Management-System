import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.db import collections
class Utils :
    def __init__(self) -> None:
        self.cred = credentials.Certificate('credentials/payroll-13c3d-firebase-adminsdk-mt5qx-7a292b3ca6.json')
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client(self.app)

    def conn(self,emp_name,acc_no,total_lec,dept):        
        doc_ref = doc_ref = self.db.collection("Employee").document("Dept").collection(dept).document('entries')
        doc_ref.set({"Emp_Name": emp_name, "Account_No":acc_no,"Total_lec": total_lec })
        users_ref = self.db.collection("Employee")
        docs = users_ref.stream()
        return docs
    
    def get(self):
        doc_ref = self.db.collection("Employee").document("Dept").collection("Teaching").collection("Non-Teaching")
        doc = doc_ref.get()
        try:
            if doc.exists:
                return doc
        except Exception as e:
            return e



    def get(self, dept):
        doc_ref = self.db.collection("Employee").document("Dept").collections(dept)
        doc = doc_ref.get()
        try:
            if doc.exists:
                return doc
        except Exception as e:
            return e
        
obj = Utils()
obj.conn('zaeem', 654654213416, 15, 'Teaching')