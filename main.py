import os
import subprocess
from base64 import b85encode, b85decode

def list_files(startpath):
	for root, dirs, files in os.walk(startpath):
		print(root.split('\\')[-1]+'\\')
		for d in dirs:
			print(f'\t{d}')
		for f in files:
			print(f'\t{f}')
		return

def dicttreeview(path: str):
	treeview = ''
	for root, dirs, files in os.walk(path):
		treeview += root+'\n'
		for file in files:
			treeview += root+'/?'+file+'\n'
	return treeview


while True:
	command =  input(f'{os.path.basename((os.getcwd()))}> ')

	if command.startswith('compress'):
		source = ' '.join(command.split()[1:])
		try:
			treeview = dicttreeview(source)
			data = bytes(treeview, 'utf-8')
			for root in treeview.split('\n'):
				for i in root.split('/'):
					if '?' in i:
						with open(root.replace('?', ''), 'rb') as f:
							data += b'root:<--|'+bytes(root, 'utf-8')+b'|'+f.read().replace(b'\n', b'\\n')+b'|-->\n'
							f.close()
			r = '/'.join(treeview.split('\n')[0].split('/')[:-1])
			with open(source.split('/')[0]+'.bfc', 'wb') as f:
				f.write(b85encode(data[:-1].replace(bytes(r, 'utf-8'), b'')))
				f.close()
			print(f"'{source}' > compressed to: '{source.split('/')[0]+'.bfc'}'")
		except Exception as e:
			print(f'Error : {e}')

	elif command.startswith('extract'):
		source = ' '.join(command.split()[1:])
		try:
			data = b85decode(bytes(open(source, encoding='utf-8', errors='ignore').read(), 'utf-8')).decode('utf-8').split('\n')

			for i in data:
				if i.startswith('root:<--|'):
					root, file_data = i.replace('root:<--|', '').replace('|-->', '').split('|')
					with open(root.replace('?', ''), 'w', encoding='utf-8') as f:
						f.write(file_data)
						f.close()
				else:
					if '?' not in i: os.mkdir(i)
					else:
						with open(i.replace('?', ''), 'x') as f: f.close()
			print(f"'{source}' > extracted to: '{source.replace('.bfc', '')}'")
		except Exception as e:
			print(f'Error : {e}')

	elif command == 'exit':
		exit()

	elif command.startswith('cd '):
		try:
			path = ' '.join(command.split()[1:]).replace('"', '').replace("'", '')+'/'
			if path in ['ld/', 'lastdir/', '!!/']:
				os.chdir(lastdir)
			else:
				lastdir = path
				os.chdir(path)
		except Exception as e:
			print(f'Error : {e}')

	elif command == 'dir':
		print('='*70)
		list_files(os.getcwd())
		print('='*70)

	elif command.startswith('open'):
		file = ' '.join(command.split()[1:])
		subprocess.Popen(file, shell=True)

	elif command == 'help':
		print("\n- Only use '/' no '\\' !\n- Files connot be compressed, only folders !\n\n"+'-'*80+"\ncompress\tcompress folders\t\t\tcompress folder\nextract\t\textract data from '.bfc' file\t\textract file.bfc\nhelp\t\tshow help message\t\t\thelp\nexit\t\texit program\t\t\t\texit\ncd\t\tchange current dir\t\t\tcd\ndir\t\tlist dirs and files in current dir\tdir\n"+'-'*80)