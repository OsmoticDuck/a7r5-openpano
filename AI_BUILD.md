# AI_BUILD.md — 给 AI 的最小扩展画幅编译/打包清单

目标：在 **sony-a7r5-custom-firmware** 与 **a7r5-rea** 两个基础项目已经能完成签名旁路/打包的前提下，构建**最小活动版本**的扩展画幅固件。

> 本仓库只保留实现扩展画幅所需的最小功能，不展开中间调试版本。先读 [README.md](README.md)。

## 0. 路径

```
$ROOT/
  sony-a7r5-custom-firmware/          # 基础项目 A（固件/签名/打包）
  a7r5/a7r5-rea/                      # 基础项目 B（DAT 工具/引擎/独立校验）
  a7r5/direct-p1-read-20261031/       # 分析依赖
  a7r5-openpano/               # 本仓库
```

- `$CUSTOM` = `$ROOT/sony-a7r5-custom-firmware`
- `$REA` = `$ROOT/a7r5/a7r5-rea`

## 1. 基础项目负责什么

### 1.1 sony-a7r5-custom-firmware（项目 A）

- 原厂/自定义固件提取、打包、FDAT/RSA 签名、AES 整包；
- 项目 A 的**最后功能基线**（本仓库的 `build_minimal.py` 读取它的 `patched/appFw.so` 和 `patched/cpapp-b.bin`）；
- `feature-extension-436/result/source`、`package.py`/现有 package 脚本；
- 原厂 DAT、升级器、公私钥、原始输入。

### 1.2 a7r5-rea（项目 B）

- `source/a7r5-dat-tool`：`a7r5dat.tool.inspect`；
- `A7R5-Studio-0.1.0-mac-arm64-test/.../engine/site`：打包/镜像运行环境；
- 相机侧执行/读取环境（本构建不需要连接相机）。

**签名旁路/密钥不在本仓库**。项目 A 的 `private.pem`、`updater.img`、`original.DAT`、`public.pem`、`sony_public.pem` 必须由使用者按项目 A 的说明准备。

## 2. 输入

| 输入 | 路径（相对 `$CUSTOM`） | SHA256 |
|---|---|---|
| 最后功能基线 AP | `build-4.85-liveview-20261104/patched/appFw.so` | `9f947f68bec0d6a5140a5d31078ed5cdda920c7b25c656fb619d953eb4833e7a` |
| 最后功能基线 CP | `build-4.85-liveview-20261104/patched/cpapp-b.bin` | `1bcdddcff45ac551d36f0992955e2ffb0c1c54c3d12d3f0c37d0cfb306146f84` |

最小最终产物（固定）：

| 产物 | SHA256 |
|---|---|
| 最小最终 AP | `e9b58ccb6fdc76789743eb1fe94ae22760c7f707f0b61c036a06e128a0b19f1f` |
| 最小最终 CP | `1bcdddcff45ac551d36f0992955e2ffb0c1c54c3d12d3f0c37d0cfb306146f84` |

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

1. 读取项目 A 的最后功能基线 AP/CP；
2. 恢复并关闭 5 个有界异常记录器钩子 + 1 个 AF RAM 观察器钩子（这些不是扩展画幅所必需）；
3. 输出 `ap-build/appFw-minimal.NONINSTALLABLE.so`（`e9b58c...`）和 `ap-build/cpapp-minimal.NONINSTALLABLE.bin`（`1bcddd...`）。

调试钩子关闭后，基础镜像里的死代码仍在，但没有活动调用；完整删除死代码需要重新链接，本仓库未提供。

## 4. 打包/签名/容器编号

使用项目 A 现有的 package 流程（以项目 A 最后功能版本的 `package` 脚本为模板），把 AP/CP 输入替换为：

```
ap-build/appFw-minimal.NONINSTALLABLE.so
ap-build/cpapp-minimal.NONINSTALLABLE.bin
```

并更新打包元数据中的 `AP_sha256` / `CP_sha256`。

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
- 测试：三个自定义比例分别关机开机；进入/退出 MF；拍照/回放；切回原厂。
- 出问题先恢复原厂/最后功能基线，不要连续刷多个自定义包。

## 6. 常见失败

| 现象 | 原因 | 处理 |
|---|---|---|
| 找不到 `build-4.85...` | 项目 A 没有最后功能基线 | 先恢复项目 A 的最后功能基线 |
| 基线 AP/CP 哈希不对 | 基线不是预期 | 用本文件哈希对照 |
| 最终 AP 哈希不对 | 钩子恢复位置/当前值不对 | 确认 6 个站点的当前/原始值 |
| 签名/整包失败 | 私钥/原厂输入/打包环境不对 | 回项目 A/B 的签名旁路；不要自己生成密钥 |
| 版本号被拒 | 容器编号不高于机内 | 换成任意更大的编号 |

## 7. 交付前检查

- [ ] 基线 AP/CP 哈希匹配；
- [ ] 最小最终 AP/CP 哈希匹配（`e9b58c...` / `1bcddd...`）；
- [ ] 容器编号是任意更高编号，且已记录；
- [ ] `a7r5dat.tool.inspect(full=True)` 通过；
- [ ] 不包含 RAW 放大/弹窗探针、私钥、Sony 原厂固件；
- [ ] 明确告知用户：AF 框修正不在本最小版本内，未实机验证的部分不得声称已解决。