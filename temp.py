import os

def moveTree(sourceRoot, destRoot):
    print(sourceRoot)
    print(destRoot)
    if not os.path.exists(destRoot):
        return False
    ok = True
    for path, dirs, files in os.walk(sourceRoot):
        relPath = os.path.relpath(path, sourceRoot)
        destPath = os.path.join(destRoot, relPath)
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for file in files:
            destFile = os.path.join(destPath, file)
            if os.path.isfile(destFile):
                print("Skipping existing file: " + os.path.join(relPath, file))
                ok = False
                continue
            srcFile = os.path.join(path, file)
            print("rename", srcFile, destFile)
            os.rename(srcFile, destFile)
    for path, dirs, files in os.walk(sourceRoot, False):
        if len(files) == 0 and len(dirs) == 0:
            os.rmdir(path)
    return ok

for item in [r"dist\relaykeysd-service",r"dist\relaykeys-cli",r"dist\relaykeys-cli-win",r"dist\relaykeys-qt"]:
    moveTree(item, r'dist\relaykeysd')