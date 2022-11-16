"""
A set of classes and methods for copying files pairs.
"""
import os
import shutil
import fnmatch

class Repository:
    """
    Register files to be search in a Repository.
    """
    def __init__(self):
        self.index = {}

    def __contains__(self, item):
        return item in self.index

    def scan(self, folder_path, extension):
        file_index = {}
        for root, _, fnames in os.walk(folder_path):
            for fname in fnames:
                if not fname.endswith(extension):
                    continue
                path = os.path.join(root, fname)
                if fname in file_index:
                    file_index[fname].append(path)
                else:
                    file_index[fname] = [path]
        self.index = file_index

    def search_filename(self, filename):
        if filename in self.index:
            return self.index[filename]
        raise NameError('Filename was not found')

class FileCollector:

    def __init__(self):
        self.path_collection = []

    def __str__(self):
        return str(self.path_collection)

    def __iter__(self):
        return iter(self.path_collection)

    def get_list_of_files(self, folder_path, extension, path_filter = None):
        paths_list = []
        for root, _, fnames in os.walk(folder_path):
            # Filter
            if path_filter is None:
                pass
            else:
                if not fnmatch.fnmatchcase(root, path_filter):
                    continue

            for fname in fnames:
                if fname.endswith(extension):
                    path = os.path.join(root, fname)
                    paths_list.append(path)
        self.path_collection =  paths_list

    def group_by_dir(self):
        path_collection = self.path_collection.copy()
        path_collection.sort()
        path_by_group = {}
        for path in self.path_collection:
            folder_path = os.path.dirname(path)
            basename = os.path.basename(path)
            if folder_path in path_by_group:
                path_by_group[folder_path].append(basename)
            else:
                path_by_group[folder_path] = [basename]
        return path_by_group

def pull_files(
    folder_path,
    file_extension,
    folder_path_filter,
    repository_path,
    search_extension,
    overwrite_files = False
    ):
    report_path = os.path.join(folder_path, 'report-missing_cases.txt')
    msg = Message()
    repository = Repository()
    repository.scan(repository_path, search_extension)

    file_collector = FileCollector()
    file_collector.get_list_of_files(folder_path, file_extension, folder_path_filter)

    for path in file_collector:
        new_target_path = os.path.splitext(path)[0] + '.'+ search_extension
        target_basename = os.path.basename(new_target_path)
        try:
            target_paths = repository.search_filename(target_basename)
            if len(target_paths) > 1:
                msg.count_overwrite_case()

            for target_path in target_paths:
                if not overwrite_files:
                    if os.path.isfile(new_target_path):
                        msg.count_skip_case()
                        continue

                shutil.copy(target_path, new_target_path)
                msg.count_copy_case()
        except:
            msg.count_missing_case()
            msg.add_missing_item(path)
    msg.print_summary()
    msg.write_missing_cases_report(report_path)

def dynamic_pull_files(folder_path, file_extension, folder_path_filter, repository_relative_path, search_extension, overwrite_files = False):
    '''
        The repository path is relative to each found file
    '''
    report_path = os.path.join(folder_path, 'report-missing_cases.txt')

    msg = Message()
    repository = Repository()

    file_collector = FileCollector()
    file_collector.get_list_of_files(folder_path, file_extension, folder_path_filter)
    paths_by_dir = file_collector.group_by_dir()

    for folder_path_, basenames in paths_by_dir.items():
        repository_path = os.path.normpath(os.path.join(folder_path_, repository_relative_path))

        if not os.path.isdir(repository_path):
            msg.count_missing_case(len(basenames))
            continue

        repository.scan(repository_path, search_extension)
        for basename in basenames:
            path = os.path.join(folder_path_, basename)
            new_target_path = os.path.splitext(path)[0] + '.' + search_extension
            target_basename = os.path.basename(new_target_path)
            try:
                target_paths = repository.search_filename(target_basename)
                if len(target_paths) > 1:
                    msg.count_overwrite_case()
                for target_path in target_paths:
                    if not overwrite_files:
                        if os.path.isfile(new_target_path):
                            msg.count_skip_case()

                            continue
                    shutil.copy(target_path, new_target_path)
                    msg.count_copy_case()
            except:
                msg.count_missing_case()
                msg.add_missing_item(path, repository_path)

    msg.print_summary()
    msg.write_missing_cases_report(report_path)

class Message:

    def __init__(self):
        self.missing_repository_counter = 0
        self.found_counter = 0
        self.missing_counter = 0
        self.overwrite_counter = 0
        self.count_skip_copy = 0
        self.missing_cases = []

    def count_skip_case(self):
        self.count_skip_copy+=1

    def count_missing_case(self, value = 1):
        self.missing_counter+=value

    def count_copy_case(self):
        self.found_counter+=1

    def count_overwrite_case(self):
        self.overwrite_counter+=1

    def add_missing_item(self,*args):
        items = [item for item in args]
        self.missing_cases.append(items)

    def write_missing_cases_report(self, path):
        counter = 0
        with open(path, mode = 'w') as text_file:
            for case_items in self.missing_cases:
                counter+=1
                text_file.write(f'WARNING [{counter}]: Cannot find the target file\n')
                for item in case_items:
                    text_file.write(f'- {item}\n')

    def print_summary(self):
        """
        Print summary of all copies done.
        """
        summary_str = (
        f'Copies done:              \t{self.found_counter}\n'
        f'Skipped copies:          \t{self.count_skip_copy}\n'
        f'Missing targets:        \t{self.missing_counter}\n'
        f'Many-to-one targets:    \t{self.overwrite_counter}\n'
        )

        print('--------------------Summary--------------------')
        print(summary_str)
        print('-----------------------------------------------')
