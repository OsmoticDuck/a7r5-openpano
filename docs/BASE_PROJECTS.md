# 两个基础项目

本仓库是**最小扩展画幅功能补丁/构建说明**，不是完整固件仓库。它依赖下面两个项目。

## 1. sony-a7r5-custom-firmware

职责：

- 原厂/自定义固件提取、打包、FDAT/RSA 签名、AES 整包；
- 项目 A 的**最后功能基线**（本仓库 `build_minimal.py` 读取它的 `patched/appFw.so` 和 `patched/cpapp-b.bin`）；
- `feature-extension-436/result/source`、`package.py`/现有 package 脚本；
- 原厂 DAT、升级器、公私钥、原始输入。

关键哈希见 [../AI_BUILD.md](../AI_BUILD.md) 和 [../firmware/MANIFEST.json](../firmware/MANIFEST.json)。

## 2. a7r5-rea

职责：

- `source/a7r5-dat-tool`：`a7r5dat.tool.inspect`，独立验证签名、整包、成员、版本；
- `A7R5-Studio-0.1.0-mac-arm64-test/.../engine/site`：打包/镜像运行环境；
- 相机侧执行/读取环境；本构建不需要连接相机。

## 3. 不在本仓库的内容

- Sony 原厂固件、`BODYDATA.DAT`、升级器；
- 私钥/公钥/签名材料；
- 基础项目的完整源码；
- 中间调试版本、RAW 放大/弹窗探针；
- 相机实机读取/刷写脚本。

两个基础项目的许可证/使用条款分别适用；本仓库不重新分发它们的代码或密钥。

## 4. 签名旁路

用户必须先按项目 A/B 的说明完成**签名旁路/打包环境**。本仓库不提供密钥、不提供绕过方法，也不对绕过签名的合法性负责。没有这一步，只能编译出未签名/不可安装的 AP/CP，不能生成可刷 `BODYDATA.DAT`。
