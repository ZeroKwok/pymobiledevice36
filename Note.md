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
```

## 实现路线

1. 在3.9 版本中跑通
   1. [ ] 剔除 cli 模块
   2. [ ] 编写 test_location.py
   3. [ ] 运行 test_location.py 并初步测试通过
   4. [ ] 检查 test_location.py 执行流程中所有加载的模块(必要的)
   5. [ ] 剔除 前一步中不需要的模块
   6. [ ] 运行 test_location.py 并初步测试通过
2. 在3.8 版本中跑通
   1. [ ] 安装 依赖项
      1. [ ] 依赖项缺失, 版本不兼容: 讨论, 寻找替代品
   2. [ ] 运行 test_location.py, 并输出错误
   3. [ ] 检查 输出错误
      1. [ ] 错误在源码中: 结合 GPT 修改
      2. [ ] 错误在依赖库中: 需要视情况而定, 可直接修改, 可能接口变更
   4. [ ] 运行 test_location.py 并初步测试通过
3. 在3.6 版本中跑通
   1. [ ] 安装 依赖项, 依赖项缺失: 讨论, 寻找替代品
   2. [ ] 运行 test_location.py, 并输出错误
   3. [ ] 检查 输出错误
      1. [ ] 错误在源码中: 结合 GPT 修改
      2. [ ] 错误在依赖库中: 需要视情况而定, 可直接修改, 可能接口变更
   4. [ ] 运行 test_location.py 并初步测试通过

## 依赖记录

必备/公共依赖:

- construct
- packaging
- cryptography

可剔除依赖:

- cli/tqdm
- cli/IPython
- cli/pygments

可选的不影响迁移的依赖:

- inquirer3

### py36

- qh3 使用 aioquic==0.9.15 代替
- opack 没有, 需要寻找替代品
- 