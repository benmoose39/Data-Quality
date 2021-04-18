import os
import shutil
import sys

profiles = []
folders = []
name_of_folder = 'Profiling'

for item in os.listdir():
    if os.path.isdir(item) and 'Output_' in item:
        folders.append(item)
        os.chdir(item)
        for file in os.listdir():
            if os.path.isfile(file) and 'Profile_' in file and file[-5:] == '.xlsx':
                profiles.append(os.path.realpath(file))
        os.chdir('../')

if len(profiles) == 0:
    print(f'[*] No files to copy')
    input('Press ENTER to exit...')
    sys.exit()

if name_of_folder not in os.listdir():
    print(f'[*] Creating folder...', end='\t')
    os.mkdir(name_of_folder)
    print(f'[OK]')

os.chdir(name_of_folder)
#print(os.listdir())


count = 0
print(f'[*] Copying {len(profiles)} files...')
for profile in profiles:
    try:
        shutil.copy(profile, '.')
        count += 1
    except:
        print('[!] Some error occured; Please copy manually.')
        input('Press ENTER to exit')
        sys.exit()

if count != len(profiles):
    print(f'[!] {len(profiles)-count} files could not be copied')

print(f'[*] {count} files copied successfully')

y = ['y', 'Y']
if input('[?] Delete the original folders? (y/N): ') in y:
    os.chdir('../')
    print('[*] Removing folders...', end=' ')
    for folder in folders:
        shutil.rmtree(folder, ignore_errors=True)
    print('[OK]')

input('Press ENTER to exit...')
sys.exit()
