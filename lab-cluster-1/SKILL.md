---
name: lab-cluster-1
description: "当需要在 lab cluster 1 / PJLAB 上使用开发机、rlaunch worker 或 rjob 任务时使用；覆盖交互 SSH、安全边界、路径规范、代理、CPU/GPU 分区、训练/部署、服务访问和排错，并要求使用原始 rlaunch/rjob 命令。"
---

Source: https://github.com/black-yt/skills/tree/main/lab-cluster-1 (`lab-cluster-1/`). Vendored and localized copy (2026-09-24, for the ailab-ai4solver project); authorship of the base skill remains with the upstream project.

> **本地化说明（2026-09-24）**：本 skill 由上游 lab-cluster-1 本地化为 **ailab-ai4solver** 项目使用。账号、开发机、分区、namespace、路径已替换为本机实测值（见"实测状态"）。**本机就是开发机**（workspace pod，hostname `yidong`，3 CPU / 7G 内存 / 无 GPU），Claude Code / Codex / Cursor agent 直接运行在开发机上，日常操作不需要 SSH 登录。文中仍出现的 scieval / ai4sdata "历史备份模板" 属于上游作者团队的历史，与本项目无关，仅作格式参考，不要对其提交。标注"未验证"的条目首次使用前必须先验证。

# Lab Cluster 1

## 文件导航

| 序号 | 文件内容概览 | 关键词 | 触发时机 | 文件路径 |
| --- | --- | --- | --- | --- |
| 1 | 概括开发机、CPU/GPU worker 和 rjob 的安全边界，列出禁止修改共享环境/conda/配置、不要在开发机跑重任务、必须使用原始 rlaunch/rjob、当前实测状态和提交前检查。 | lab cluster、dev host、rlaunch worker、rjob、CPU/GPU、environment safety、conda、shared config、raw commands、tested status、storage limit、no secrets | 触发本 skill 后默认读取；接触开发机/worker/rjob 前；准备跑测试、训练、部署、联网或改环境前；不确定某个操作是否会影响共享环境时读取 | `SKILL.md` |
| 2 | 说明开发机形态（本机即 workspace pod 开发机，无需 SSH）、本机路径与存储布局、conda 现状、从外部电脑 SSH 访问开发机的入口与备用 IP、文件编辑边界（`git apply`/`perl`/`sed`/备份清理）和缓存控制。 | dev machine、workspace pod、本机即开发机、SSH、ailab-ai4solver.ws、100.96.218.176、project path、storage path、`git apply --check`、unified diff、`perl -0pi`、`sed -i`、scp、tmp cleanup | 确认本机路径/存储/conda 前；从外部电脑访问开发机时；域名 SSH 连接失败时；编辑文件、应用 patch、小范围替换、清理临时文件或确认路径边界时必须读取 | [references/remote-access-and-editing.md](references/remote-access-and-editing.md) |
| 3 | 记录网络和存储资源规则，覆盖开发机/CPU/GPU 节点联网差异、代理启停、`no_proxy`、公共模型/软件目录、Hugging Face cache 格式转标准模型目录、大文件放置、缓存控制、当前 `ai4solver` 分区与历史 ai4sdata/scieval 备份模板。 | proxy、network、`setup_proxy.sh`、`no_proxy`、CPU internet、GPU no internet、shared storage、model weights、HuggingFace cache、`models--Org--Model`、`refs`、`snapshots`、standard checkpoint、large files、ai4solver、ai4solver_gpu、ai4solver_cpu、ai4sdata、scieval、partition status、legacy backup | 需要联网下载/访问 API 前；CPU/GPU 节点网络行为不确定时；选择分区前；查模型权重/公共软件路径前；发现模型目录是 Hugging Face hub cache 而不是标准 ckpt 目录时；放置大文件、缓存或排查代理/407/timeout 问题时必须读取 | [references/network-storage-resources.md](references/network-storage-resources.md) |
| 4 | 给出交互式 `rlaunch` CPU/GPU worker 的原始命令模板，包含 CPU task 分区剩余 CPU/存储查看、当前 `ai4solver_gpu`/`ai4solver_cpu` 资源配比、历史 scieval/ai4sdata 备份模板、mount、启动后检查、联网测试、GPU 检查和 worker 释放边界。 | `rlaunch`、interactive worker、CPU worker、GPU worker、predict-only、remaining CPU、storage remaining、resource ratio、mount、namespace、charged group、`nvidia-smi`、proxy test、worker cleanup、ai4solver_gpu、ai4solver_cpu、ai4sdata、scieval、legacy backup | 需要启动临时 CPU/GPU worker 前；需要查看 CPU task 分区 CPU 或存储剩余前；需要交互式测试、短任务、临时服务或资源预测时；排查 worker 资源、挂载、联网、GPU 可见性或分区参数时必须读取 | [references/rlaunch-workers.md](references/rlaunch-workers.md) |
| 5 | 提供正式 `rjob` CPU/GPU 作业模板和排错规则，覆盖当前 `ai4solver_gpu`/`ai4solver_cpu` submit/query/logs/delete、历史 ai4sdata/scieval 备份模板、脚本初始化、CUDA_HOME/CUDA_PATH/CUDACXX、conda 恢复、host-network、代理联网、1/2 GPU 资源模板、rjob/replica 结构化查询、GPU 卡位巡检，以及 rjob 任务层信息与网页监控层信息的边界。 | `rjob submit`、CPU task、GPU job、logs、delete、events、replica、CRD、status.phase、Inqueue、GPU slot、creator、pod mapping、monitoring separation、CUDA_HOME、CUDA_PATH、CUDACXX、worker_init、conda env、host-network、proxy、namespace、resource template、ai4solver_gpu、ai4solver_cpu、ai4sdata、scieval、legacy backup | 提交正式训练/部署/评测任务前；写 rjob runner 前；查询/删除/看日志前；巡检 GPU 卡位、排队任务、成员占用或排队原因前；需要把 rjob/replica 与 GPU 利用率/显存/功率等监控数据合并前；配置 CUDA/conda/代理/host-network 前；排查 job Pending/Starting/Inqueue/OOM/联网失败时必须读取 | [references/rjob-tasks.md](references/rjob-tasks.md) |
| 6 | 说明集群内网服务部署和本地访问链路，覆盖从 job 日志读取服务 IP/端口、设置 `no_proxy`、CPU/GPU 协作、KAPI 访问、任意内网服务的 SSH local port forwarding 和本地 OpenAI SDK/curl 验证。 | service deployment、internal IP、job logs、`SERVICE_IP`、`no_proxy`、CPU/GPU collaboration、KAPI、SSH local port forwarding、`ssh -L`、OpenAI SDK、curl `/v1/models`、private service | 部署模型/API/HTTP 服务后；需要从开发机/CPU worker/本地访问内网服务时；rjob 重启导致 IP 变化时；做多节点协作、端口转发、OpenAI SDK 验证或排查本地直连超时时必须读取 | [references/service-deployment-and-collaboration.md](references/service-deployment-and-collaboration.md) |
| 7 | 提供 Hugging Face hub cache 到标准模型目录的离线转换脚本，读取 `refs/<revision>` 与 `snapshots/<commit>`，把 snapshot 中的 symlink 解引用为硬链接或普通文件，输出可作为 `MODEL_PATH` 的目录。 | `hf_cache_to_model_dir.py`、Hugging Face hub cache、`models--Org--Model`、`refs/main`、`snapshots/<commit>`、symlink、hardlink、copy、`MODEL_PATH`、vLLM、Transformers、dry-run、overwrite | 公共模型路径只有 `blobs/refs/snapshots` 而没有根目录 `config.json` 时；vLLM/Transformers 不能直接读取 cache 顶层目录时；需要把公共 cache 转到大模型目录并避免重复下载时；执行大文件转换前做 dry-run 或检查 hardlink/copy 行为时必须读取 | [scripts/hf_cache_to_model_dir.py](scripts/hf_cache_to_model_dir.py) |

## 覆盖范围

- 安全边界：开发机、worker、共享环境、conda、包管理、密钥和长期配置。
- 固定信息、登录与路径：后台持久交互 SSH、单次 SSH 适用边界、公共挂载、镜像、CUDA、conda、项目根目录、大文件目录。
- 远端文件编辑：本地编辑工具边界、后台持久 SSH、标准 unified diff + `git apply`、远端编辑器、`sed`/`perl` 小替换、`scp` 传输替换和清理。
- 网络代理：开发机、CPU worker、CPU rjob、GPU 节点、私网服务和 OpenAI 相关代理边界。
- 模型权重：公共 HuggingFace 目录、大模型保存目录、cache 格式转标准模型目录、查找和迁移前检查。
- 资源任务：CPU/GPU 资源公式、当前 `ai4solver_gpu`/`ai4solver_cpu` 默认模板、ai4sdata/scieval 历史备份模板、GPU/CPU `rlaunch`、`rjob`、日志和清理。
- 服务协作：host-network、KAPI、GPU 服务 + CPU 评测、多 worker 协作和排错。

## 核心原则

- **本机就是开发机**：agent 直接运行在开发机 workspace pod 上，`cd`、编辑、提交 `rjob`、看日志全部本地直接执行，不要为日常操作建立 SSH 连接，也不要把本地文件当"远端文件"绕 SSH 编辑。SSH 入口 `ssh -CAXY yidong.luoyidong+root.ailab-ai4solver.ws@h.pjlab.org.cn`（域名异常时备用 IP `100.96.218.176`）仅用于从外部电脑访问开发机或端口转发。
- 多步操作在同一个持久 shell 会话中连续完成，不要把有状态的流程拆成一条条独立命令。
- 涉及 `rlaunch` worker 或远端服务上的文件时才考虑 SSH/scp 方式，并在同一个持久会话中操作。
- 主路径必须使用原始 `rlaunch` 和 `rjob submit` 命令。不要依赖远端 `.bashrc` 中的 `gpu`、`cpu`、`pred`、`proxy_on`、`openai_on` 等函数或 alias。
- 把开发机只当作登录、编辑、提交、监控和轻量检查入口。不要在开发机上跑训练、评测、部署、压力测试或依赖 GPU/大内存的任务；开发机联网但资源很少，高负载可能导致死机。
- `rlaunch` 申请到的 CPU/GPU 交互节点称为 worker，适合临时调试、短测试和临时服务部署。worker 可能因长时间无操作或长时间占用被释放，不适合正式长期任务。
- 正式训练、正式评测、稳定部署和长时间批处理用 `rjob submit`。
- GPU worker 和 GPU rjob 节点不可联网。需要下载、访问外部 API、联网评测或做网络中转时，使用 CPU worker/rjob，并在命令或脚本里直接写出 `setup_proxy.sh`、`no_proxy`、`env | grep -i proxy` 和联网测试。
- 使用开发机和集群时务必格外小心。默认只做任务局部、临时、可回滚的操作；严禁擅自修改长期环境、系统配置、共享配置或他人依赖的目录。
- 不要把真实 token、代理密码、API key、KAPI AK/SK 写入仓库、脚本、提交信息或最终回复。需要鉴权时从远端环境变量读取，并在输出中打码。

## 环境安全边界

- 不要自行修改开发机、worker、共享 `.bashrc`、`/etc/profile`、conda 全局配置、系统 PATH、CUDA 软链接、代理脚本、集群 CLI 配置或其他长期生效的环境设置。
- 不要自行安装系统软件、升级驱动、升级 CUDA、升级 Python/conda 基础环境、修改全局 pip/conda 源，或在共享环境中执行会影响他人的安装命令。
- 不要在 `/root`、系统目录、公共共享目录或他人项目目录中写入持久配置，除非用户明确要求并说明影响范围。
- 个人项目根目录是 `/home/luoyidong/workspace`（系统盘 100G）。代码、脚本、普通数据、日志和项目局部产物默认放在该目录下的具体项目目录中。
- 大于 5G 的数据、模型权重、缓存和中间产物放 `/data`（独立 200G 数据盘）下的合适子目录，避免占满系统盘。
- 本机没有挂载 gpfs 共享存储（`/mnt/shared-storage-*` 不存在）。`rlaunch`/`rjob` 模板里的 `--mount=gpfs://...` 卷名是占位推断、未经本团队确认；使用前必须先向团队核实真实卷名，未确认前不要假设任何共享挂载可用。
- 不要把代码、数据、权重、日志或缓存长期放入 `/tmp`、`/var/tmp` 或默认 `~/.cache`。临时文件必须用后清理，避免 `tmp`、`.cache` 等目录无限增长。
- 所有会产生大量缓存的工具都要显式指定缓存目录；小缓存放项目目录，大于 5G 的缓存或中间产物放 `/data` 下的合适子目录。
- 本机 conda 在 `/root/miniconda3`，当前只有 `base` 环境，用户尚未创建其他环境。不要重新安装 conda，不要假设任何环境名（上游的 `agent`/`llmv2`/`llm` 在本机不存在）。
- 需要新环境（含 LLM 训练/部署环境）时，先向用户说明安装位置、Python 版本、命令和可能影响，取得明确许可后再创建。
- 其他 conda 环境用途不清楚时先问用户；不要擅自创建 conda 环境、修改环境、安装/升级/卸载环境中的包。
- 需要依赖时，优先使用项目内已有环境和已有 conda 环境。确需新建环境或安装包时，先向用户说明安装位置、命令和可能影响，并取得明确许可。
- 需要改配置时，优先写到任务脚本、当前 shell 环境变量或当前 job 的局部配置中。不要把临时代理、API key、CUDA 路径、conda 设置写入长期启动文件。
- 不要清理、重命名、移动或删除共享存储中的数据、模型、环境、缓存和日志，除非用户明确指定目标路径和清理策略。
- 如果发现现有环境缺依赖、版本不匹配或配置损坏，先报告现状和建议命令；不要直接修全局环境。

## 实测状态（2026-09-24 本机验证）

已验证（在本机 workspace pod 上直接执行）：

- 本机是开发机：hostname `yidong`，FQDN `yidong.luoyidong.ailab-ai4solver.svc.pjlab.local`，K8s workspace pod（3 CPU / 7G 内存 / 无 GPU，`nvidia-smi` 不存在）。
- `rlaunch` 位于 `/kubebrain/rlaunch`，`rjob` 位于 `/usr/local/bin/rjob`；`rjob` 在非交互 shell 中需要先执行 `source /etc/profile.d/ssh-init.sh 2>/dev/null || true`。
- CPU 分区 charged group 是 `ai4solver_cpu`（**注意：不是 `ai4solver_cpu_task`**，后者返回 403 Forbidden）：`rlaunch --charged-group=ai4solver_cpu --predict-only` 可用，返回全部 CPU 节点剩余 CPU/内存。
- GPU 分区 charged group 是 `ai4solver_gpu`：predict-only 通过鉴权（组名有效）；2026-09-24 测试时返回"资源不足，无可用机器"，当时无空闲 GPU 机器，不代表组名错误。
- namespace 是 `ailab-ai4solver`：本机环境变量 `KUBEBRAIN_NAMESPACE` 已设置，`KUBEBRAIN_QUOTA_GROUP=ai4solver_cpu`；`rjob list`（空结果）可用。
- 代理：本机环境变量已配置 `http_proxy/https_proxy = http://httpproxy-headless.kubebrain.svc.pjlab.local:3128` 及 `no_proxy`，开发机上联网开箱即用；worker / rjob 内仍需按模板自行配置代理。
- 存储布局：`/` 100G（系统 + home），`/data` 200G 独立数据盘，`/jobutils` 只读集群工具（含 `scripts/worker_init.sh`）。本机无 gpfs 共享存储挂载，`/mnt/shared-storage-*` 不存在。
- conda：`/root/miniconda3` 存在，仅有 `base` 环境。

未验证（首次使用前先确认，不要当成已知事实）：

- 从外部电脑 SSH 登录入口 `yidong.luoyidong+root.ailab-ai4solver.ws@h.pjlab.org.cn` 和备用 IP `100.96.218.176`（本机即开发机，日常用不到）。
- `--mount=gpfs://gpfs1/luoyidong`、`gpfs://gpfs2/ai4solver`、`gpfs2-shared-public` 等挂载卷名是否属于本团队。向团队确认后再用；错误卷名会导致 worker 启动失败或看不到数据。没有共享存储时，worker/rjob 无法直接读取本机 `/home` 和 `/data` 里的代码数据，提交前先解决存储问题。
- GPU rjob / GPU worker 真实提交与调度（当时无空闲 GPU 机器）。
- 镜像 `registry.h.pjlab.org.cn/ailab/ml-base:22.04-pjlab` 在本团队的可用性；CUDA 公共路径在本机的对应位置。
- CPU worker / CPU rjob 内的代理与外网连通性（模板来自上游，未在本团队复测）。

上游历史记录：原文 2026-05 ~ 2026-08 的 scieval / ai4sdata 分区切换与实测记录属于上游作者团队，与本项目无关，已从本节移除；对应模板只作格式参考。

关键边界：

- CPU rjob 外网任务使用 `--host-network=false`。`--host-network=true` 下代理访问外网返回 `407 Proxy Authentication Required`，不要用于 CPU rjob 外网任务。
- 当前 `rlaunch` CPU worker 优先使用 `ai4solver_cpu` + `--namespace=ailab-ai4solver`。
- 当前 CPU rjob 优先使用 `ai4solver_cpu` + `--namespace=ailab-ai4solver`；非交互 shell 查询、日志和删除时如遇权限问题，显式加 `KUBEBRAIN_NAMESPACE=ailab-ai4solver` 前缀。
- 当前 GPU `rlaunch`/`rjob` 优先使用 `ai4solver_gpu` + `--namespace=ailab-ai4solver`；正式使用前先做 predict-only、dry-run 或最小短任务验证。
- 文中的 ai4sdata / scieval 模板是上游作者团队的历史备份模板，与本项目无关，不要提交；除非用户明确说明本团队也有这些分区并验证过。

## 提交前检查

- 真实申请 `rlaunch` worker 或提交 `rjob` 前，先向用户说明会占用的 CPU/GPU/memory 和预计持续时间。
- 任务是否真的需要 GPU；能用 CPU 解决的联网任务不要占 GPU。
- 是短测试还是正式任务；短测试用 `rlaunch`，正式任务用 `rjob submit`。
- GPU 数是否和 CPU/memory 匹配。
- 分区是否正确：2026-08-11 当前 rlaunch/rjob 默认使用 GPU `ai4solver_gpu` / CPU `ai4solver_cpu` + `--namespace=ailab-ai4solver`；查询、日志和删除 ai4solver rjob 时加 `KUBEBRAIN_NAMESPACE=ailab-ai4solver`；ai4sdata/scieval 只作为历史备份模板，不作为默认提交目标。
- GPU 任务是否完全不依赖外网。
- `command.sh` 是否位于共享存储，且没有硬编码 secret。
- 代码、脚本和普通项目数据是否位于 `/home/luoyidong/workspace/<project>`。
- 大于 5G 的数据或权重是否位于 `/data/<project>` 的合适子目录。
- 是否避免使用 `/tmp`、`/var/tmp`、worker 本地盘或默认 `~/.cache` 存放长期内容。
- 是否为临时目录设置了退出清理逻辑，例如 `trap 'rm -rf "$RUN_TMP"' EXIT`。
- 是否显式设置了缓存目录，避免工具把大缓存写进默认 home cache。
- 服务是否监听 `0.0.0.0`，端口是否和客户端 URL 一致。
- 私网 URL 是否绕过代理。
- 日志输出是否会泄露 API key、代理认证、KAPI AK/SK。
- `rlaunch` 测试命令必须自动退出，除非用户明确要求进入交互 worker。
- `rjob` 测试任务结束后必须用 `rjob delete` 清理。

## 排错

- `gpu: command not found` 或 `cpu: command not found`：不要修 `.bashrc`，直接使用本 skill 中的原始 `rlaunch` 命令。
- 非交互 SSH 没加载 alias/function：这是正常现象。`.bashrc` 常见写法会在非交互 shell 中提前 return。
- `rlaunch` 申请失败：先跑对应资源的 `rlaunch --predict-only`，再降低 CPU/memory/GPU 或换分区。
- `unknown charged-group` 或 namespace 相关错误：核对当前分区矩阵；2026-08-11 默认使用 CPU `ai4solver_cpu` 或 GPU `ai4solver_gpu` 且必须带 `--namespace=ailab-ai4solver`；ai4solver rjob 查询、日志和删除需要临时前缀 `KUBEBRAIN_NAMESPACE=ailab-ai4solver`。ai4sdata/scieval 是历史备份模板，只有用户确认回退或资源恢复后再按对应 namespace 使用。
- GPU 节点下载失败：预期行为。改用 CPU worker 下载到共享存储，或提前准备镜像/环境。
- GPU rjob 里 `flashinfer`、`ninja`、CUDA extension build、`nvcc not found`、`CUDA_HOME not set` 报错：不要只看开发机或 submit host 的 CUDA 路径。进入 rjob 日志或 worker 内检查 `echo "$CUDA_HOME"`、`echo "$CUDA_PATH"`、`echo "$CUDACXX"`、`test -x "$CUDACXX"`、`which nvcc`、`nvcc --version`。如果脚本 source 了 `/jobutils/scripts/worker_init.sh`，确认之后又恢复了 `CUDA_HOME`、`CUDA_PATH`、`CUDACXX`、`PATH` 和 conda env。
- 外部 API 调用失败：确认任务是否在 CPU 节点；GPU 节点不可联网。
- CPU rjob 外网返回 407：先检查提交命令是否误用了 `--host-network=true`；外网任务改用 `--host-network=false`，job 内 `sleep 5` 后再配置代理。
- 私网服务访问失败：检查服务是否监听 `0.0.0.0`、端口是否开放、URL 是否用了正确 worker id 或私网 IP、私网地址是否在 `no_proxy`。
- 训练 OOM：先降低 batch、sequence length、并发生成数或改用更多 GPU；再按资源公式调整 CPU/memory。
- worker 被释放：`rlaunch` 不适合长期运行；改用 `rjob submit`。
