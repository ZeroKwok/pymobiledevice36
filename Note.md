# Note

## 虚拟环境

```sh
python -m venv .venv
.venv/Scripts/python -m pip install -U pip
.venv/Scripts/pip install -e .[test]
source .venv/Scripts/activate
```

## 测试

```sh
# 安装 pip
./py39/python.exe -m pip install --index-url http://192.168.3.225:8080/simple/ --trusted-host 192.168.3.225 -U pip

# 安装项目 pymobiledevice3 及依赖
./py39/python.exe -m pip install --index-url http://192.168.3.225:8080/simple/ --trusted-host 192.168.3.225 -e .

# 仅安装依赖
./py39/python.exe -m pip install --index-url http://192.168.3.225:8080/simple/ --trusted-host 192.168.3.225 xxx 
./py39/python.exe -m pip install --index-url http://192.168.3.225:8080/simple/ --trusted-host 192.168.3.225 -r requirements.txt

# 运行测试 简单测试
./py39/python.exe -m pymobiledevice3 syslog live
./py39/python.exe -m pymobiledevice3 amfi developer-mode-status

# 运行测试 关键测试 < iOS 17.0
./py39/python.exe -m pymobiledevice3 mounter auto-mount
./py39/python.exe -m pymobiledevice3 developer simulate-location set -- 33.03267791671306 107.08929777145387

# 运行测试 关键测试 >= iOS 17.0
./py39/python.exe -m pymobiledevice3 amfi enable-developer-mode  or 手动开启开发者模式
sudo ./py39/python.exe -m pymobiledevice3 remote tunneld
./py39/python.exe -m pymobiledevice3 developer dvt simulate-location set -- 30.587252101162736 107.08929777145387

# 运行测试用例
./py39/python.exe -m pip install --index-url http://192.168.3.225:8080/simple/ --trusted-host 192.168.3.225 pytest pytest_asyncio
./py39/python.exe -m pytest -W ignore::UserWarning
./py39/python.exe -m pytest tests/services/test_afc.py -W ignore::UserWarning
./py39/python.exe example/location.py
./py39/python.exe example/location.py unset
```

## 实现路线

1. 在3.9 版本中跑通
   1. [x] 剔除 cli 模块
   1. [x] 剔除 services 流程不需要的依赖
   1. [x] 剔除 restore 仅该模块需要的依赖
   1. [x] 编写 location.py
   1. [x] 运行 location.py 并初步测试通过
   1. [x] 检查 location.py 执行流程中所有加载的依赖(必要的)
   1. [x] 剔除 前一步中不需要的依赖
   1. [x] 运行 location.py 并初步测试通过
2. 在3.8 版本中跑通
   1. [x] 安装 依赖项
      1. [x] 依赖项缺失, 版本不兼容
   2. [x] 运行 location.py, 并输出错误
   3. [x] 检查 输出错误
      1. [x] 错误在源码中
      2. [x] 错误在依赖库中
   4. [x] 运行 location.py 并初步测试通过
3. 在3.6 版本中跑通
   1. [x] 安装 依赖项, 处理依赖项缺失
   2. [x] 运行 location.py, 并输出错误
   3. [ ] 检查 输出错误
      1. [ ] 错误在源码中
      2. [ ] 错误在依赖库中
   4. [ ] 运行 location.py 并初步测试通过

## 依赖记录

必备/公共依赖:

- struct
- construct
- packaging
- cryptography
- bpylist2

可剔除依赖:

- cli/IPython
- cli/pygments
- restore/ipsw_parser
- services/mobile_image_mounter.py/developer_disk_image
- services/webinspector.py/prompt_toolkit, wsproto
- services/web_protocol/cdp_screencast.py/Pillow
- [restore/recovery.py|irecv.py]/pyusb

可选的不影响迁移的依赖:

- inquirer3
- [cli|restore]/tqdm
- [cli|services/mobile_activation.py]/inquirer3
- [restore|installation_proxy.py]/zipfile
- tunnel_service.py/aiofiles (`sys.platform != 'win32'`)
- services/dvt/instruments/location_simulation_base.py/gpxpy

### py36

- qh3 使用 aioquic==0.9.15 代替
- opack 没有, 需要寻找替代品
