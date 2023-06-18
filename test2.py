import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QGridLayout, QMessageBox, QInputDialog

class File:
    def __init__(self, name):
        self.name = name

class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.subdirectories = []

class BinarySearchTree:
    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = self.Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = self.Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = self.Node(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

class FileSystem:
    def __init__(self):
        self.root = Directory("root")
        self.directory_stack = [self.root]
        self.file_map = {}
        self.bst = BinarySearchTree()

    def create_file(self, name):
        current_directory = self.directory_stack[-1]
        if name in self.file_map:
            print("File with the same name already exists!")
        else:
            file = File(name)
            current_directory.files.append(file)
            self.file_map[name] = file
            self.bst.insert(name)
            print("File created successfully!")

    def create_directory(self, name):
        current_directory = self.directory_stack[-1]
        if current_directory.name == "root":
            if any(directory.name == name for directory in current_directory.subdirectories):
                print("Directory with the same name already exists!")
            else:
                directory = Directory(name)
                current_directory.subdirectories.append(directory)
                print("Directory created successfully!")
        else:
            if any(directory.name == name for directory in current_directory.subdirectories):
                print("Directory with the same name already exists!")
            else:
                directory = Directory(name)
                current_directory.subdirectories.append(directory)
                print("Directory created successfully!")


    def delete_file(self, name):
        current_directory = self.directory_stack[-1]
        for file in current_directory.files:
            if file.name == name:
                current_directory.files.remove(file)
                print("File deleted successfully!")
                return
        print("File not found.")

    def delete_directory(self, name):
        current_directory = self.directory_stack[-1]
        for directory in current_directory.subdirectories:
            if directory.name == name:
                # Delete all files and subdirectories within the directory
                for file in directory.files:
                    directory.files.remove(file)
                for subdirectory in directory.subdirectories:
                    directory.subdirectories.remove(subdirectory)

                current_directory.subdirectories.remove(directory)
                print("Directory deleted successfully!")
                return
        print("Directory not found.")

    def search_file(self, name):
        current_directory = self.directory_stack[-1]
        file_list = current_directory.files

        # Perform binary search
        left = 0
        right = len(file_list) - 1

        while left <= right:
            mid = (left + right) // 2
            if file_list[mid].name == name:
                return file_list[mid]
            elif name < file_list[mid].name:
                right = mid - 1
            else:
                left = mid + 1

        return None

    # Rest of the code remains the same...
    def change_directory(self, name):
        if name == "..":
            if len(self.directory_stack) > 1:
                self.directory_stack.pop()
                print("Changed to parent directory.")
            else:
                print("Already at the root directory.")
        elif name == "-":
            if len(self.directory_stack) > 2:
                self.directory_stack.pop()
                print("Changed back to previous directory.")
            else:
                print("No previous directory.")
        else:
            current_directory = self.directory_stack[-1]
            for directory in current_directory.subdirectories:
                if directory.name == name:
                    self.directory_stack.append(directory)
                    print("Changed to", directory.name, "directory.")
                    return
            print("Directory not found.")

    def print_files(self):
        current_directory = self.directory_stack[-1]
        print("Files in the", current_directory.name, "directory:")
        for file in current_directory.files:
            print(file.name)

    def print_all_files(self, current_directory=None, indent=""):
        if current_directory is None:
            current_directory = self.root

        for file in current_directory.files:
            print(indent + file.name)
        for directory in current_directory.subdirectories:
            print(indent + directory.name + "/")
            self.print_all_files(directory, indent + "    ")

    def print_files_ui(self, text_widget):
        current_directory = self.directory_stack[-1]
        text_widget.append("Files in the " + current_directory.name + " directory:\n")
        for file in current_directory.files:
            text_widget.append(file.name)

    def print_all_files_ui(self, text_widget, current_directory=None, indent=""):
        if current_directory is None:
            current_directory = self.root

        for file in current_directory.files:
            text_widget.append(indent + file.name)
        for directory in current_directory.subdirectories:
            text_widget.append(indent + directory.name + "/")
            self.print_all_files_ui(text_widget, directory, indent + "    ")

class FileSystemApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_system = FileSystem()

        self.setWindowTitle("File System App")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.vertical_layout = QVBoxLayout(self.central_widget)

        self.options_text = QTextEdit()
        self.options_text.setReadOnly(True)
        self.options_text.append("1. Create File")
        self.options_text.append("2. Create Directory")
        self.options_text.append("3. Delete File")
        self.options_text.append("4. Delete Directory")
        self.options_text.append("5. Search File")
        self.options_text.append("6. Change Directory")
        self.options_text.append("7. Print Files in Current Directory")
        self.options_text.append("8. Print All Files in File System")
        self.options_text.append("9. Quit")
        self.vertical_layout.addWidget(self.options_text)

        self.choice_label = QLabel("Enter your choice:")
        self.vertical_layout.addWidget(self.choice_label)

        self.choice_entry = QLineEdit()
        self.vertical_layout.addWidget(self.choice_entry)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.process_choice)
        self.vertical_layout.addWidget(self.submit_button)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.vertical_layout.addWidget(self.output_text)

    def process_choice(self):
        choice = self.choice_entry.text()

        if choice == '1':
            name, ok = QInputDialog.getText(self, "Create File", "Enter file name:")
            if ok:
                self.file_system.create_file(name)
        elif choice == '2':
            name, ok = QInputDialog.getText(self, "Create Directory", "Enter directory name:")
            if ok:
                self.file_system.create_directory(name)
        elif choice == '3':
            name, ok = QInputDialog.getText(self, "Delete File", "Enter file name to delete:")
            if ok:
                self.file_system.delete_file(name)
        elif choice == '4':
            name, ok = QInputDialog.getText(self, "Delete Directory", "Enter directory name to delete:")
            if ok:
                self.file_system.delete_directory(name)
        elif choice == '5':
            name, ok = QInputDialog.getText(self, "Search File", "Enter file name to search:")
            if ok:
                file = self.file_system.search_file(name)
                if file:
                    self.output_text.append("File found!")
                else:
                    self.output_text.append("File not found.")
        elif choice == '6':
            name, ok = QInputDialog.getText(self, "Change Directory", "Enter directory name to change (or '-' to go back):")
            if ok:
                self.file_system.change_directory(name)
        elif choice == '7':
            self.output_text.clear()
            self.output_text.append("Files in the current directory:")
            self.file_system.print_files_ui(self.output_text)
        elif choice == '8':
            self.output_text.clear()
            self.output_text.append("All files in the file system:")
            self.file_system.print_all_files_ui(self.output_text)
        elif choice == '9':
            self.close()
        else:
            options = [
                "1. Create File",
                "2. Create Directory",
                "3. Delete File",
                "4. Delete Directory",
                "5. Search File",
                "6. Change Directory",
                "7. Print Files in Current Directory",
                "8. Print All Files in File System",
                "9. Quit"
            ]
            message = "Invalid choice. Please try again.\n\nAvailable options:\n" + "\n".join(options)
            QMessageBox.information(self, "Invalid Choice", message)

        self.choice_entry.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_system_app = FileSystemApp()
    file_system_app.show()
    sys.exit(app.exec_())