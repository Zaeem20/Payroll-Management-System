import json
import firebase_admin
from core.models.employee import EmployeeDetails
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client, CollectionReference, DocumentReference,FieldFilter, DocumentSnapshot
from typing import Literal, Dict, List, Any

class Manager :
    def __init__(self, credentials_path: str) -> None:
        self.cred = credentials.Certificate(credentials_path)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db: Client = firestore.client(self.app)
        self.collection_path = "maha-emp-01/department/{}" 

    def update(self, id, new_values: EmployeeDetails):
        dept_type = new_values.deptType
        collection_ref = self.db.collection(self.collection_path.format(dept_type))
        doc: List[DocumentSnapshot[DocumentReference]] = collection_ref.where(filter=FieldFilter('id', '==', id)).get()
        if doc:
            doc[0].reference.update(new_values.to_dict())
            return True
        return False

    def get_next_id(self, dept_type: Literal['teaching', 'non-teaching']):
        counter_ref = self.db.collection(self.collection_path.format(dept_type))
        doc = counter_ref.order_by('id', direction='DESCENDING').limit(1).get()
        if doc:
            max_id = doc[0].to_dict().get('id')
            return max_id + 1
        else:
            return 1

    def get(self, id: int, dept_type: Literal['teaching', 'non-teaching'] = None) -> Dict[str, Any]:
        """
        Retrieves a document from a specified collection in the Firestore database based on the provided ID and department type.
        Returns the document as a dictionary with the key-value pairs sorted in a specified order.

        Args:
            id (int): The ID_Field from the document to retrieve.
            dept_type (Optional[Literal['teaching', 'non-teaching']]): The department type of the document. Defaults to None.

        Returns:
            Dict[str, Any]: The retrieved document as a dictionary with the key-value pairs sorted based on a specified order.
            If the document does not exist, returns None.
        """
        collection_ref = self.db.collection(self.collection_path.format(dept_type))
        doc = collection_ref.where(filter=FieldFilter('id', '==', id)).get()
        if doc:
            document_dict = doc[0].to_dict()
            return EmployeeDetails(**self.__sort_in_required_order(document_dict))
        return None

    def __sort_in_required_order(self, data: dict, order=None):
        """
        Sorts the key-value pairs in a dictionary based on a specified order.

        Args:
            data (dict): The dictionary to be sorted.
            order (tuple, optional): The desired order of the keys in the sorted dictionary. If not provided, a default order is used.

        Returns:
            dict: The input dictionary with the key-value pairs sorted based on the specified order.
        """
        if order is None:
            order = ('id', 'empName', 'deptType', 'salary', 'income_tax', 'prominent_fund', 'other_tax', 'bankAccount', 'ifsc_code')
    
        ordered_dict = {key: data[key] for key in order if key in data}
        return ordered_dict
    
    def getAll(self, dept_type: Literal['teaching', 'non-teaching'] = None):
        if dept_type is None:
            raise KeyError('No collection found: None')
    
        collecion_ref = self.db.collection(self.collection_path.format(dept_type)).stream()
        for doc in collecion_ref:
            yield self.__sort_in_required_order(doc.to_dict())

    def add(self, details: EmployeeDetails = None):
        """
        Adds a new employee to the specified department in the Firestore database.

        Args:
            details (EmployeeDetails): An instance of the EmployeeDetails class representing the details of the employee to be added.

        Returns:
            None
        """
        dept = details.deptType
        doc_ref = self.db.collection(f'maha-emp-01/department/{dept}')
        details_dict = details.to_dict()
        # details_dict['id'] = self.get_next_id(dept_type=dept)
        timestamp, doc = doc_ref.add(details_dict)

        return f'[{timestamp.strftime("%Y-%m-%d %H:%M:%S")}]\nDocument ID: {doc.id}\nCollection: {dept}\nField ID: {details_dict["id"]}'

    def remove(self, id, dept_type):
        collection_ref: CollectionReference = self.db.collection(self.collection_path.format(dept_type))
        document_to_remove: DocumentSnapshot = collection_ref.where(filter=FieldFilter('id', '==', id)).get()
        if document_to_remove:
            document_to_remove[0].reference.delete()
            return True
        else:
            return False

# print(obj.get(10, 'teaching'))
# print(obj.remove(6, 'teaching'))
# entries = json.load(open('random_data.json'))

# for entry in entries:
#     # print(entry)
#     obj.add(EmployeeDetails.from_dict(entry))

# for i in range(1):
#     obj.remove(i, 'teaching')

def load_data(dtype):
    entries = json.load(open('random_data.json'))
    for data in entries:
        if dtype == 'both':
            yield data.values()
        elif data['type'] == dtype:
            yield data.values()
        