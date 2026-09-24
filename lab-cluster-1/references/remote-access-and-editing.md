# Remote Access And Editing（本地化：本机即开发机）

## 本机就是开发机

- 本机是开发机：hostname `yidong`，FQDN `yidong.luoyidong.ailab-ai4solver.svc.pjlab.local`，一个 K8s workspace pod，资源 3 CPU / 7G 内存 / 无 GPU。
- Claude Code / Codex / Cursor agent 通常直接运行在这台开发机上：`cd`、编辑文件、提交 `rjob`、查看日志全部本地直接执行，**不需要也不应该**为日常操作建立 SSH 连接，不要把本地文件当"远端文件"绕 SSH/scp 编辑。
- 开发机资源很少且无 GPU：只做编辑、提交、监控和轻量检查。训练、评测、部署、压力测试走 `rlaunch` worker 或 `rjob submit`。
- 本机环境变量已带代理（`http_proxy`/`https_proxy` = `http://httpproxy-headless.kubebrain.svc.pjlab.local:3128`，含 `no_proxy`），联网开箱即用；GPU worker / GPU rjob 节点不可联网的规则仍然适用。

## 从外部电脑访问开发机（仅外部需要）

```bash
ssh -CAXY yidong.luoyidong+root.ailab-ai4solver.ws@h.pjlab.org.cn
```

`h.pjlab.org.cn` 域名连接失败、DNS 解析异常时，保持相同用户把目标主机临时换成开发机 IP（未在本账号复测）：

```bash
ssh -CAXY yidong.luoyidong+root.ailab-ai4solver.ws@100.96.218.176
```

一次性健康检查适合单次 SSH：

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 -o ServerAliveInterval=5 -o ServerAliveCountMax=1 \
  -CAXY yidong.luoyidong+root.ailab-ai4solver.ws@h.pjlab.org.cn \
  'hostname; command -v rlaunch; command -v rjob'
```

这只是 SSH 入口的备用连接方式。`rjob` 日志里的服务 IP、worker 内网 IP、KAPI URL 和 `ssh -L` 转发目标仍按对应章节从日志或实际服务信息获取，不要用这个入口 IP 代替服务 IP。端口转发（`ssh -N -T -L`）见 [service-deployment-and-collaboration.md](service-deployment-and-collaboration.md)。

## 本机路径与存储（2026-09-24 实测）

| 用途 | 路径 | 说明 |
| --- | --- | --- |
| 个人项目根 | `/home/luoyidong/workspace` | 系统盘（100G）；现有 `docker/`、`jupyter/`、`llm-milp-gen/` 等 |
| 大文件（>5G）、权重、大缓存 | `/data` | 独立 200G 数据盘 |
| 集群工具（只读） | `/jobutils` | `scripts/worker_init.sh` 等 |
| 共享存储 | **无 gpfs 挂载** | `/mnt/shared-storage-*` 不存在；worker `--mount` 卷名需向团队确认 |

缓存控制模板：

```bash
PROJECT_DIR="/home/luoyidong/workspace/<project>"
BIG_DIR="/data/<project>"
mkdir -p "$PROJECT_DIR" "$BIG_DIR"

# 小型项目缓存。不要使用默认 ~/.cache。
export XDG_CACHE_HOME="$PROJECT_DIR/.cache"
export HF_HOME="$PROJECT_DIR/.cache/huggingface"
export TRANSFORMERS_CACHE="$HF_HOME/transformers"
export HF_DATASETS_CACHE="$HF_HOME/datasets"

# 大于 5G 的缓存、数据或权重改放 BIG_DIR，并在命令结束后检查容量。
# export HF_HOME="$BIG_DIR/huggingface"

# 必须用临时目录时，只放任务内短生命周期文件，并确保退出时清理。
RUN_TMP="$PROJECT_DIR/.tmp/run-$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$RUN_TMP"
trap 'rm -rf "$RUN_TMP"' EXIT
```

## conda

- 本机 conda 在 `/root/miniconda3`，当前只有 `base` 环境；用户尚未创建其他环境。
- 不要重新安装 conda，不要假设任何环境名（上游作者的 `agent` / `llmv2` / `llm` 在本机不存在）。
- 新建环境或装包前，先向用户说明安装位置、Python 版本、命令和影响，征得明确许可。

## 文件编辑边界（本机直接编辑）

- 项目是 git repo 时，用 `git status` / `git diff` 检查改动；非 git 目录用 `diff -u` 前后备份检查，检查后删除备份。
- 所有临时文件放目标项目自己的 `.tmp` 子目录，文件名带任务名或时间戳；任务结束必须删除，不要塞进系统 `/tmp`、`/var/tmp`。
- 少量机械替换可用 `perl` 或 `sed`，但只适合非常小、确定、唯一匹配、可立即校验的替换：

```bash
cd /home/luoyidong/workspace/<project>
TARGET_FILE="path/to/file"
BACKUP_FILE="${TARGET_FILE}.bak.$(date +%Y%m%d-%H%M%S)"
cp "$TARGET_FILE" "$BACKUP_FILE"

grep -n "OLD_TEXT" "$TARGET_FILE"
perl -0pi -e 's/OLD_TEXT/NEW_TEXT/g' "$TARGET_FILE"
diff -u "$BACKUP_FILE" "$TARGET_FILE" || true
rm -f "$BACKUP_FILE"
```

`perl`/`sed` 使用边界：

- 替换前先 `grep` 确认匹配对象唯一或所有匹配都应修改；替换后立即 `git diff -- <file>` 或 `diff -u backup file`。
- 不要用它们做多文件复杂改动、代码重构或结构性编辑；这种情况用编辑器或 patch。
- 不要在不理解正则转义、换行、贪婪匹配影响时使用 `perl -0pi`。

- 往 worker / 其他机器传 patch 时，patch 必须是标准 unified diff（`git diff` 生成的 `diff --git` / `---` / `+++` / `@@` 格式）。不要把 Codex `apply_patch` 工具专用的 `*** Begin Patch` / `*** Update File` 格式传给远端 `git apply`，标准 `git apply` 不认识这种格式。应用前先 `git apply --check`。

## 与 worker / rjob 的文件关系

- 本机 `/home` 和 `/data` 是 workspace pod 自己的卷，**worker 默认看不到**。worker 需要的代码和数据要通过 `--mount` 挂共享存储解决；本团队可用的 gpfs 卷名尚未确认（见 SKILL.md 实测状态"未验证"）。
- 确认共享存储前，不要设计"在 worker 里改文件/读项目目录"的流程；优先先解决存储问题再提交任务。
