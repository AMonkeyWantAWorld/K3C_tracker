# K3C_tracker
#### 此插件基于1.6的官改版本！
##### homeassistant的K3C插件，可以获取路由器中在线的设备和mac。
#### 用法:
##### 将插件文件夹拷贝至custom_components目录中，重启后在configuration.yaml中填写以下内容：
device_tracker:  
&ensp;\-&ensp;platform: K3C_tracker  
&ensp;&ensp;&ensp;host: 192.168.2.1  
&ensp;&ensp;&ensp;password: ***  
&ensp;&ensp;&ensp;username: admin  
