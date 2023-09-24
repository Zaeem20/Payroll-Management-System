import firebase_admin
from typing import Literal, Dict, Any
from core.models.employee import EmployeeDetails
from firebase_admin import credentials, firestore
from google.cloud.exceptions import Conflict, NotFound
from google.cloud.firestore import Client, CollectionReference, FieldFilter, DocumentSnapshot

class Manager :
    def __init__(self, credentials_path: str) -> None:
        self.cred = credentials.Certificate(credentials_path)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db: Client = firestore.client(self.app)
        self.collection_path = "maha-emp-01/department/{}" 

    def update(self, id, new_values: EmployeeDetails):
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

