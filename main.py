# import base64
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
# # def decode_from_base64(encoded_string):
# #     decoded_message = base64.b64decode('IFRXI2LWMU======').decode('utf-8')
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     # decode_from_base64('IFRXI2LWMU======')
#     encoded_message = "IFRXI2LWMU======"
#     decoded_message = base64.b64decode(encoded_message).decode('utf-8')
#     print(decoded_message)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import base64
import os, sys
import numpy as np
from PIL import Image
import pickle
import re
import datetime


def decode_from_base32(encoded_string):
    decoded_string = base64.b32decode(encoded_string).decode('utf-8')
    return decoded_string


# def listdirs(rootdir):
#     for it in os.scandir(rootdir):
#         if it.is_dir():
#             print(it)
# listdirs(it)
# os.rename(it, it + '1')
# os.rename(it, 'new_name')

def decode_folder_names(path):
    for folder_name in os.listdir(path):
        if os.path.isdir(os.path.join(path, folder_name)):
            os.rename(os.path.join(path, folder_name), os.path.join(path, decode_from_base32(folder_name)))


def ex1():
    control_ex_file = os.path.dirname(os.path.abspath(__file__)) + '\control_ex1.ct1'
    if os.path.exists(control_ex_file):
        print("The ex1 script was already executed. Please restore folder names and remove control_ex1.ct1 file")
        return
    else:
        open(control_ex_file, 'w').write(str(os.getpid()))
        rootdir_ex1 = (os.path.dirname(os.path.abspath(__file__)) + '/Bar_python_exercise/ex1').replace("\\", "/")
        decode_folder_names(rootdir_ex1)  # ex1


def ex2():
    rootdir_ex2 = (os.path.dirname(os.path.abspath(__file__)) + '/Bar_python_exercise/ex2').replace("\\", "/")
    mysterious_data = np.load(rootdir_ex2 + '/mysterious_file.npz')
    names = mysterious_data.files
    img = Image.open(rootdir_ex2 + '/noised_img.png')
    np_img = np.array(img)
    denoise_image = np_img + mysterious_data[names[0]]
    denoise_img = Image.fromarray(denoise_image)
    denoise_img.save(rootdir_ex2 + '/denoised_image.png')


# def find_file(name, path)
# def rename_file(path)

def ex3():
    control_ex1_file = os.path.dirname(os.path.abspath(__file__)) + '\control_ex1.ct1'
    control_ex3_file = os.path.dirname(os.path.abspath(__file__)) + '\control_ex3.ct1'
    if os.path.exists(control_ex3_file):
        print("The ex3 script was already executed. Please restore the file and the folders names and remove "
              "control_ex1.ct1 file")
        exit()
    elif os.path.exists(control_ex1_file):
        open(control_ex3_file, 'w').write(str(os.getpid()))
        rootdir_ex1 = (os.path.dirname(os.path.abspath(__file__)) + '/Bar_python_exercise/ex1').replace("\\", "/")
        rootdir_ex3 = (os.path.dirname(os.path.abspath(__file__)) + '/Bar_python_exercise/ex3').replace("\\", "/")
        file_from_d110 = open(rootdir_ex3 + '/6/6.pkl',
                              'rb')  # 110 obtained from ex2 and converted from binary to decimal
        data6 = pickle.load(file_from_d110)

        for key, value in data6.items():

            dir_path = rootdir_ex1 + '/' + decode_from_base32(key)
            for filename in os.listdir(dir_path):
                f = os.path.join(dir_path, filename)
                if os.path.isfile(f):
                    file_old_unix_name = os.path.basename(f).split('_')[0]
                    file_index = int(re.findall('_(.*).npz', os.path.basename(f))[0])
                    file_new_unix_name = int(file_old_unix_name) + int(value[file_index])
                    new_file_name = dir_path + '/' + str(
                        datetime.datetime.fromtimestamp(file_new_unix_name).date()) + '.npz'
                    os.rename(f, new_file_name)
    else:
        print("In order to run ex3 you must run ex1")  # relevant if you run them separately
        return



    # print(datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=-214920))


if __name__ == '__main__':
    # print("The dir is: %s" % os.listdir(os.getcwd()))
    ex1()
    #ex2()
    ex3()
    #print(os.path.dirname(os.path.abspath(__file__)))
