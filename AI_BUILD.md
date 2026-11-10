# AI_BUILD.md — 给 AI 的最小扩展画幅编译/打包清单

目标：在**上游项目 A、B**和**本项目的 OpenPano 下游基线**都就绪的前提下，构建最小活动版本的扩展画幅固件。

> 本仓库只保留实现扩展画幅的最小功能，不展开中间调试版本。先读 [README.md](README.md)。

## 0.1 用户把项目交给你时，先做这些

- 你是操作者；用户不需要懂代码。
- **先分清三个东西**：
  - 上游 A：[Hearts-Ace/sony-a7r5-custom-firmware](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware) — 胶片/滤镜、声音等自定义固件源；**A 本身没有扩展画幅、OpenPano、自制图标、AF 修正或 RAW 预览修正**。
  - 上游 B：[Liwenru88/a7r5-rea](https://github.com/Liwenru88/a7r5-rea) — A7R5 Studio、a7r5-dat-tool、更新信任、libjit、ColorLab 等 DAT/验证/相机工具；**B 不是固件基线**。
  - **OpenPano 下游基线**：本项目在 A 的固件源基础上、借助 B 的工具构建的扩展画幅基线；当前副本在**下游构建工作区**（本机文件夹名为 `sony-a7r5-custom-firmware`，但它**不是 A 的 GitHub 仓库**）。OpenPano 不在本 GitHub 文件夹，也不是 A 的发布。
- OpenPano 基线是外部输入；如果用户从别处拿到同哈希 AP/CP，可用 `A7R5_BASELINE` 指向（绝对路径，或相对于下游构建工作区的路径）。
- 缺以下任何一项就停止并问用户，不要自己造基线/密钥：
  - A/B 的源码或工具环境；
  - OpenPano 下游 AP/CP（`1a0480...` / `33b63...`）；
  - `package-openpano 入口`、`分区材料`、`resources/`、原厂输入、升级器、签名材料。
- 最终 AP/CP 与 OpenPano 下游基线**逐字节相同**；本项目不修 RAW 放大弹窗，不要声称修好。
- **A 只用于胶片/滤镜/声音；自定义画幅逻辑不依赖 A**。当前 OpenPano 是在 A 的上游胶片源 + 本项目下游构建材料上形成的；不要把它说成 A/B 的发布。如果用户要求“只从原版固件、不要胶片预设”，不要拿 OpenPano 冒充，也不要直接删 A 的资源；必须说明需要把 aspect 补丁重新移植到原版 R5 AP/CP，并重新做图标、AF、RAW 预览和打包验证。这个纯原版 port 当前不存在。
- 只刷最终单个 `BODYDATA.DAT`；不要刷中间 AP/CP。
- 本仓库**不是 self-contained**：GitHub 文件夹只有 README/AI/CHANGES/assets 和 `firmware/final` 构建脚本；OpenPano AP/CP、OpenPano package 入口、分区/资源材料、原厂输入、公私钥、可刷 DAT 都不在本仓库。用户只给本文件夹时，列出缺失并停止，不能引用外部 ready DAT 冒充本仓库产物。

## 0.2 路径

```
$ROOT/
  upstream/sony-a7r5-custom-firmware/ # 上游 A 的克隆；只提供 A 的胶片/声音固件源
  a7r5/a7r5-rea/                      # 上游 B 的克隆；DAT/Studio/信任工具
  build-workspace/                    # 下游构建工作区；本机可能叫 sony-a7r5-custom-firmware
  a7r5-openpano/                      # 本仓库
```

- `$A` = A 的克隆（上游 A）。
- `$B` = `$ROOT/a7r5/a7r5-rea`（上游 B）。
- `$BUILD` = 下游构建工作区（当前本机文件夹名可能是 `sony-a7r5-custom-firmware`；包含 `build-openpano` 和 `package-openpano`）。**它不是 A 的 GitHub 仓库。**

> 名字冲突很容易误导：A 的 GitHub 仓库叫 `sony-a7r5-custom-firmware`，本机下游工作区也可能叫这个名。执行前先确认路径里有没有 `build-openpano` 和 `package-openpano`；只有它们才是下游基线。

## 1. [上游 A](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware) 负责什么

[Hearts-Ace/sony-a7r5-custom-firmware](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware)

- Sony A7R V / R5 的胶片/滤镜、声音等自定义固件源与构建。
- 六槽回读/解放工具、声音包、滤镜 BIN、ColorLab 工作台；
- 固件源码构建入口；原厂输入、外部签名材料和工具链由使用者按 A 的 README 准备。

A **不包含**：

- 扩展画幅 2:1 / 2.35:1 / XPan 65:24；
- OpenPano 下游基线；
- 自制 2:1 / 65:24 图标；
- AF 修正、RAW 预览比例修正、RAW 放大研究。

## 2. [上游 B](https://github.com/Liwenru88/a7r5-rea) 负责什么

[Liwenru88/a7r5-rea](https://github.com/Liwenru88/a7r5-rea)

- A7R5 Studio 客户端；
- `source/a7r5-dat-tool`：DAT 工具、独立签名/整包/成员/版本校验；
- 更新信任环境、按需 SSH、libjit、ColorLab 等研究/打包工具；
- 相机侧执行/读取环境（本构建不需要连接相机）。

B **不是固件基线**，不提供 OpenPano AP/CP；它用于构建/验证/打包。

## 3. OpenPano 下游基线是什么

OpenPano 是本项目在 A 的固件源基础上、借助 B 的工具构建出来的扩展画幅基线：

- 不是 A 的发布，也不是 B 的发布；
- 当前验证副本在下游构建工作区 `$BUILD/build-openpano/patched/`；它是本项目的下游构建材料，不是 A/B 的发布；
- 本仓库不包含它；也可以用 `A7R5_BASELINE` 指向其他同哈希副本；
- 已包含：扩展画幅、2:1/65:24 自制图标、AF 修正、RAW 预览比例修正、重启/显示修复；
- 唯一未解决：自定义画幅 RAW 回放放大仍提示“无法放大”。

### 3.1 后端实现摘要

- 扩展画幅模型 **4..6** 保存在原生 `52b`；菜单增加自定义行；
- CP 增加手动比例记录和消费路径，覆盖取景、对焦放大、拍摄、回放；
- AP 为普通取景、MF、拍摄、回放分别构建独立几何/上下文；RAW 保留原厂全源；大预览使用独立 1920 宽；
- OpenPano 下游基线包含菜单/回放自制图标（2:1、65:24；2.35:1 用原厂图标）；
- 包含 RAW 预览比例/裁切修正；
- 包含 AF 修正（AF 显示类别读取真实源，而不是固定全传感器类别）；
- 包含必需的重启/显示修复：菜单资源、AF 边界/glyph、FC/YUV、CWB、自动布局、显示校准、规则 NOT_SET、源格式、网格/菜单 getter、追踪、AF 窗口、MF/回放共用 PID3019、菜单所有权、回放表交接、CP selector；
- 基线的调试钩子已经是原版指令，没有活动 diagnostics；
- **未解决**：自定义画幅 RAW 回放放大仍提示“无法放大”。此前诊断确认 AP 的 read/availability/descriptor 均成功；caution finder、四个直接 `0x0207a042` 构造点、`0x18992f4` 对话框键都未命中；最后一次 caution 入口钩子导致启动循环，已作废。后续的 RAW zoom 诊断/探针不属于本最小版本。

### 3.2 自制画幅图标

`assets/icons/` 保存自制图标的源文件/备份：

| 用途 | 画幅 | 尺寸 | 文件 |
|---|---|---|---|
| 菜单 | 2:1 | 76×40 | `menu-2x1.png` + `menu-2x1.rgba4444` |
| 菜单 | 65:24 (XPan) | 76×40 | `menu-65x24.png` + `menu-65x24.rgba4444` |
| 回放 | 2:1 | 47×32 | `play-2x1.png` + `play-2x1.rgba4444` |
| 回放 | 65:24 (XPan) | 47×32 | `play-65x24.png` + `play-65x24.rgba4444` |

- 这些图标已经安装在 OpenPano 下游基线的菜单/回放资源中；`assets/icons/` 是源文件，不是独立可刷固件；
- 2.35:1 沿用原厂图标；
- 图标哈希见 `assets/icons/artwork-manifest.json` 和 `assets/icons/README.md`。

## 4. 输入

| 输入 | 路径（相对 `$BUILD`） | SHA256 |
|---|---|---|
| OpenPano 下游 AP（默认路径；可用 `A7R5_BASELINE` 覆盖） | `build-openpano/patched/appFw.so` | `1a048077a42c538483ec9bb7f354bf7edbb1be95919cce5df299c56c4a9b0751` |
| OpenPano 下游 CP（默认路径；可用 `A7R5_BASELINE` 覆盖） | `build-openpano/patched/cpapp-b.bin` | `33b63f6bc300f481e1a04126e81b9b3d9e0c2db2eb178164362adb52522d8b10` |

最小最终产物（固定）：

| 产物 | SHA256 |
|---|---|
| 最小最终 AP | `1a048077a42c538483ec9bb7f354bf7edbb1be95919cce5df299c56c4a9b0751` |
| 最小最终 CP | `33b63f6bc300f481e1a04126e81b9b3d9e0c2db2eb178164362adb52522d8b10` |

**不提供固定 DAT 哈希**：DAT 版本字段是容器编号，换编号后整包哈希会变。

## 5. 构建最小 AP/CP

把 `firmware/final` 复制为 `$BUILD` 的直接子目录：

```bash
cd "$BUILD"
rm -rf ext-aspect-minimal
cp -R "$ROOT/a7r5-openpano/firmware/final" ext-aspect-minimal
cd ext-aspect-minimal
python3 build_minimal.py
```

脚本会：

1. 读取 OpenPano 下游基线 AP/CP（默认 `$BUILD/build-openpano`；`A7R5_BASELINE` 可指向其他已验证副本）；
2. 断言 AP `1a0480...`、CP `33b63...`；
3. 直接复制为 `ap-build/appFw-minimal.NONINSTALLABLE.so` 和 `ap-build/cpapp-minimal.NONINSTALLABLE.bin`。

OpenPano 下游基线已经包含扩展画幅、图标、RAW 预览比例修正、AF 和重启修复；不在这里打额外补丁，也不添加调试钩子。

## 6. 打包/签名/容器编号

使用**下游构建工作区**的 OpenPano package 入口（不是 A 的 GitHub 仓库）：

```bash
cd "$BUILD/package-openpano"
# 如果这个目录不存在，就在下游 OpenPano 打包材料目录里找现有 package 入口；不要改 AP/CP
```

说明：

- 最小最终 AP/CP 与 OpenPano 下游基线逐字节相同，所以该 package 入口可以直接使用；不需要改 AP/CP；
- 该 package 入口的输出目录 `build-openpano` 可能已存在；如果已存在，不要覆盖，按该目录现有的版本准备流程使用新的容器编号/输出目录（只改版本字段，不改 AP/CP/分区），或停下问用户；不要用外部 ready DAT 冒充打包结果；
- 打包后必须独立验证；
- 不要直接把 PNG 图标或 AP/CP 塞进 DAT。

### 6.1 版本号只是容器编号

本仓库不分配自己的版本号。打包时把固件版本字段设为**任意一个比机内当前版本更新的编号**即可：

- 机内版本为 X → 填任意 X+0.01 或更大的编号；
- 不需要匹配任何历史编号，也没有 Sony 发布语义。

版本字段只影响 DAT 的容器编号和整包哈希；AP/CP 功能内容不变。打包后记录实际生成的 DAT 哈希。

### 6.2 必须验证

```python
from a7r5dat.tool import inspect
inspect('BODYDATA.DAT', Path('public.pem'), full=True)
```

确认 `signature_verified`、`full_frame_validation`、你选择的容器编号、实际 DAT SHA256；相对原版基线只改变 AP/CP/sum 三个成员（以原版/上游基线比较为准）。

## 7. 刷写

- 先完成[上游 A](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware)/[上游 B](https://github.com/Liwenru88/a7r5-rea) 的**签名旁路/刷写环境**；本仓库不提供绕过方法。
- 只刷最终生成的单个 `BODYDATA.DAT`。
- 测试：三个自定义比例分别关机开机；摇杆 AF；对焦放大进出；拍照/回放；切回原厂。
- 出问题先恢复原厂/OpenPano 下游基线，不要连续刷多个自定义包。

## 8. 常见失败

| 现象 | 原因 | 处理 |
|---|---|---|
| 找不到 `build-OpenPano...` | 下游构建工作区没有 OpenPano | 让用户提供下游 OpenPano AP/CP，或用 `A7R5_BASELINE` |
| 找不到 A/B 源码或工具 | [上游 A](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware)/[上游 B](https://github.com/Liwenru88/a7r5-rea) 未准备 | 按 [A](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware)/[B](https://github.com/Liwenru88/a7r5-rea) README 准备；缺什么问用户 |
| AP/CP 哈希不对 | 基线不是预期 | 用本文件哈希对照 |
| 签名/整包失败 | 私钥/原厂输入/打包环境不对 | 回 A/B 的签名旁路；不要自己生成密钥 |
| 版本号被拒 | 容器编号不高于机内 | 换成任意更大的编号 |

## 9. 交付前检查

- [ ] [上游 A](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware)/[上游 B](https://github.com/Liwenru88/a7r5-rea) 的来源和角色已向用户说明：A 是胶片/声音固件源，B 是工具，OpenPano 是下游基线；
- [ ] OpenPano 下游 AP/CP 哈希匹配（`1a0480...` / `33b63...`）；
- [ ] 最小最终 AP/CP 哈希匹配；
- [ ] 容器编号是任意更高编号，且已记录；
- [ ] `a7r5dat.tool.inspect(full=True)` 通过；
- [ ] 不包含 RAW zoom 探针、私钥、Sony 原厂固件；
- [ ] 明确告知用户：自定义画幅 RAW 回放放大仍未解决，未实机验证的部分不得声称已解决。