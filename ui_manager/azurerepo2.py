import logging
import os
from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError
)

from azure.storage.fileshare import (
    ShareServiceClient,
    ShareClient,
    ShareDirectoryClient,
    ShareFileClient
)

def create_file_share(connection_string, share_name):
    try:
        # Create a ShareClient from a connection string
        share_client = ShareClient.from_connection_string(
            connection_string, share_name)

        logging.warning("Creating share:", share_name)
        share_client.create_share()

    except ResourceExistsError as ex:
        logging.warning(f"ResourceExistsError: {ex.message}")

    
def create_directory(connection_string, share_name, dir_name):
    try:
        # Create a ShareDirectoryClient from a connection string
        dir_client = ShareDirectoryClient.from_connection_string(
            connection_string, share_name, dir_name)

        logging.warning(f"Creating directory: {share_name}/{dir_name}")
        dir_client.create_directory()

    except ResourceExistsError as ex:
        logging.warning(f"ResourceExistsError: {ex.message}")


def delete_dir_tree(c_str, s_name, d_name, space = ""):

    dir_client = ShareDirectoryClient.from_connection_string(conn_str=c_str, share_name=s_name, directory_path=d_name)

    my_list = []
    for item in dir_client.list_directories_and_files():
        my_list.append(item)

    for ele in my_list:
        logging.warning(f"{space}, {ele}")

        if ele['is_directory']:
            delete_dir_tree(c_str, s_name, d_name+"/"+ele['name'], space = space+"   ")
        else:
            file_client = ShareFileClient.from_connection_string(conn_str=c_str, share_name=s_name, file_path=d_name+"/"+ele['name'])
            file_client.delete_file()

    dir_client.delete_directory()

def helper_copy_dir(source_dir, desti_dir, c_str, s_name, useless_ele, space = ""):
    for ele in os.listdir(source_dir):
        if ele in useless_ele:
            continue

        print(space, int(os.path.isdir(source_dir + "/" + ele)), ele)

        if os.path.isdir(source_dir + "/" + ele):
            dir_client = ShareDirectoryClient.from_connection_string(conn_str=c_str, share_name=s_name, directory_path=desti_dir + "/" + ele)
            dir_client.create_directory()

            helper_copy_dir(source_dir + "/" + ele, desti_dir + "/" + ele, c_str, s_name, useless_ele, space = space + "   ")
        else:
            file_client = ShareFileClient.from_connection_string(conn_str=c_str, share_name=s_name, file_path=desti_dir + "/" + ele)

            with open(source_dir + "/" + ele, "rb") as source_file:
                file_client.upload_file(source_file)


def upload_source(source_name, source_dir, desti_dir, c_str, s_name, useless_ele = {"__pycache__"}, space = ""):

    if os.path.isdir(source_dir + "/" + source_name):
        logging.warning(f"Is Directory {source_dir + '/' + source_name}")
        dir_client = ShareDirectoryClient.from_connection_string(conn_str=c_str, share_name=s_name, directory_path=desti_dir + "/" + source_name)
        dir_client.create_directory()

        print(source_dir + "/" + source_name)
        helper_copy_dir(source_dir + "/" + source_name, desti_dir + "/" + source_name, c_str, s_name, useless_ele, space = space)
    
    else:
        file_client = ShareFileClient.from_connection_string(conn_str=c_str, share_name=s_name, file_path=desti_dir + "/" + source_name)
        logging.warning(f"os.getcwd() = {os.getcwd()}")
        logging.warning(f"Normal files: {source_dir} + '/' + {source_name}")
        with open(source_dir + "/" + source_name, "rb") as source_file:
            file_client.upload_file(source_file)

    print("Upload Complete")



def upload_local_file(connection_string, data, share_name, dest_file_path):
    try:

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, dest_file_path)

        logging.warning(f"dest_file_path = {dest_file_path}")        

        logging.warning(f"Uploading to: {share_name}/{dest_file_path}")
        file_client.upload_file(data)

    except ResourceExistsError as ex:
        logging.warning(f"ResourceExistsError: {ex.message}")

    except ResourceNotFoundError as ex:
        logging.warning(f"ResourceNotFoundError: {ex.message}")
        

if __name__ == "__main__":
    share_name = "ias-storage"
    connection_string = "DefaultEndpointsProtocol=https;AccountName=iasproject;AccountKey=QmnE09E9Cl6ywPk8J31StPn5rKPy+GnRNtx3M5VC5YZCxAcv8SeoUHD2o1w6nI1cDXgpPxwx1D9Q18bGcgiosQ==;EndpointSuffix=core.windows.net"
    # Create a ShareServiceClient from a connection string
    service_client = ShareServiceClient.from_connection_string(connection_string)
    #create_file_share(connection_string,share_name)
    #create_directory(connection_string, share_name,"iasdir")
    # delete_dir_tree(connection_string, share_name, )
    # upload_local_file(connection_string, "./temp.txt", share_name, "application_repo/mytest.txt")