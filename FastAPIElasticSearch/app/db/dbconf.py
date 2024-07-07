from elasticsearch import Elasticsearch, \
    NotFoundError
from elasticsearch.helpers import bulk

from app.conf.config import settings


class ElasticsearchHandler:
    """
    A class to handle Elasticsearch operations.
    """

    def __init__(self, api_key=None, user_name: str = None,
                 pwd: str = None, hosts=None, maxsize=10):
        """
        Initialize the ElasticsearchHandler with a connection pool.

        Args:
            api_key (str, optional): The API key for authentication. Required if Elasticsearch requires API key authentication.
            hosts (list, optional): A list of Elasticsearch hosts. Defaults to ["http://localhost:9200"].
            maxsize (int, optional): The maximum number of connections in the pool. Defaults to 10.
        """

        # if not api_key:
        #     raise ValueError("API key must be provided")

        self.client = Elasticsearch(
            hosts=hosts or ["https://localhost:9200"],
            basic_auth=(user_name, pwd),
            # api_key=(api_key),
            maxsize=maxsize,
            # Enable sniffing to automatically detect new nodes
            # sniff_on_start=True,
            # sniff_on_connection_fail=True,
            # sniffer_timeout=60
            verify_certs=False
        )

    def test_connection(self):
        """
        Test the connection to the Elasticsearch cluster.

        Returns:
            dict: Information about the cluster's health.
        """
        try:
            return self.client.cluster.health()
        except Exception as e:
            return {"error": str(e)}

    def create_index(self, index_name, settings=None, mappings=None):
        """
        Create an Elasticsearch index.

        Args:
            index_name (str): The name of the index to be created.
            settings (dict, optional): The settings for the index. Defaults to None.
            mappings (dict, optional): The mappings for the index. Defaults to None.

        Returns:
            dict: Response from Elasticsearch.
        """
        body = {}
        if settings:
            body['settings'] = settings
        if mappings:
            body['mappings'] = mappings
        return self.client.indices.create(index=index_name, body=body)

    def delete_index(self, index_name):
        """
        Delete an Elasticsearch index.

        Args:
            index_name (str): The name of the index to be deleted.

        Returns:
            dict: Response from Elasticsearch.
        """
        return self.client.indices.delete(index=index_name)

    def index_document(self, index_name, document, id=None):
        """
        Index a document in an Elasticsearch index.

        Args:
            index_name (str): The name of the index.
            document (dict): The document to be indexed.
            id (str, optional): The ID of the document. Defaults to None.

        Returns:
            dict: Response from Elasticsearch.
        """
        return self.client.index(index=index_name, id=id,
                                 body=document)

    def get_document(self, index_name, id):
        """
        Retrieve a document from an Elasticsearch index.

        Args:
            index_name (str): The name of the index.
            id (str): The ID of the document.

        Returns:
            dict or None: The document if found, otherwise None.
        """
        try:
            return self.client.get(index=index_name, id=id)['_source']
        except NotFoundError:
            return None

    def search_documents(self, index_name, query):
        """
        Search for documents in an Elasticsearch index.

        Args:
            index_name (str): The name of the index.
            query (dict): The search query.

        Returns:
            list: List of search results.
        """
        return \
            self.client.search(index=index_name, body=query)['hits'][
                'hits']

    def delete_document(self, index_name, id):
        """
        Delete a document from an Elasticsearch index.

        Args:
            index_name (str): The name of the index.
            id (str): The ID of the document.

        Returns:
            dict or None: Response from Elasticsearch if the document is found, otherwise None.
        """
        try:
            return self.client.delete(index=index_name, id=id)
        except NotFoundError:
            return None

    def bulk_index(self, index_name, documents):
        """
        Bulk index documents in an Elasticsearch index.

        Args:
            index_name (str): The name of the index.
            documents (list): List of documents to be indexed.

        Returns:
            tuple: A tuple containing the number of successfully processed actions and a list of errors (if any).
        """
        actions = [
            {
                "_index": index_name,
                "_id": doc.get('id'),
                "_source": doc
            }
            for doc in documents
        ]
        return bulk(self.client, actions)


elastic_search = ElasticsearchHandler(
    hosts=settings.ELASTICSEARCH_URL,
    user_name=settings.ELASTICSEARCH_USER_NAME,
    pwd=settings.ELASTICSEARCH_PWD)
