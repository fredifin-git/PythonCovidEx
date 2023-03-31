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


def decode_folder_names(path):
    for folder_name in os.listdir(path):
        if os.path.isdir(os.path.join(path, folder_name)):
            os.rename(os.path.join(path, folder_name), os.path.join(path, decode_from_base32(folder_name)))


def ex1():
    control_ex_file = os.path.dirname(os.path.abspath(__file__)) + '\control_ex1.ct1'
    # This code avoids launching the script more than once
    # It uses very simple logic without exceptions checks etc.
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


def ex3():
    control_ex1_file = os.path.dirname(os.path.abspath(__file__)) + '\control_ex1.ct1'
    control_ex3_file = os.path.dirname(os.path.abspath(__file__)) + '\control_ex3.ct1'
    if os.path.exists(control_ex3_file):
        print("The ex3 script was already executed. Please restore the file and the folders names and remove "
              "control files")
        return
    elif os.path.exists(control_ex1_file):
        open(control_ex3_file, 'w').write(str(os.getpid()))
        rootdir_ex1 = (os.path.dirname(os.path.abspath(__file__)) + '/Bar_python_exercise/ex1').replace("\\", "/")
        rootdir_ex3 = (os.path.dirname(os.path.abspath(__file__)) + '/Bar_python_exercise/ex3').replace("\\", "/")
        file_from_d110 = open(rootdir_ex3 + '/6/6.pkl',
                              'rb')  # 110 obtained from ex2 and converted from binary to decimal
        data6 = pickle.load(file_from_d110)
        # gets the file name and the index of the file in the folder and adds the time difference to the file name to
        # get the new file name
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


def ex4():
    control_ex1_file = os.path.dirname(os.path.abspath(__file__)) + '\control_ex1.ct1'
    control_ex3_file = os.path.dirname(os.path.abspath(__file__)) + '\control_ex3.ct1'
    if os.path.exists(control_ex1_file) and os.path.exists(control_ex3_file):

        rootdir_ex4 = (os.path.dirname(os.path.abspath(__file__)) + '/Bar_python_exercise/ex1').replace("\\", "/")
        print(rootdir_ex4)

        subdirs = [d for d in os.listdir(rootdir_ex4) if os.path.isdir(os.path.join(rootdir_ex4, d))]
        data_list = []

        # Sorts the subdirs in alphabetical order and npz files by chronological order
        for subdir in sorted(subdirs):
            subdir_path = os.path.join(rootdir_ex4, subdir)
            npz_files = [f for f in os.listdir(subdir_path) if f.endswith(".npz")]
            for npz_file in sorted(npz_files):
                npz_path = os.path.join(subdir_path, npz_file)
                npz_data = np.load(npz_path, allow_pickle=True)['arr_0']
                # print(npz_data.shape)
                if npz_data.size > 0:
                    data_list.append(npz_data)
                    # print(npz_data)

        # Concatenate the arrays along the rows axis to get their shape
        shapes = np.array([arr.shape for arr in data_list])
        max_rows = np.max(shapes[:, 0])

        # Fixes the difference in rows number between the arrays
        for i, arr in enumerate(data_list):
            n_rows = arr.shape[0]
            if n_rows < max_rows:
                pad_rows = max_rows - n_rows
                pad = np.zeros(pad_rows)
                data_list[i] = np.concatenate((arr, pad))
            elif n_rows > max_rows:
                data_list[i] = arr[:max_rows]

        result_array = np.column_stack(data_list)

        print(result_array
              .shape)
        print(result_array)

        np.savez('my_array.npz', arr=result_array)
    else:
        print("In order to run ex4 you must run ex1 and ex3 before!")


if __name__ == '__main__':
    ex1()
    ex2()
    ex3()
    ex4()

