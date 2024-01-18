from requests.auth import HTTPBasicAuth
from . import key
import requests
import re

class BitBucket_API(object):

    def __init__(self,repo,branch,path):
        self.repo = repo
        self.branch = branch
        self.url = 'https://api.bitbucket.org/2.0/repositories/corvesta/{repo}'.format(repo=repo)

        cred = key.get_keys()
        username = cred.bitbucket_username
        password = cred.bitbucket_password

        self.basic_auth = HTTPBasicAuth(username, password)
        self.path = path
        self.node = self.get_latest_node()

    def get_latest_node(self):

        url = '{basic_url}/commits/{branch}?pagelen=1'.format(basic_url=self.url, branch=self.branch)

        response = requests.get(url, auth=self.basic_auth)

        if response.status_code == 200:
            data = response.json()

            if data:
                node = data['values'][0]['hash']
                return node

        else:
            raise Exception('no hash was returned')

    def get_files(self,type):

        url = '{basic_url}/src/{node}/{path}?pagelen=100'.format(basic_url=self.url, node=self.node, path=self.path)
        #need to consider pages here

        response = requests.get(url, auth=self.basic_auth)

        files = []

        if response.status_code == 200:
            data = response.json()
            file_path_list = data['values']

            files = []

            if type.lower() == 'cicd':
                for i in file_path_list:
                    file_name = i['path'].split('/')[-1]
                    if file_name.find('_test') > 0 or file_name.find('test_') > 0:
                        files.append(file_name)

            elif type.lower() == 'he':
                for i in file_path_list:
                    file_name = str(i['path'].split('/')[-1])

                    if file_name.startswith('TC') and file_name.endswith('.py'):
                        files.append(file_name)

        return files

    def get_test(self,type):

        files_list = self.get_files(type)
        tests_list = []

        if type.lower() == 'cicd':
            for i in files_list:
                url = '{basic_url}/src/{node}/{file_path}?raw'.format(basic_url=self.url,node=self.node, file_path='%s/%s' % (self.path,i))

                response = requests.get(url, auth=self.basic_auth)
                content = response.text

                #Here is to find test case id, return a list
                test_list = re.findall(r'\ndef test_(\d+)\(\):',content)

                tests_list = tests_list + test_list


        elif type.lower() == 'he':
            for i in files_list:
                test = re.search('TC(.+?).py', i)
                test_id = test.group(1).split('_')[0]
                if test_id != '':
                    tests_list.append(test_id)

        return tests_list
