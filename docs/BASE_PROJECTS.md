# 上游项目与下游基线

本仓库是**最小扩展画幅功能补丁/构建说明**，不是完整固件仓库，也不是上游 A/B 的发布。它区分三个东西：

1. 上游 A：[Hearts-Ace/sony-a7r5-custom-firmware](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware)
2. 上游 B：[Liwenru88/a7r5-rea](https://github.com/Liwenru88/a7r5-rea)
3. 本项目的 **OpenPano 下游基线**

## 1. 上游 A — sony-a7r5-custom-firmware

- Sony A7R V / R5 的胶片/滤镜、声音等自定义固件源与构建；
- 六槽回读/解放工具、声音包、滤镜 BIN、ColorLab 工作台；
- 固件源码构建入口；原厂输入、外部签名材料和工具链由使用者按 A 的 README 准备。

A **不包含**：扩展画幅、OpenPano、自制 2:1/65:24 图标、AF 修正、RAW 预览比例修正、RAW 放大研究。

## 2. 上游 B — a7r5-rea

- A7R5 Studio 客户端；
- `source/a7r5-dat-tool`：`a7r5dat.tool.inspect`，独立验证签名、整包、成员、版本；
- 更新信任环境、按需 SSH、libjit、ColorLab 等研究/打包工具；
- 相机侧执行/读取环境；本构建不需要连接相机。

B **不是固件基线**，不提供 OpenPano AP/CP。

## 3. OpenPano 下游基线

- 本项目在 A 的上游胶片/滤镜源 + B 的工具基础上构建；
- 不是 A 的发布，也不是 B 的发布；
- 当前验证副本在下游构建工作区（本机文件夹名可能是 `sony-a7r5-custom-firmware`，但**不是 A 的 GitHub 仓库**）；
- 本仓库不包含它；可用 `A7R5_BASELINE` 指向其他同哈希副本；
- 已包含扩展画幅、自制图标、AF、RAW 预览比例修正和重启/显示修复；
- 唯一未解决：自定义画幅 RAW 回放放大仍提示“无法放大”。

关键哈希见 [../AI_BUILD.md](../AI_BUILD.md) 和 [../firmware/MANIFEST.json](../firmware/MANIFEST.json)。

## 4. 不在本仓库的内容

- Sony 原厂固件、`BODYDATA.DAT`、升级器；
- 私钥/公钥/签名材料；
- 上游 A/B 的完整源码或工具；
- OpenPano AP/CP、`package-openpano 入口`、`分区材料`、`resources/`；
- 中间调试版本、RAW 放大/弹窗探针；
- 相机实机读取/刷写脚本。

上游 A/B 和本仓库的许可证/使用条款分别适用；本仓库不重新分发它们的代码、固件或密钥。

## 5. 签名旁路

用户必须先按上游 A/B 的说明完成**签名旁路/打包环境**。本仓库不提供密钥、不提供绕过方法，也不对绕过签名的合法性负责。没有这一步，只能得到未签名/不可安装的 AP/CP，不能生成可刷 `BODYDATA.DAT`。