# AI_BUILD.md — 给 AI 的最小扩展画幅编译/打包清单

目标：在 **sony-a7r5-custom-firmware** 与 **a7r5-rea** 两个基础项目已经能完成签名旁路/打包的前提下，构建**最小活动版本**的扩展画幅固件。

> 本仓库只保留实现扩展画幅的最小功能，不展开中间调试版本。先读 [README.md](README.md)。

## 0.1 用户把项目交给你时，先做这些

- 你是操作者；用户不需要懂代码。
- 先确认 `$CUSTOM/build-5.01-magnify-20261110/patched/appFw.so` 和 `cpapp-b.bin` 存在且哈希匹配；没有就请用户提供基础项目 A 的 5.01 基线，不要自己造基线。
- 确认项目 A 的原厂输入/升级器/公私钥、`raw-zoom-magnify-501-20261110/package501.py`、`partition501.json`、`resources/` 都在；缺什么直接问用户，不要生成密钥或替换成未验证版本。
- 最终 AP/CP 与 5.01 基线**逐字节相同**；本项目不修 RAW 放大弹窗，不要声称修好。
- 只刷最终单个 `BODYDATA.DAT`；不要刷中间 AP/CP。
- **本仓库不是 self-contained**：GitHub 文件夹只有 README/AI/CHANGES/assets 和 `firmware/final` 构建脚本；5.01 AP/CP、`package501.py`、`partition501.json`、`resources/`、原厂输入、公私钥和任何可刷 DAT 都在**外部**项目 A/B，不在本仓库。
- 如果用户只提供本 GitHub 文件夹：停止，列出缺失，请用户提供项目 A/B 和 5.01 基线/密钥；不能生成/交付可刷 DAT，也不能引用项目 A 的 ready DAT 冒充本仓库产物。

## 0. 路径

```
$ROOT/
  sony-a7r5-custom-firmware/          # 基础项目 A（固件/签名/打包）
  a7r5/a7r5-rea/                      # 基础项目 B（DAT 工具/引擎/独立校验）
  a7r5/direct-p1-read-20261031/       # 分析依赖
  a7r5-openpano/                      # 本仓库
```

- `$CUSTOM` = `$ROOT/sony-a7r5-custom-firmware`
- `$REA` = `$ROOT/a7r5/a7r5-rea`

## 1. 基础项目负责什么

### 1.1 sony-a7r5-custom-firmware（项目 A）

- 原厂/自定义固件提取、打包、FDAT/RSA 签名、AES 整包；
- 项目 A 的 **5.01 raw-preview-magnify 基线**（本仓库 `build_minimal.py` 读取它的 `patched/appFw.so` / `patched/cpapp-b.bin`）；
- 该基线已经包含扩展画幅、自制菜单/回放图标、AF 修正和重启/显示修复；
- `feature-extension-436/result/source`、`package.py`/现有 package 脚本；
- 原厂 DAT、升级器、公私钥、原始输入。

### 1.2 a7r5-rea（项目 B）

- `source/a7r5-dat-tool`：`a7r5dat.tool.inspect`；
- `A7R5-Studio-0.1.0-mac-arm64-test/.../engine/site`：打包/镜像运行环境；
- 相机侧执行/读取环境（本构建不需要连接相机）。

**签名旁路/密钥不在本仓库**。项目 A 的 `private.pem`、`updater.img`、`original.DAT`、`public.pem`、`sony_public.pem` 必须由使用者按项目 A 的说明准备。

### 1.3 后端实现摘要（从 README 移入）

- 扩展画幅模型 **4..6** 保存在原生 `52b`；菜单增加自定义行；
- CP 增加手动比例记录和消费路径，覆盖取景、对焦放大、拍摄、回放；
- AP 为普通取景、MF、拍摄、回放分别构建独立几何/上下文；RAW 保留原厂全源；大预览使用独立 1920 宽；
- 5.01 基线已包含菜单/回放自制图标（2:1、65:24；2.35:1 用原厂图标）；
- 5.01 基线已包含 RAW 预览比例/裁切修正；
- 5.01 基线已包含 AF 修正（AF 显示类别读取真实源，而不是固定全传感器类别）；
- 5.01 基线已包含使用自定义画幅所必需的重启/显示修复：菜单资源、AF 边界/glyph、FC/YUV、CWB、自动布局、显示校准、规则 NOT_SET、源格式、网格/菜单 getter、追踪、AF 窗口、MF/回放共用 PID3019、菜单所有权、回放表交接、CP selector；
- 5.01 基线的调试钩子已经是原版指令，没有活动 diagnostics；
- **未解决**：自定义画幅 RAW 回放放大仍提示“无法放大”。此前诊断确认 AP 的 read/availability/descriptor 均成功；caution finder、四个直接 `0x0207a042` 构造点、`0x18992f4` 对话框键都未命中；最后一次 caution 入口钩子导致启动循环，已作废。5.02 起的 RAW zoom 诊断/探针不属于本最小版本；5.x 探针也不包含。

### 1.4 自制画幅图标

`assets/icons/` 保存自制图标的源文件/备份：

| 用途 | 画幅 | 尺寸 | 文件 |
|---|---|---|---|
| 菜单 | 2:1 | 76×40 | `menu-2x1.png` + `menu-2x1.rgba4444` |
| 菜单 | 65:24 (XPan) | 76×40 | `menu-65x24.png` + `menu-65x24.rgba4444` |
| 回放 | 2:1 | 47×32 | `play-2x1.png` + `play-2x1.rgba4444` |
| 回放 | 65:24 (XPan) | 47×32 | `play-65x24.png` + `play-65x24.rgba4444` |

- 这些图标已经安装在 5.01 基线的菜单/回放资源中；`assets/icons/` 是源文件，不是独立可刷固件；
- 2.35:1 沿用原厂图标；
- 图标哈希见 `assets/icons/artwork-manifest.json` 和 `assets/icons/README.md`。

## 2. 输入

| 输入 | 路径（相对 `$CUSTOM`） | SHA256 |
|---|---|---|
| 5.01 基线 AP | `build-5.01-magnify-20261110/patched/appFw.so` | `1a048077a42c538483ec9bb7f354bf7edbb1be95919cce5df299c56c4a9b0751` |
| 5.01 基线 CP | `build-5.01-magnify-20261110/patched/cpapp-b.bin` | `33b63f6bc300f481e1a04126e81b9b3d9e0c2db2eb178164362adb52522d8b10` |

最小最终产物（固定）：

| 产物 | SHA256 |
|---|---|
| 最小最终 AP | `1a048077a42c538483ec9bb7f354bf7edbb1be95919cce5df299c56c4a9b0751` |
| 最小最终 CP | `33b63f6bc300f481e1a04126e81b9b3d9e0c2db2eb178164362adb52522d8b10` |

**不提供固定 DAT 哈希**：DAT 版本字段是容器编号，换编号后整包哈希会变。

## 3. 构建最小 AP/CP

把 `firmware/final` 复制为 `$CUSTOM` 的直接子目录：

```bash
cd "$CUSTOM"
rm -rf ext-aspect-minimal
cp -R "$ROOT/a7r5-openpano/firmware/final" ext-aspect-minimal
cd ext-aspect-minimal
python3 build_minimal.py
```

脚本会：

1. 读取项目 A 的 5.01 基线 AP/CP；
2. 断言 AP `1a0480...`、CP `33b63...`；
3. 直接复制为 `ap-build/appFw-minimal.NONINSTALLABLE.so` 和 `ap-build/cpapp-minimal.NONINSTALLABLE.bin`。

5.01 基线已经包含扩展画幅、图标、RAW 预览比例修正、AF 和重启修复；不在这里打额外补丁，也不添加调试钩子。

## 4. 打包/签名/容器编号

使用项目 A 的 5.01 package 入口：

```bash
cd "$CUSTOM/raw-zoom-magnify-501-20261110"
# package501.py 已使用与最小最终 AP/CP 相同的 5.01 AP/CP 和 partition501/resources
python3 package501.py
```

说明：

- 最小最终 AP/CP 与 5.01 基线逐字节相同，所以 `package501.py` 可以直接使用；不需要改 AP/CP；
- `package501.py` 的默认版本是 5.01，输出目录 `build-5.01-magnify-20261110` 可能已存在；如果已存在，不要覆盖，按 `prepare_version501.py` 的方式使用新的容器编号/输出目录（只改版本字段，不改 AP/CP/分区），或停下问用户；不要用外部 ready DAT 冒充本仓库打包结果；
- 打包后必须独立验证；
- 不要直接把 PNG 图标或 AP/CP 塞进 DAT。

本仓库不包含现成 DAT；必须按上面的流程打包并独立验证。如果用户只有本文件夹，先列出缺失的基础项目/5.01 基线/密钥，不要交付未经本流程生成的 DAT。

### 4.1 版本号只是容器编号

本仓库不分配自己的版本号。打包时把固件版本字段设为**任意一个比机内当前版本更新的编号**即可：

- 机内版本为 X → 填任意 X+0.01 或更大的编号；
- 不需要匹配任何历史编号，也没有 Sony 发布语义。

版本字段只影响 DAT 的容器编号和整包哈希；AP/CP 功能内容不变。打包后记录实际生成的 DAT 哈希。

### 4.2 必须验证

```python
from a7r5dat.tool import inspect
inspect('BODYDATA.DAT', Path('public.pem'), full=True)
```

确认 `signature_verified`、`full_frame_validation`、你选择的容器编号、实际 DAT SHA256；相对原版基线只改变 AP/CP/sum 三个成员（以项目 A 的基线比较为准）。

## 5. 刷写

- 先完成两个基础项目的**签名旁路/刷写环境**；本仓库不提供绕过方法。
- 只刷最终生成的单个 `BODYDATA.DAT`。
- 测试：三个自定义比例分别关机开机；摇杆 AF；对焦放大进出；拍照/回放；切回原厂。
- 出问题先恢复原厂/5.01 基线，不要连续刷多个自定义包。

## 6. 常见失败

| 现象 | 原因 | 处理 |
|---|---|---|
| 找不到 `build-5.01...` | 项目 A 没有 5.01 基线 | 先恢复项目 A 的 5.01 raw-preview-magnify 构建 |
| AP/CP 哈希不对 | 基线不是预期 | 用本文件哈希对照 |
| 签名/整包失败 | 私钥/原厂输入/打包环境不对 | 回项目 A/B 的签名旁路；不要自己生成密钥 |
| 版本号被拒 | 容器编号不高于机内 | 换成任意更大的编号 |

## 7. 交付前检查

- [ ] 5.01 基线 AP/CP 哈希匹配；
- [ ] 最小最终 AP/CP 哈希匹配（`1a0480...` / `33b63...`）；
- [ ] 容器编号是任意更高编号，且已记录；
- [ ] `a7r5dat.tool.inspect(full=True)` 通过；
- [ ] 不包含 RAW zoom 探针、私钥、Sony 原厂固件；
- [ ] 明确告知用户：自定义画幅 RAW 回放放大仍未解决，未实机验证的部分不得声称已解决。