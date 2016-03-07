from tkinter import *
from tkinter import messagebox
import shutil
import os
import re
import glob


class AppGui:
    def __init__(self, master):
        main_frame = Frame(master)
        main_frame.grid()
        source_frame = LabelFrame(master, text="SOURCE")
        source_frame.grid(row=1)
        source_field = Entry(source_frame, width=120)
        source_field.grid()
        destination_frame = LabelFrame(master, text="DESTINATION")
        destination_frame.grid(row=2)
        destination_field = Entry(destination_frame, width=120)
        destination_field.grid()
        dwgnum_frame = LabelFrame(master, text="DRAWING NUMBER (1-9)")
        dwgnum_frame.grid(row=3)
        dwgnum_field = Entry(dwgnum_frame, width=120)
        dwgnum_field.grid()
        start_button = Button(main_frame, text="start", command=lambda: self.copy_prep(source_field.get(),
                                                                                       destination_field.get(),
                                                                                       dwgnum_field.get()))
        start_button.grid(row=0)

    #   check for errors in user inputs before proceeding
    @staticmethod
    def copy_prep(src_path, dest_path, filetype):
        copy_check = {'source': False, 'dest': False, 'dwgnum': False}
        for z in range(3):
            if z == 0:
                if os.path.exists(src_path):
                    #   index of filename
                    filename_index = len(src_path)
                    src_path += "\\*.dwg"
                    copy_check['source'] = True
                else:
                    messagebox.showerror(title="error", message="Source directory does not exist, enter C:\\...\\...\\")
            elif z == 1:
                if os.path.exists(dest_path):
                    if decision("Directory", "Directory exists. Copy into directory?"):
                        copy_check['dest'] = True
                elif not os.path.exists(dest_path) and re.search(r"[a-zA-Z]:\\", dest_path):
                    if decision("Directory", "Directory does not exist. Create directory?"):
                        os.makedirs(dest_path)
                        copy_check['dest'] = True
                else:
                    messagebox.showerror(title="error", message="invalid destination path format")

            elif z == 2:
                if filetype in "123456789":
                    copy_check['dwgnum'] = True
                else:
                    messagebox.showerror(title="error", message="enter 1-9 for drawing type")

        if all(copy_check.values()):
            continue_copy(filename_index, src_path, dest_path, filetype)


def continue_copy(filename_index, src_path, dest_path, filetype):
    file_src_list = glob.glob(src_path)
    #   index of file type
    filetype_index = filename_index + 7
    final_list = {}
    file_dict = {}
    rev_order = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    #   create dict from specified file type
    for dwg in file_src_list:
        if dwg[filetype_index] == filetype:
            file_dict[dwg] = [dwg[filename_index:find_rev_index(dwg)], dwg[find_rev_index(dwg)]]
    #   create dict with specified file type from latest revision
    for dwg in file_dict:
        t = dwg[filename_index:find_rev_index(dwg)]
        if t in final_list:
            if rev_order.index(file_dict[dwg][1]) > rev_order.index(final_list[t][1]):
                final_list[t] = [dwg, file_dict[dwg][1]]
        else:
            final_list[t] = [dwg, file_dict[dwg][1]]
    for file_path in final_list:
        print(final_list[file_path])
    print("{0} files copied from {1} into {2}".format(len(final_list), src_path[:len(src_path)-6], dest_path))
    #   copy drawings into destination path
    for drawing in final_list:
        shutil.copy(final_list[drawing][0], dest_path)


#   return index of revision number
def find_rev_index(filename_length):
    return len(filename_length)-5


#   produce yes or no message box
def decision(decision_subject, decision_msg):
    if messagebox.askyesno(title=decision_subject, message=decision_msg):
        return True
    else:
        return False

root = Tk()
test = AppGui(root)
root.mainloop()
