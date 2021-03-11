from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


class FileManager:

    def __init__(self, folder_name):
        while True:
            file_list = drive.ListFile({
                'q': f"title='{folder_name}' and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
            if len(file_list) == 0:
                folder = drive.CreateFile({'title': f"{folder_name}", "mimeType": "application/vnd.google-apps.folder"})
                folder.Upload()
            elif len(file_list) == 1:
                break
            elif len(file_list) > 1:
                raise ValueError('There are multiple folders with that specified folder name')

        self.data = file_list[0]

    def upload_file(self, path, filename):
        file = drive.CreateFile({'title': f'{filename}', 'parents': [{'id': f"{self.data['id']}"}]})
        file.SetContentFile(path)
        file.Upload()

    def download_file(self, filename):
        file = drive.CreateFile({'title': f'{filename}', 'parents': [{'id': f"{self.data['id']}"}]})
        file.SetContentFile(filename)

    # create list filename in folder
    def clist_lfif(self):
        query = []
        file_list = drive.ListFile({'q': f"'{self.data['id']}' in parents and trashed=false "}).GetList()
        for file in file_list:
            query.append({'title': file['title'], 'id': file['id']})
        return query
