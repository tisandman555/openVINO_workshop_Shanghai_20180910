
# look for models in these dirs
model_dirs = ["/opt/intel/workshop/smart-video-workshop/",
              "/opt/intel/computer_vision_sdk/deployment_tools/demo/",
              "/opt/intel/computer_vision_sdk/deployment_tools/intel_models/",
              "/opt/intel/computer_vision_sdk/deployment_tools/model_downloader/"]

# look for apps in these dirs
app_dirs = ["/opt/intel/computer_vision_sdk/deployment_tools/inference_engine/samples/build/intel64/Release",
            "/opt/intel/workshop/smart-video-workshop/"]

# look for files to infer in these dirs
file_dirs=["/opt/intel/computer_vision_sdk/deployment_tools/demo",
           "/opt/intel/workshop/smart-video-workshop/"]

# model optimizer exes
mo_caffe = "/opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/mo_caffe.py"
mo_tf= "/opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/mo_tf.py"
mo_mxnet= "/opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/mo_mxnet.py"

# app parameters
app_name = ""
model_names = [] # can be multiple
model_name_va = "" # this is dirty workaround for some apps
model_name_lpr = "" # this is dirty workaround for some apps
model_name_ag = "" # this is dirty workaround for some apps
model_name_hp = "" # this is dirty workaround for some apps
data_type = ""
file_to_infer = ""
infer_device = ""
infer_device_hp = "" # this is dirty workaround for some apps
batch_size = ""