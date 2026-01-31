# Things to do:
# View and open the files on their device
# Create new files
# Delete files
# Move or otherwise reorganize existing files

import os

class SuperNode: # root folder
    def __init__(self, children=None, name=None):
        self.children = children if children is not None else []
        self.name = name or "No name given"

    def open_folder(self, foldername):
        # for now just reads off children in folder
        children = os.listdir(foldername)
        if children == '':
            print("Folder empty")
        else:
            print("Folders, files in folder", children)

class Node: # folders
    def __init__(self, parent=None, children=None, name=None):
        self.parent = parent
        self.children = children if children is not None else []
        self.name = name or "No name given"

    def open_folder(self, foldername):
        # for now just reads off children in folder
        children = os.listdir(foldername)
        if children == '':
            print("Folder empty")
        else:
            print("Folders, files in folder", children)

    def create_folder(self, foldername):
        try:
            os.mkdir(foldername)
            print("folder created", foldername)
        except Exception as e:
            print("Error making folder")
    
    def delete_folder(self, foldername):
        if os.path.exists(foldername):
            os.rmdir(foldername)
        else:
            print("Folder does not exists so cannot be deleted")

    def move_folder_to_location(self, foldername, detination):
        pass

class OuterNode: # files
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name or "No name given"

    def open_file(self, filename):
        # for now just prints file info
        try:
            with open(filename, 'r') as file:
                info = file.read()
                print(info)
        except Exception as e:
            print("Error reading file")
        
    def create_file(self, filename):
        # creates and adds temp line
        try:
            with open(filename, 'w') as file:
                file.write("Hello World")
            print("File created") # change to say in parent name
        except Exception as e:
            print("Error making file (should mean it already exists)")
    
    def delete_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("File does not exists so cannot be deleted")

    def move_file_to_location(self, filename, detination):
        pass


# TESTS
def main():
    
    # root1 = SuperNode(name="root1") # blank superNode has nothign in it
    # folder1 = Node(name="folder1")
    # file1 = OuterNode(name="file1") 
    # root1.children.append(folder1)
    # root1.children.append(file1)
    # print([child.name for child in root1.children])  # should print folder1, file1
    # folder1.parent = root1
    # file1.parent = root1
    # print(folder1.parent.name) # should be root1
    # print(file1.parent.name) # should be root1


    # folder2 = Node(name="folder2")
    # file2 = OuterNode(name="file2")
    # root2 = SuperNode(name="root2", children=[folder2, file2])
    # print([child.name for child in root2.children])  # should print folder2, file2
    # folder2.parent = root2
    # file2.parent = root2
    # print(folder2.parent.name) # should be root2
    # print(file2.parent.name) # should be root2



    # dummyfolder = "dummySuperNodeFolder"
    # if not os.path.exits(dummyfolder):
    #     os.mkdir(dummyfolder)
    # os.chdir(dummyfolder)
    
    # dummy_super_node = SuperNode(name="dummysupernode")
    # test_node = Node(name="testnode", parent=dummy_super_node)

    pass


if __name__ == "__main__":
    main()
