
from pdf2image import convert_from_path
import os
import zipfile
from zipfile import ZipFile
import snip_image
from paddleocr import PPStructure, save_structure_res
import cv2

def pdf_2_image(file_path,file_name):
    images = convert_from_path(os.path.join(file_path, file_name),poppler_path=r'C:\Program Files (x86)\poppler-23.01.0\Library\bin')
    directory=file_name[:-4]
    mid_path=os.path.join(file_path,directory)
    process_path=os.path.join(file_path,directory,'images')
    if os.path.exists(process_path):
        return process_path
    else:
        os.mkdir(mid_path)
        os.mkdir(process_path)
        for i in range(len(images)):
            images[i].save(process_path+f'\{i}.jpg','JPEG')
        return process_path

#%%
def crop_all_pages(file_path):
    pages_path_list = []
    for file in os.listdir(file_path):
        if file.endswith(".jpg") or file.endswith(".png"):
            print('file found:',os.path.join(file_path, file))
            snip_image.snip(file_path=file_path,image_name=file)
    #         pages_path_list.append(os.path.join(result_path, file))
    # return pages_path_list

#%%
def crop_2_table(file_path, image_name):
    table_engine = PPStructure(layout=False, show_log=True, return_ocr_result_in_table=True)
    parent=os.path.dirname(file_path)
    save_folder = os.path.join(parent)
    img_path = os.path.join(file_path, image_name)
    print('crop2talbe: ' + img_path)
    img = cv2.imread(img_path)
    result = table_engine(img)
    save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

    for line in result:
        line.pop('img')
        print(line)
    print('done: ' + img_path)

#%%
def get_cropped_image(file_path):
    for file in os.listdir(file_path):
        if file.startswith('cropped'):
            print('process cropped file: ',os.path.join(file_path, file))
            crop_2_table(file_path, file)




# def get_all_file_paths(directory):
#     # initializing empty file paths list
#     file_paths = []
#
#     # crawling through directory and subdirectories
#     for root, directories, files in os.walk(directory):
#         for filename in files:
#             # join the two strings in order to form the full filepath.
#             filepath = os.path.join(root, filename)
#             file_paths.append(filepath)
#
#     # returning all file paths
#     return file_paths
#
#
# def zip(directory,original_file_name):
#     # path to folder which needs to be zipped
#     # directory =
#
#     # calling function to get all file paths in the directory
#     file_paths = get_all_file_paths(directory)
#
#     # printing the list of all files to be zipped
#     print('Following files will be zipped:')
#     for file_name in file_paths:
#         print(file_name)
#
#     # writing files to a zipfile
#     zip_file_name = original_file_name[:-4] + '.zip'
#     zip_file_abs=os.path.join(directory,zip_file_name)
#     with ZipFile(zip_file_abs, 'w') as zip:
#         # writing each file one by one
#         for file in file_paths:
#             zip.write(file)
#
#     print('All files zipped successfully!')


def zip(file_path, original_file_name):
    # parent=os.path.dirname(file_path)
    zip_file_name=original_file_name[:-4]+'.zip'
    output_filename=os.path.join(file_path,zip_file_name)
    process_file=os.path.join(file_path,original_file_name[:-4])

    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(file_path)
    for parent, dirnames, filenames in os.walk(process_file):
        for filename in filenames:
            # print(filename)
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()
    print('zip done')
#%%

def main():
    if __name__=='__main__':
        var=input('please drag the file:')
        file_path = os.path.dirname(var[1:-1])
        file_name = os.path.basename(var[1:-1])

        print(file_path)
        print(file_name)

        process_path = pdf_2_image(file_path, file_name)
        crop_all_pages(process_path)
        get_cropped_image(process_path)
        # zip(file_path=file_path, original_file_name=file_name)
        print('all done! limengxuan')
main()

