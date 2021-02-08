import os
import shutil
import fnmatch

class Repository:

	def __init__(self):
		self.index = dict()

	def __contains__(self, item):
		return item in self.index

	def scan(self, folder_path, extension):
		file_index = dict()
		for root, paths, fnames in os.walk(folder_path):
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
		else:
			raise NameError('Filename was not found')

class FileCollector:
	
	def __init__(self):
		self.path_collection = list()

	def __str__(self):
		return str(self.path_collection)
		
	def __iter__(self):
		return iter(self.path_collection)
		
	def get_list_of_files(self, folder_path, extension, path_filter = None):
		paths_list = list()
		for root, paths, fnames in os.walk(folder_path):
			# Filter
			if path_filter == None:
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
		path_by_group = dict()
		for path in self.path_collection:
			folder_path = os.path.dirname(path)
			basename = os.path.basename(path)
			if folder_path in path_by_group:
				path_by_group[folder_path].append(basename)
			else:
				path_by_group[folder_path] = [basename]
		return path_by_group

def pull_files(folder_path, file_extension, folder_path_filter, repository_path, search_extension):
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
				msg.count_found_case()
				shutil.copy(target_path, new_target_path)
		except:
			msg.count_missing_case()
			msg.add_missing_item(path, target_path)
	msg.print_summary()
	msg.write_missing_cases_report(report_path)
	
def dynamic_pull_files(folder_path, file_extension, folder_path_filter, repository_relative_path, search_extension):
	'''
		The repository path is relative to each found file
	'''
	report_path = os.path.join(folder_path, 'report-missing_cases.txt')
	
	msg = Message()
	repository = Repository()
	
	file_collector = FileCollector()
	file_collector.get_list_of_files(folder_path, file_extension, folder_path_filter)
	paths_by_dir = file_collector.group_by_dir()

	for folder_path, basenames in paths_by_dir.items():
		repository_path = os.path.normpath(os.path.join(folder_path, repository_relative_path))
		
		if not os.path.isdir(repository_path):
			msg.count_missing_case(len(basenames))
			continue
	
		repository.scan(repository_path, search_extension)
		for basename in basenames:
			path = os.path.join(folder_path, basename)
			new_target_path = os.path.splitext(path)[0] + '.' + search_extension
			target_basename = os.path.basename(new_target_path)		
			try:
				target_paths = repository.search_filename(target_basename)
				if len(target_paths) > 1:
					msg.count_overwrite_case()
				for target_path in target_paths:
					msg.count_found_case()
					shutil.copy(target_path, new_target_path)		
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
		self.missing_cases =list()
	
	def count_missing_case(self, value = 1):
		self.missing_counter+=value
	
	def count_found_case(self):
		self.found_counter+=1

	def count_overwrite_case(self):
		self.overwrite_counter+=1
	
	def add_missing_item(self,*args):
		items = [item for item in args]
		self.missing_cases.append(items)

	def write_missing_cases_report(self, path):
		counter = 0
		with open(path, mode = 'w') as f:
			for case_items in self.missing_cases:
				counter+=1
				f.write('WARNING [{}]: Cannot find the target file\n'.format(counter))
				for item in case_items:
					f.write('- {}\n'.format(item))
			
	def print_summary(self):
		summary_str = 'Copied target files:     \t{}\nMissing target files:     \t{}\nOverwritten target files:\t{}\n'.format(self.found_counter, self.missing_counter, self.overwrite_counter)
		print('--------------------Summary--------------------')
		print(summary_str)
		print('-----------------------------------------------')

if __name__ == '__main__':
	folder_path1 = r'C:\Users\lab\Desktop\pull_copy\test\test3\data'
	file_extension = 'wav'
	folder_path_filter = '*\datos2\*'
	repository_path1 = r'C:\Users\lab\Desktop\pull_copy\test\test1\repository'
	repository_path2 = r'..\sha256'
	search_extension = 'wav.SHA256'
	#dynamic_pull_files(folder_path, file_extension, folder_path_filter, repository_path2, search_extension)
	pull_files(folder_path1, file_extension, folder_path_filter, repository_path1, search_extension)