from genelang import Genelang
import os


def auto_copy(version):
    generated_engine = Genelang.load_engine(version=version)
    ast = generated_engine.read(filepath=f"genelang/versions/{Genelang.filename(version)}.gl")
    new_engine = Genelang.ast2py(ast)
    Genelang.save_engine((version[0], version[1], f"{version[2]}_test"), new_engine)

    with open(
            file=f"genelang/versions/{Genelang.filename(version)}.py",
            mode="r",
            encoding="utf-8"
    ) as file1:
        content1 = file1.read()

    with open(
            file=f"genelang/versions/{Genelang.filename(version)}_test.py",
            mode="r",
            encoding="utf-8"
    ) as file2:
        content2 = file2.read()

    os.remove(f"genelang/versions/{Genelang.filename(version)}_test.py")

    return content1 == content2


def build_next(version_to_use, version_to_build):
    generated_engine = Genelang.load_engine(version=version_to_use)
    ast = generated_engine.read(filepath=f"genelang/versions/{Genelang.filename(version_to_build)}.gl")
    new_engine = Genelang.ast2py(ast)
    Genelang.save_engine(version_to_build, new_engine)


def rebuild_version_patchs(major, minor):
    patch = 0
    while True:
        version_at = (major, minor, patch)
        version_to = (major, minor, patch + 1)
        filename_at = Genelang.filename(version_at)
        filename_to = Genelang.filename(version_to)
        if os.path.exists(f"genelang/versions/{filename_at}.py"):
            assert auto_copy(version_at), f"The version {version_at} is not able to auto-transpile. " \
                                          f"This version is invalid !"
            if os.path.exists(f"genelang/versions/{filename_to}.gl"):
                build_next(version_at, version_to)
            else:
                print(f"File 'genelang/versions/{filename_to}.gl' not found !")
                break
        else:
            print(f"File 'genelang/versions/{filename_to}.py' not found !")
            break
        patch += 1

    print(f"All patchs built from v{major}.{minor}.0 to v{major}.{minor}.{patch} !")


if __name__ == '__main__':
    rebuild_version_patchs(1, 0)
