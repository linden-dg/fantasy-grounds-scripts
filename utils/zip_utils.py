from zipfile import ZipFile, ZIP_DEFLATED
import os


def zip_folder(foldername, *zipname, input_path='./modules/unpacked', output_path='./modules/output', file_type='mod'):
    directory = f'{input_path}/{foldername}'
    zname = zipname if zipname else foldername

    if os.path.exists(directory):
        output = ZipFile(f'{output_path}/{zname}.{file_type}', 'w', ZIP_DEFLATED)

        # The root directory within the ZIP file.
        rootdir = os.path.basename(directory)
        print(rootdir)

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                # Write the file named filename to the archive,
                # giving it the archive name 'arcname'.
                filepath = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, directory)
                output.write(filepath, parentpath)

        print(f'Saved to - {output_path}/{zname}.{file_type}')
        output.close()


def extract_to_directory(zipname, directory='./modules/raw', output_path='./modules/unpacked', file_type='mod'):
    with ZipFile(f'{directory}/{zipname}.{file_type}', 'r') as z:
        z.printdir()
        z.extractall(path=f'{output_path}/{zipname}')
