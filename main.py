from genelang import Genelang
import os


def auto_transpile(version):
    """
        using `genelang_<M>_<m>_<p>.py` on `genelang_<M>_<m>_<p>.gl`,
        do we still obtain `genelang_<M>_<m>_<p>.py` ?
        NB : this will create and remove `genelang_<M>_<m>_<p>_test.py` to check equivalence !
    :param version: (<M>, <m>, <p>)
    :return:
    """
    Genelang.build_engine(lang="genelang", version=version, gl_version=version, tag="test")

    filepath1 = Genelang.make_filepath(lang="genelang", version=version, type="python")
    with open(file=filepath1, mode="r", encoding="utf-8") as file1:
        content1 = file1.read()

    filepath2 = Genelang.make_filepath(lang="genelang", version=version, type="python", tag="test")
    with open(file=filepath2, mode="r", encoding="utf-8") as file2:
        content2 = file2.read()

    os.remove(filepath2)

    return content1 == content2


def rebuild_version_patchs(major, minor):
    patch = 0
    while True:
        version_at = (major, minor, patch)
        version_to = (major, minor, patch + 1)

        filepath_at_py = Genelang.make_filepath(lang="genelang", version=version_at, type="python")
        filepath_to_gl = Genelang.make_filepath(lang="genelang", version=version_to, type="genelang")

        if os.path.exists(filepath_at_py):
            assert auto_transpile(version_at), f"The version {version_at} is not able to auto-transpile. " \
                                          f"This version is invalid !"
            if os.path.exists(filepath_to_gl):
                Genelang.build_engine(lang="genelang", version=version_to, gl_version=version_at)
            else:
                print(f"File '{filepath_to_gl}' not found !")
                break
        else:
            print(f"File '{filepath_at_py}' not found !")
            break
        patch += 1

    print(f"All patchs built from v{major}.{minor}.0 to v{major}.{minor}.{patch} !")


if __name__ == '__main__':
    rebuild_version_patchs(1, 0)
