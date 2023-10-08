import sys, os
import firebase_admin
from typing import Literal, Dict, Any
from core.models.employee import EmployeeDetails
from firebase_admin import credentials, firestore
from google.cloud.exceptions import Conflict, NotFound
from google.cloud.firestore import Client, CollectionReference, FieldFilter, DocumentSnapshot

class Manager :
    def __init__(self, credentials_path: str) -> None:
        """
        Constructor for the Manager class.
    
        Args:
            credentials_path (str): The path to the credentials file for accessing the Firestore database.
        """
        # Create credentials object
        self.credentials = credentials.Certificate(credentials_path)
    
        # Initialize Firebase app
        self.app = firebase_admin.initialize_app(self.credentials)
    
        # Create database client
        self.db = firestore.client(self.app)
    
        # Set collection path
        self.collection_path = "maha-emp-01/department/{}"

    def add(self, details: EmployeeDetails = None):
        """
        Adds a new employee to the specified department in the Firestore database.
        
        Args:
            details (EmployeeDetails): An instance of the EmployeeDetails class representing the details of the employee to be added.
        Returns:
            None
        """
        try:
            dept = details.deptType
            doc_ref = self.db.collection(f'maha-emp-01/department/{dept}')
            details_dict = details.to_dict()
            # details_dict['id'] = self.get_next_id(dept_type=dept)
            timestamp, doc = doc_ref.add(details_dict)
            return f'[{timestamp.strftime("%Y-%m-%d %H:%M:%S")}]\nDocument ID: {doc.id}\nCollection: {dept}\nField ID: {details_dict["id"]}'
        
        except Conflict:
            return False

    def remove(self, id: int, dept_type: Literal['teaching', 'non-teaching']) -> bool:
        """
        Remove a document from the specified collection in the Firestore database based on the provided ID and department type.

        Args:
            id (int): The ID of the document to be removed.
            dept_type (Literal['teaching', 'non-teaching']): The department type of the document.

        Returns:
            bool: True if the document was successfully deleted, False otherwise.
        """
        collection_ref: CollectionReference = self.db.collection(self.collection_path.format(dept_type))
        document_to_remove: DocumentSnapshot = collection_ref.where(filter=FieldFilter('id', '==', id)).get()
        if document_to_remove:
            document_to_remove[0].reference.delete()
            return True
        else:
            return False

    def update(self, id: int, new_values: EmployeeDetails) -> bool:
        """
        Updates the details of an employee in the Firestore database based on the provided ID and department type.

        Args:
            id (int): The ID of the employee to be updated.
            new_values (EmployeeDetails): An instance of the EmployeeDetails class representing the updated details of the employee.

        Returns:
            bool: True if the document was successfully updated, False otherwise.
        """
        dept_type = new_values.deptType
        collection_ref = self.db.collection(self.collection_path.format(dept_type))
        doc = collection_ref.where(filter=FieldFilter("id", "==", id)).get()
    
        if doc:
            try:
                doc[0].reference.update(new_values.to_dict())
                return True
            except NotFound:
                return False
    
        return False

    def get_next_id(self, dept_type: Literal['teaching', 'non-teaching']) -> int:
        """
        Retrieves the maximum ID value from a specified collection in the Firestore database and returns the next ID value to be used for a new document.

        Args:
            dept_type (Literal['teaching', 'non-teaching']): The department type for which the next ID needs to be retrieved.

        Returns:
            int: The next ID value to be used for a new document in the specified collection. if collection is empty then 1
        """
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

    def getAll(self, dept_type: Literal['teaching', 'non-teaching'] = None):
        """
        Retrieves all documents from a specified collection in the Firestore database and returns them one by one in a sorted order.
        Args:
            dept_type (str, optional): The department type of the documents to retrieve. Defaults to None.
        Yields:
            dict: Each document in the specified collection as a sorted dictionary.
        """
        if dept_type is None:
            raise KeyError('No collection found: None')

        collection_ref = self.db.collection(self.collection_path.format(dept_type)).stream()
        for doc in collection_ref:
            yield self.__sort_in_required_order(doc.to_dict())


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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
