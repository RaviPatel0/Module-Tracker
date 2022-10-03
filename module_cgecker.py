import os


class ModuleFinder:
    def __init__(self):
        self.python_file_list = []
        self.module_list = []
        self.path = ""

    def find_modules(self, path):
        self.path = path
        files = os.listdir(self.path)
        for file in files:
            if file.endswith(".py"):
                self.python_file_list.append(file)
        for file in self.python_file_list:
            path_to_file = path + "\\" + file
            with open(path_to_file) as file_obj:
                for line in file_obj.readlines():
                    if line.startswith("from"):
                        self.module_list.append(line.split()[1])
                    elif line.startswith("import"):
                        self.module_list.append(line.split()[1])
        final_list = []
        for num in self.module_list:
            if num not in final_list:
                final_list.append(num)
        return final_list


if __name__ == "__main__":
    MODULE_OBJ = ModuleFinder()
    print(MODULE_OBJ.find_modules(input("enter path : ")))
