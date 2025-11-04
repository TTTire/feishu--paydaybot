# Git 常用命令速查表

## 📋 基础操作

### 查看状态
```bash
git status          # 查看工作区状态
git log             # 查看提交历史
git log --oneline   # 简洁版提交历史
git diff            # 查看未暂存的修改
git diff --staged   # 查看已暂存的修改
```

### 添加和提交
```bash
git add <file>              # 添加指定文件到暂存区
git add .                   # 添加所有修改到暂存区
git commit -m "提交信息"     # 提交暂存区的修改
git commit -am "提交信息"    # 添加并提交所有修改（仅限已跟踪文件）
```

## 🔄 版本回滚

### 1. 撤销未提交的修改
```bash
git restore <file>          # 撤销工作区的修改
git restore --staged <file> # 取消暂存区的修改
git checkout -- <file>      # 旧版语法，功能相同
```

### 2. 回滚到指定版本
```bash
git reset --hard <commit-id>    # 硬回滚：删除之后的所有提交
git reset --soft <commit-id>    # 软回滚：保留修改，重新暂存
git reset --mixed <commit-id>   # 混合回滚：保留修改，不暂存（默认）
```

### 3. 查找丢失的提交
```bash
git reflog                      # 查看所有操作历史
git fsck --lost-found           # 查找丢失的对象
```

## 🌿 分支操作

### 分支管理
```bash
git branch                      # 查看本地分支
git branch -r                   # 查看远程分支
git branch -a                   # 查看所有分支
git branch <branch-name>        # 创建新分支
git checkout <branch-name>      # 切换分支
git checkout -b <branch-name>   # 创建并切换到新分支
git branch -d <branch-name>     # 删除本地分支
git branch -D <branch-name>     # 强制删除分支
```

### 分支合并
```bash
git merge <branch-name>         # 合并指定分支到当前分支
git merge --no-ff <branch-name> # 不使用快进方式合并
git cherry-pick <commit-id>     # 挑选指定提交到当前分支
```

## 🔄 远程操作

### 远程仓库
```bash
git remote -v                   # 查看远程仓库
git remote add <name> <url>     # 添加远程仓库
git remote remove <name>        # 删除远程仓库
git fetch <remote>              # 获取远程更新
git pull <remote> <branch>      # 拉取并合并远程更新
git push <remote> <branch>      # 推送到远程仓库
git push -u <remote> <branch>   # 首次推送并设置上游分支
```

## 🏷️ 标签操作

```bash
git tag                         # 查看所有标签
git tag <tag-name>              # 创建轻量标签
git tag -a <tag-name> -m "说明"  # 创建附注标签
git push --tags                 # 推送所有标签
git push origin <tag-name>      # 推送指定标签
```

## 🔍 查看和比较

```bash
git show <commit-id>            # 查看指定提交的详细信息
git show --name-only <commit-id> # 只查看文件列表
git blame <file>                # 查看文件的每行修改信息
git log --graph --oneline --all # 图形化显示提交历史
git log --grep="关键词"         # 搜索提交信息
```

## 🚨 危险操作（谨慎使用）

```bash
# 永久删除提交历史
git reset --hard HEAD~1         # 删除最近一次提交
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch <file>' \
  --prune-empty --tag-name-filter cat -- --all  # 从历史中删除文件

# 强制推送（会覆盖远程历史）
git push --force-with-lease <remote> <branch>
git push -f <remote> <branch>   # 强制推送（更危险）
```

## 💡 实用技巧

### 提交信息规范
```bash
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

### 暂存当前工作
```bash
git stash                        # 暂存当前修改
git stash list                   # 查看暂存列表
git stash apply                  # 应用最新的暂存
git stash pop                    # 应用并删除最新的暂存
git stash clear                  # 清除所有暂存
```

### 交互式变基
```bash
git rebase -i HEAD~3             # 交互式变基最近3个提交
# 编辑指令：
# pick: 保留提交
# reword: 修改提交信息
# edit: 编辑提交
# squash: 合并到上一个提交
# drop: 删除提交
```

## 📝 工作流程建议

### 1. 功能开发流程
```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 开发和提交
git add .
git commit -m "feat: 实现新功能"

# 3. 推送分支
git push origin feature/new-feature

# 4. 合并到主分支
git checkout main
git merge feature/new-feature
git push origin main

# 5. 删除功能分支
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### 2. 提交前检查
```bash
# 查看将要提交的内容
git diff --staged

# 查看提交历史
git log --oneline -5

# 确认无误后提交
git commit -m "详细的提交信息"
```

---

**⚠️ 重要提示：**
- 在使用 `reset --hard` 前请确保已备份重要修改
- 强制推送 (`git push -f`) 在团队协作中要谨慎使用
- 定期推送到远程仓库作为备份
- 使用有意义的提交信息，便于团队协作和代码维护