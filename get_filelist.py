import os
import re
import git

from collections.abc import Generator

def get_files_from_git(root: git.objects.tree.Tree, level: int = 0, extension: str = None) -> Generator[str, None, None]:
    """
        ファイルツリーの再帰探索関数
        <Params>
        root (git.objects.tree.Tree) : 探索対象のディレクトリ（treeオブジェクト）
        level (int) : ファイルツリーの深さのカウント（デバッグ用）
        extension (str) : 取得したいファイルの拡張子（Noneであれば全て取得）
        
        <Return>
        Generator（Iterator）: ファイルパス
    """
    
    # 対象ディレクトリに含まれるオブジェクトを取り出す
    for entry in root:
        
        # print(f'{"-" * 4 * level}| {entry.path}, {entry.type}') # DEBUG
        
        if entry.type == "tree":
            # 対象オブジェクトが"tree"（ディレクトリ）であるときはさらに探索
            yield from get_files_from_git(entry, level+1, extension=extension)
            
        elif entry.type == "blob":
            # 対象オブジェクトが"blob"（ファイル）であるときはパスを取得
            if extension is None:
                # 取得したいファイルの拡張子に指定がなければ全て取得
                yield entry.path
            else:
                # 取得したいファイルの拡張子に指定があれば一致するか判定
                if extension in os.path.splitext(entry.path)[1]:
                    yield entry.path
                else:
                    pass
            
            
if __name__ == '__main__':
    
    # How to use
    repo = git.Repo('C:\\Users\森壮平\\Desktop\\gitpyiter\\cloned_project\\RWKV-LM')
    for commit in repo.iter_commits():
        root: git.objects.tree.Tree = commit.tree
        files = get_files_from_git(root=root, extension='.py')
        for file in files:
            print(file)
        exit(0) # DEBUG