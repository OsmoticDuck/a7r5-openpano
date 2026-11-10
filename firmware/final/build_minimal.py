"""Minimal active extended-aspect build.

Uses the last functional baseline after the RAW preview aspect/geometry fix
(the 5.01 raw-preview-magnify base supplied by sony-a7r5-custom-firmware).
That baseline already contains the custom 2:1/65:24 icons, AF fixes, RAW
preview ratio correction and the required restart/display fixes.

No version number is assigned here. The firmware version is a container number
chosen at packaging time (any value newer than the installed one).
"""
from pathlib import Path
import hashlib, json, os

H = Path(__file__).resolve().parent
P = H.parent
BASE_AP = P / "build-5.01-magnify-20261110/patched/appFw.so"
BASE_CP = P / "build-5.01-magnify-20261110/patched/cpapp-b.bin"
BASE_AP_SHA = "1a048077a42c538483ec9bb7f354bf7edbb1be95919cce5df299c56c4a9b0751"
BASE_CP_SHA = "33b63f6bc300f481e1a04126e81b9b3d9e0c2db2eb178164362adb52522d8b10"
FINAL_AP_SHA = BASE_AP_SHA
FINAL_CP_SHA = BASE_CP_SHA


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = BASE_AP.read_bytes()
    cp = BASE_CP.read_bytes()
    assert sha(ap) == BASE_AP_SHA
    assert sha(cp) == BASE_CP_SHA
    (H / "ap-build").mkdir(exist_ok=True)
    (H / "ap-build/appFw-minimal.NONINSTALLABLE.so").write_bytes(ap)
    (H / "ap-build/cpapp-minimal.NONINSTALLABLE.bin").write_bytes(cp)
    report = dict(
        container_version=os.environ.get("FIRMWARE_VERSION", ""),
        base_AP_sha256=BASE_AP_SHA,
        final_AP_sha256=FINAL_AP_SHA,
        final_CP_sha256=FINAL_CP_SHA,
        base_is_final=True,
        active_feature="extended aspect ratios 4..6, custom icons, AF, RAW preview ratio fix and required restart/display fixes",
        icons_installed=True,
        af_frame_fix_included=True,
        raw_preview_ratio_fixed=True,
        raw_zoom_fix_included=False,
        debug_hooks_already_absent=True,
        physical_camera_tested=False,
        all_issues_fixed=False,
    )
    (H / "build-minimal.json").write_text(json.dumps(report, indent=2) + "\n")
    print(FINAL_AP_SHA)


if __name__ == "__main__":
    main()
