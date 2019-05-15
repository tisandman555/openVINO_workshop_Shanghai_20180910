在ubuntu下安装新字体

以win10下windows/fonts的新宋体为例，
sudo mkdir /usr/share/fonts/win10
sudo cp simsun.ttf /usr/share/fonts/win10
sudo chmod 644 /usr/share/fonts/win10/*
cd /usr/share/fonts/win10
执行下面命令，先安装
sudo apt install fonts-utils(它包含mkfontscale等命令)
sudo mkfontscale （创建新宋体字体的fonts.scale文件，它用来控制字体旋转缩放） 
sudo mkfontdir （创建新宋体字体的fonts.dir文件，它用来控制字体粗斜体产生） 
sudo fc-cache -fv （建立字体缓存信息，也就是让系统认识新宋体）

