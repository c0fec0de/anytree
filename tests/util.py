import filecmp
import pathlib
import shutil

LEARN = False


def assert_gen(genpath, refpath):
    """Compare Generated Files Versus Reference."""
    genpath.mkdir(parents=True, exist_ok=True)
    refpath.mkdir(parents=True, exist_ok=True)
    if LEARN:  # pragma: no cover
        shutil.rmtree(refpath, ignore_errors=True)
        shutil.copytree(genpath, refpath)

    gens = [path for path in sorted(genpath.glob("**/*")) if path.is_file() and not "__pycache__" in path.parts]
    refs = [path for path in sorted(refpath.glob("**/*")) if path.is_file() and not "__pycache__" in path.parts]

    genfiles = [path.relative_to(genpath) for path in gens]
    reffiles = [path.relative_to(refpath) for path in refs]
    assert reffiles == genfiles, f"{reffiles} != {genfiles}"

    for gen, ref in zip(gens, refs):
        reftext = ref.read_text(encoding="utf-8")
        gentext = gen.read_text(encoding="utf-8")
        assert reftext == gentext
