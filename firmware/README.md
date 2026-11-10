# firmware — 最小活动版本

只有 `final/`，不保留中间调试版本。

| 文件 | 作用 |
|---|---|
| `final/build_minimal.py` | 读取本项目的 OpenPano **下游**基线 AP/CP，校验后输出最小最终 AP/CP |

## 构建

把 `final` 复制为下游构建工作区 `$BUILD` 的直接子目录：

```bash
cd "$BUILD"
rm -rf ext-aspect-minimal
cp -R "$ROOT/a7r5-openpano/firmware/final" ext-aspect-minimal
cd ext-aspect-minimal
python3 build_minimal.py
```

输入 = 最终（OpenPano 下游基线已经包含扩展画幅、自制图标、RAW 预览比例修正、AF 和重启修复）：

- AP：`build-openpano/patched/appFw.so`，SHA256 `1a048077...`
- CP：`build-openpano/patched/cpapp-b.bin`，SHA256 `33b63f6b...`

默认路径在下游构建工作区；也可以用 `OPENPANO_BASELINE` 指向其他同哈希副本。OpenPano 是本项目在 A 的固件源基础上、借助 B 的工具构建的下游基线，**不是 A 的发布**。

输出：

- `ap-build/appFw-minimal.NONINSTALLABLE.so`，SHA256 `1a048077a42c538483ec9bb7f354bf7edbb1be95919cce5df299c56c4a9b0751`
- `ap-build/cpapp-minimal.NONINSTALLABLE.bin`，SHA256 `33b63f6bc300f481e1a04126e81b9b3d9e0c2db2eb178164362adb52522d8b10`

## 图标

OpenPano 下游基线的菜单/回放资源已经安装自制 2:1、65:24 图标；`assets/icons/` 是源文件/备份。2.35:1 用原厂图标。

## 未解决

自定义画幅拍摄的 RAW 在回放里按放大时仍会提示“无法放大”。AP 的 read/availability/descriptor 已成功，问题在其后的 UI/caution/显示层；本最小版本未修复，也不包含 RAW zoom 探针。

## 版本号

本仓库不分配版本号。打包时版本字段是**容器编号**，填任意比机内当前版本更新的编号即可；最终 AP/CP 哈希固定，DAT 哈希随编号变化。

详细打包/签名见 [../AI_BUILD.md](../AI_BUILD.md)。