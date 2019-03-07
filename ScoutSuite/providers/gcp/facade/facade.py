from googleapiclient import discovery
from ScoutSuite.providers.gcp.utils import MemoryCache
from ScoutSuite.providers.gcp.facade.stackdriverlogging import StackdriverLoggingFacade

class GCPFacade:
    def __init__(self):
        self._resourcemanager_client = discovery.build('cloudresourcemanager', 'v1', cache_discovery=False, cache=MemoryCache())
        self.stackdriverlogging = StackdriverLoggingFacade()

    # TODO: Make truly async    
    async def get_projects(self):
        projects = []
        request = self._resourcemanager_client.projects().list() 
        while request is not None:
            response = request.execute()
            projects.extend(response.get('projects', []))
            request = self._resourcemanager_client.projects().list_next(previous_request=request, previous_response=response)
        return projects