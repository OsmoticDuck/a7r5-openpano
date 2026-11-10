# firmware — 最小活动版本

只有 `final/`，不保留中间调试版本。

| 文件 | 作用 |
|---|---|
| `final/build_minimal.py` | 读取项目 A 的 4.92 quality-menu 基线 AP/CP，校验后输出最小最终 AP/CP |

## 构建

把 `final` 复制为 `$CUSTOM` 的直接子目录：

```bash
cd "$CUSTOM"
rm -rf ext-aspect-minimal
cp -R "$ROOT/a7r5-openpano/firmware/final" ext-aspect-minimal
cd ext-aspect-minimal
python3 build_minimal.py
```

输入 = 最终（4.92 基线已经包含扩展画幅、自制图标、AF 和重启修复）：

- AP：`build-4.92-quality-menu-20261105/patched/appFw.so`，SHA256 `d1786165...`
- CP：`build-4.92-quality-menu-20261105/patched/cpapp-b.bin`，SHA256 `feececdc...`

输出：

- `ap-build/appFw-minimal.NONINSTALLABLE.so`，SHA256 `d17861657b062d4228ea74b31844bf7476cd82e3530c36b9b201f930c3df432f`
- `ap-build/cpapp-minimal.NONINSTALLABLE.bin`，SHA256 `feececdcfdfff740324327eadedc863fc293e136b9b1db91cc8bc4e222f550c4`

## 图标

4.92 基线的菜单/回放资源已经安装自制 2:1、65:24 图标；`assets/icons/` 是源文件/备份。2.35:1 用原厂图标。

## 未解决

自定义画幅拍摄的 RAW 在回放里按放大时仍会提示“无法放大”。AP 的 read/availability/descriptor 已成功，问题在其后的 UI/caution/显示层；本最小版本未修复，也不包含 RAW zoom 探针。

## 版本号

本仓库不分配版本号。打包时版本字段是**容器编号**，填任意比机内当前版本更新的编号即可；最终 AP/CP 哈希固定，DAT 哈希随编号变化。

详细打包/签名见 [../AI_BUILD.md](../AI_BUILD.md)。
