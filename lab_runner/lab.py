#!/usr/bin/env python3
from __future__ import print_function
import sys
import os
import global_vars
import subprocess
from subprocess import CalledProcessError

files_found = []
def find_file(file_name, target_dirs, clear_cache = True):
    if clear_cache:
        del files_found[:]
    for d in target_dirs:
        for f in os.listdir(d):
            full_path = os.path.join(d, f)
            if os.path.isdir(full_path):
                find_file(file_name, [full_path], False)
            elif full_path.endswith(file_name):
                files_found.append(full_path)
    return files_found

def show_help_and_exit():
    print("Run me following below param format:")
    print("python3 lab.py $app_name -i $file_to_infer -m %model_name -p FP32/FP16 -d $infer_device(CPU/GPU,etc.) -b $batch_size")
    exit()

def parse_parameters(params):
    
    if len(params) <= 1:
        show_help_and_exit()
    
    if "-h" in params:
        if params.index("-h") == 1:
            show_help_and_exit()
        if params.index("-h") == 2:
            apps = find_file(params[1], global_vars.app_dirs)
            if len(apps) < 1:
                print("app not found: " + params[1])
                exit()
            try:
                for path in execute([apps[0],params[2]]):
                    print(path, end = "")
                exit()
            except CalledProcessError as e:
                print('')
                if e.output:
                    print(e.output)
                exit()
    
    global_vars.app_name = params[1]
    global_vars.model_names.append(params[params.index("-m") + 1])
    
    sub_param = params[params.index("-m") + 1:]
    while True:
        if "-m" not in sub_param:
            break
        if sub_param.index("-m") >=0 :
            global_vars.model_names.append(sub_param[sub_param.index("-m") + 1])
        sub_param = sub_param[sub_param.index("-m") + 1:]
    
    if("-p" in params):
        global_vars.data_type = params[params.index("-p") + 1]
    
    if("-m_va" in params):
        global_vars.model_name_va = params[params.index("-m_va") + 1]
    
    if("-m_lpr" in params):
        global_vars.model_name_lpr = params[params.index("-m_lpr") + 1]
    
    if("-m_ag" in params):
        global_vars.model_name_ag = params[params.index("-m_ag") + 1]
        
    if("-m_hp" in params):
        global_vars.model_name_hp = params[params.index("-m_hp") + 1]
        
    global_vars.file_to_infer = params[params.index("-i") + 1]
    
    if("-d" in params):
        global_vars.infer_device = params[params.index("-d") + 1]
        
    if("-d_hp" in params):
        global_vars.infer_device_hp = params[params.index("-d_hp") + 1]
        
    if("-b" in params):
        global_vars.batch_size = params[params.index("-b") + 1]

    if (len(global_vars.app_name) < 1):
        print("app_name can not be null")
        exit(-1)
    if (len(global_vars.model_names) < 1):
        print("model_name can not be null")
        exit(-1)
    if (len(global_vars.data_type) < 1):
        #print("data_type null, use default value - FP32 ")
        global_vars.data_type = "FP32"
    if (len(global_vars.file_to_infer) < 1):
        print("file_to_infer can not be null")
        exit(-1)
    if (len(global_vars.infer_device) < 1):
        #print("infer_device null, use default value -  CPU ")
        global_vars.infer_device = "CPU"

def setup_params():
    
    apps = find_file(global_vars.app_name, global_vars.app_dirs)
    if len(apps) > 1:
        pass
        #print("multiple app_names found, using the first one we found.")
    global_vars.app_name = apps[0]
    
    updated_models = []
    for model in global_vars.model_names:
        model_name = find_file(model + ".xml", global_vars.model_dirs)
        if len(model_name) > 1 :
            #print("multiple models with same name found :" + model)
            matched = False
            for mn in model_name:
                if(global_vars.data_type in mn):
                    #print("using the model matching data_type "+global_vars.data_type)
                    updated_models.append(mn)
                    matched = True
            if not matched:
                #print("using the first model that we found")
                updated_models.append(model_name[0])
        elif len(model_name) == 1:
            updated_models.append(model_name[0])
    global_vars.model_names = updated_models
    if len(global_vars.model_names) < 1:
        print("model not found!")
        exit()
    
    if len(global_vars.model_name_va) > 1:
        mva = find_file(global_vars.model_name_va + ".xml", global_vars.model_dirs)
        if len(mva) < 1:
            print("va model not found!")
            exit()
        else:
            global_vars.model_name_va = mva[0]
            
    if len(global_vars.model_name_lpr) > 1:
        mlpr = find_file(global_vars.model_name_lpr + ".xml", global_vars.model_dirs)
        if len(mlpr) < 1:
            print("lpr model not found!")
            exit()
        else:
            global_vars.model_name_lpr = mlpr[0]
    
    if len(global_vars.model_name_ag) > 1:
        mag = find_file(global_vars.model_name_ag + ".xml", global_vars.model_dirs)
        if len(mag) < 1:
            print("ag model not found!")
            exit()
        else:
            global_vars.model_name_ag = mag[0]
    
    if len(global_vars.model_name_hp) > 1:
        mhp = find_file(global_vars.model_name_hp + ".xml", global_vars.model_dirs)
        if len(mhp) < 1:
            print("hp model not found!")
            exit()
        else:
            global_vars.model_name_hp = mhp[0]
    
    if "/dev/" not in global_vars.file_to_infer:
        fti = find_file(global_vars.file_to_infer, global_vars.file_dirs)
        if len(fti) > 1:
            #print("multiple file_to_infer found, using the first one we found.")
            pass
        if len(fti) < 1:
            print("file for infer is not found(which was specified by '-i' option): " + global_vars.file_to_infer)
            exit()
        global_vars.file_to_infer = fti[0]
    else:
        print("using camera stream for infer: " + global_vars.file_to_infer);
        
    #print("app_name: " + global_vars.app_name);
    #print("model_names: " + "".join(global_vars.model_names));
    #print("file_to_infer: " + global_vars.file_to_infer);

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def run_target_app():
    
    msg = global_vars.app_name +" -i " + global_vars.file_to_infer
    for model in global_vars.model_names:
        msg = msg + " -m " + model
    msg = msg + " -d " + global_vars.infer_device
    if len(global_vars.batch_size) > 0:
        msg = msg + " -b " + global_vars.batch_size
    
    if len(global_vars.model_name_va) > 0:
        msg = msg + " -m_va " + global_vars.model_name_va
    if len(global_vars.model_name_lpr) > 0:
        msg = msg + " -m_lpr " + global_vars.model_name_lpr
    if len(global_vars.model_name_ag) > 0:
        msg = msg + " -m_ag " + global_vars.model_name_ag
    if len(global_vars.model_name_hp) > 0:
        msg = msg + " -m_hp " + global_vars.model_name_hp
    if len(global_vars.infer_device_hp) > 0:
        msg = msg + " -d_hp " + global_vars.infer_device_hp
        
    print('#########')
    print(msg)
    print('#########')
    input('hit enter to run the above command...')
    print('')
    
    command = [global_vars.app_name,"-i",global_vars.file_to_infer]
    for model in global_vars.model_names:
        command.append("-m")
        command.append(model)
    command.append("-d")
    command.append(global_vars.infer_device)
    if len(global_vars.batch_size) > 0:
        command.append("-b")
        command.append(global_vars.batch_size)
    if len(global_vars.model_name_va) > 0:
        command.append("-m_va")
        command.append(global_vars.model_name_va)
    if len(global_vars.model_name_lpr) > 0:
        command.append("-m_lpr")
        command.append(global_vars.model_name_lpr)
    if len(global_vars.model_name_ag) > 0:
        command.append("-m_ag")
        command.append(global_vars.model_name_ag)
    if len(global_vars.model_name_hp) > 0:
        command.append("-m_hp")
        command.append(global_vars.model_name_hp)
    if len(global_vars.infer_device_hp) > 0:
        command.append("-d_hp")
        command.append(global_vars.infer_device_hp)
    
    try:
        for path in execute(command):
            print(path, end = "")
    except CalledProcessError as e:
        print('')
        print(e.output)
        
# main function
# e.g. lab.py security_barrier_camera_sample -m mobilenet-ssd -p FP32 -i car_1.bmp -d GPU
if __name__ == '__main__':
    #print("lab runner starting..")
    parse_parameters(sys.argv)
    setup_params()
    run_target_app()
    exit(0)
    
    
