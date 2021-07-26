from pathlib import PurePath, Path
from pprint import pprint

def is_git_dir(path):
    git_dir = Path(path) / '.git'
    return git_dir.exists()

class GitDir:
    """
    Parse a path searching for all the git repositories, trying to extract parent dir and module name/dir
    """

    __do_log = True

    def __init__(self, path: str):
        self.modules = []
        cur_path = Path('')
        for part in Path(path).parts:
            cur_path /= part
            if self.__do_log: 
                print(cur_path)
            if (is_git_dir(cur_path)):
                entry = {}
                entry["abs"] = cur_path # absolute path of git repository
                entry["name"] = str(part) # by default we take the dirname to be the repository name
                if self.modules:
                    entry["name"] = str(cur_path.relative_to(self.modules[-1]["abs"]))
                if self.__do_log:
                    print("entry:")
                    pprint(entry)
                self.modules.append(entry)


