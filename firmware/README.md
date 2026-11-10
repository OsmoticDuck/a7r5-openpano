# firmware — 最小活动版本

只有 `final/`，不保留中间调试版本。

| 文件 | 作用 |
|---|---|
| `final/build_minimal.py` | 在项目 A 的最后功能基线上关闭不属于扩展画幅的调试钩子，输出最小最终 AP/CP |

## 构建

把 `final` 复制为 `$CUSTOM` 的直接子目录：

```bash
cd "$CUSTOM"
rm -rf ext-aspect-minimal
cp -R "$ROOT/a7r5-openpano/firmware/final" ext-aspect-minimal
cd ext-aspect-minimal
python3 build_minimal.py
```

输入（项目 A 的最后功能基线）：

- AP：`build-4.85-liveview-20261104/patched/appFw.so`，SHA256 `9f947f68...`
- CP：`build-4.85-liveview-20261104/patched/cpapp-b.bin`，SHA256 `1bcdddcf...`

输出：

- `ap-build/appFw-minimal.NONINSTALLABLE.so`，SHA256 `e9b58ccb6fdc76789743eb1fe94ae22760c7f707f0b61c036a06e128a0b19f1f`
- `ap-build/cpapp-minimal.NONINSTALLABLE.bin`，SHA256 `1bcdddcff45ac551d36f0992955e2ffb0c1c54c3d12d3f0c37d0cfb306146f84`

脚本关闭的钩子：

- 有界异常记录器的 assert/fatal/request/set/sequence 五个入口；
- AF RAM 观察器入口。

这些不是扩展画幅的必要条件；关闭后不产生调试文件 IO。基础镜像中的死代码仍在，但没有活动调用；完整删除需要重新链接，本仓库未提供。

## 版本号

本仓库不分配版本号。打包时版本字段是**容器编号**，填任意比机内当前版本更新的编号即可；最终 AP/CP 哈希固定，DAT 哈希随编号变化。

详细打包/签名见 [../AI_BUILD.md](../AI_BUILD.md)。
