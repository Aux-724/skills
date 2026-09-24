# Rlaunch Workers

> **2026-09-24 本机实测**：本团队 CPU 分区是 `ai4solver_cpu`（不是 `ai4solver_cpu_task`，后者 403 Forbidden），GPU 分区是 `ai4solver_gpu`（当时无空闲机器）；namespace `ailab-ai4solver`（本机 env 已设 `KUBEBRAIN_NAMESPACE`）。模板中的 `--mount=gpfs://...` 卷名为占位推断、未经本团队确认，提交前必须先向团队核实真实卷名。文中 scieval / ai4sdata 模板是上游作者团队的历史备份，与本项目无关。

## rlaunch 资源检查

先在开发机交互 shell 中检查。只做资源预测时不会启动 worker：

```bash
# 只查看当前 CPU task 分区的 CPU 和存储剩余，不申请具体 worker。
rlaunch --charged-group=ai4solver_cpu --predict-only

# 2026-08-11 当前默认 CPU/GPU worker 检查。
rlaunch --cpu=4 --memory=16000 --charged-group=ai4solver_cpu --namespace=ailab-ai4solver --predict-only
rlaunch --cpu=8 --memory=32000 --charged-group=ai4solver_cpu --namespace=ailab-ai4solver --predict-only
rlaunch --gpu=1 --cpu=22 --memory=230000 --charged-group=ai4solver_gpu --private-machine=group --namespace=ailab-ai4solver --predict-only
rlaunch --gpu=2 --cpu=44 --memory=460000 --charged-group=ai4solver_gpu --private-machine=group --namespace=ailab-ai4solver --predict-only

# 2026-06-05 备份 CPU worker 检查；2026-08-11 起不作为默认分区。
rlaunch --cpu=4 --memory=16000 --charged-group=scieval_cpu_task --namespace=ailab-scieval --predict-only
rlaunch --cpu=8 --memory=32000 --charged-group=scieval_cpu_task --namespace=ailab-scieval --predict-only

# ai4sdata 历史备份；仅在资源恢复并得到用户确认后使用。
rlaunch --cpu=4 --memory=16000 --charged-group=ai4sdata_cpu_task --predict-only
rlaunch --gpu=1 --cpu=22 --memory=230000 --charged-group=ai4sdata_gpu --private-machine=group --predict-only

# scieval GPU 历史备份；是否可用仍需单独检查。
rlaunch --gpu=1 --cpu=22 --memory=230000 --charged-group=scieval_gpu --private-machine=group --namespace=ailab-scieval --predict-only
```

`rlaunch --charged-group=ai4solver_cpu --predict-only` 用于快速查看 CPU task 分区整体剩余 CPU 和存储资源；带 `--cpu` / `--memory` / `--gpu` 的 predict-only 用于判断某个具体资源申请能否调度。先用预测命令看调度结果；如果 GPU 返回资源不足或不可调度，不要循环提交或长期占用开发机轮询。

## rlaunch CPU Worker

真实交互使用时把末尾命令写成 `-- bash`。需要做短检查时，可以把末尾命令改成 `-- bash -lc '...'`，让 worker 自动退出，避免留下空闲资源。

2026-08-11 当前默认 CPU worker 使用 `ai4solver_cpu` + `--namespace=ailab-ai4solver`。旧 `scieval_cpu_task` 和 `ai4sdata_cpu_task` 模板只作为历史备份保留，不要删除；回退前先做 predict-only 和最小短任务验证。

ai4solver 4 CPU，当前默认模板：

```bash
rlaunch \
  --cpu=4 \
  --memory=16000 \
  --charged-group=ai4solver_cpu \
  --namespace=ailab-ai4solver \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=5m \
  -- bash -lc 'echo worker_host=$(hostname); echo nproc=$(nproc); test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok; test -d /mnt/shared-storage-user/ai4solver && echo mount_ai4solver_ok; test -d /mnt/shared-storage-gpfs2/gpfs2-shared-public && echo mount_public_ok; test -d /mnt/shared-storage-gpfs2/ai4solver && echo mount_ai4solver_ok'
```

ai4solver 8 CPU，当前默认模板：

```bash
rlaunch \
  --cpu=8 \
  --memory=32000 \
  --charged-group=ai4solver_cpu \
  --namespace=ailab-ai4solver \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=5m \
  -- bash -lc 'echo worker_host=$(hostname); echo nproc=$(nproc); test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok; test -d /mnt/shared-storage-user/ai4solver && echo mount_ai4solver_ok; test -d /mnt/shared-storage-gpfs2/gpfs2-shared-public && echo mount_public_ok; test -d /mnt/shared-storage-gpfs2/ai4solver && echo mount_ai4solver_ok'
```

scieval 4 CPU，2026-06-05 曾作为默认模板并已实测启动、挂载和自动清理；2026-08-11 起仅作历史备份：

```bash
# 2026-08-11: scieval 不再作为当前默认分区；仅在用户确认回退或资源恢复并短测后使用。
rlaunch \
  --cpu=4 \
  --memory=16000 \
  --charged-group=scieval_cpu_task \
  --namespace=ailab-scieval \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=5m \
  -- bash -lc 'echo worker_host=$(hostname); echo nproc=$(nproc); test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok; test -d /mnt/shared-storage-user/ai4solver && echo mount_ai4solver_ok; test -d /mnt/shared-storage-gpfs2/gpfs2-shared-public && echo mount_public_ok; test -d /mnt/shared-storage-gpfs2/ai4solver && echo mount_ai4solver_ok'
```

ai4sdata 4 CPU，历史模板；2026-06-05 当前 ai4sdata 无 CPU/GPU 资源，不作为默认命令：

```bash
# 2026-06-05: ai4sdata 当前无 CPU/GPU 可用资源；仅在资源恢复并短测后使用。
rlaunch \
  --cpu=4 \
  --memory=16000 \
  --charged-group=ai4sdata_cpu_task \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=2m \
  -- bash -lc 'echo worker_host=$(hostname); test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok; test -d /mnt/shared-storage-user/ai4solver && echo mount_ai4solver_ok; test -d /mnt/shared-storage-gpfs2/gpfs2-shared-public && echo mount_public_ok; test -d /mnt/shared-storage-gpfs2/ai4solver && echo mount_ai4solver_ok'
```

ai4sdata 8 CPU，历史模板；2026-06-05 当前 ai4sdata 无 CPU/GPU 资源，不作为默认命令：

```bash
# 2026-06-05: ai4sdata 当前无 CPU/GPU 可用资源；仅在资源恢复并短测后使用。
rlaunch \
  --cpu=8 \
  --memory=32000 \
  --charged-group=ai4sdata_cpu_task \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=2m \
  -- bash -lc 'echo worker_host=$(hostname); nproc; test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok; test -d /mnt/shared-storage-gpfs2/gpfs2-shared-public && echo mount_public_ok'
```

scieval 8 CPU，历史备份；2026-08-11 起不作为默认命令：

```bash
# 2026-08-11: scieval 不再作为当前默认分区；仅在用户确认回退或资源恢复并短测后使用。
rlaunch \
  --cpu=8 \
  --memory=32000 \
  --charged-group=scieval_cpu_task \
  --namespace=ailab-scieval \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=2m \
  -- bash -lc 'echo worker_host=$(hostname); nproc; test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok; test -d /mnt/shared-storage-user/ai4solver && echo mount_ai4solver_ok; test -d /mnt/shared-storage-gpfs2/gpfs2-shared-public && echo mount_public_ok; test -d /mnt/shared-storage-gpfs2/ai4solver && echo mount_ai4solver_ok'
```

CPU Worker 联网：

CPU worker 可联网。2026-08-11 当前默认使用 ai4solver CPU worker；下面命令可直接复制到开发机交互 shell 中运行，设置代理、测试外网并自动退出，不留下空闲 worker：

```bash
rlaunch \
  --cpu=4 \
  --memory=16000 \
  --charged-group=ai4solver_cpu \
  --namespace=ailab-ai4solver \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=5m \
  -- bash -lc 'set -eo pipefail; echo worker_host=$(hostname); echo nproc=$(nproc); source /jobutils/scripts/worker_init.sh 2>/dev/null || true; source <(curl -sSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh); export no_proxy=10.140.158.153,100.100.125.235,10.0.0.0/8,100.96.0.0/12,0.0.0.0,127.0.0.1,localhost,10.140.213.96,10.140.213.145,.pjlab.org.cn,10.140.14.204,10.140.2.204,10.140.31.254,10.140.14.254,p-ceph-norm-outside.pjlab.org.cn,p-ceph-norm-inside.pjlab.org.cn,10.140.97.32,10.140.96.147; export NO_PROXY=$no_proxy; env | grep -i "^http_proxy\|^https_proxy\|^no_proxy"; curl -I -L --max-time 30 https://www.google.com | sed -n "1,12p"; wget --spider --timeout=30 --tries=1 https://www.google.com; echo ai4solver_cpu_network_ok'
```

scieval CPU worker 联网检查，历史备份；2026-08-11 起不作为当前默认分区：

```bash
# 2026-08-11: scieval 不再作为当前默认分区；仅在用户确认回退或资源恢复并短测后使用。
rlaunch \
  --cpu=4 \
  --memory=16000 \
  --charged-group=scieval_cpu_task \
  --namespace=ailab-scieval \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=5m \
  -- bash -lc 'set -eo pipefail; echo worker_host=$(hostname); echo nproc=$(nproc); source /jobutils/scripts/worker_init.sh 2>/dev/null || true; source <(curl -sSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh); export no_proxy=10.140.158.153,100.100.125.235,10.0.0.0/8,100.96.0.0/12,0.0.0.0,127.0.0.1,localhost,10.140.213.96,10.140.213.145,.pjlab.org.cn,10.140.14.204,10.140.2.204,10.140.31.254,10.140.14.254,p-ceph-norm-outside.pjlab.org.cn,p-ceph-norm-inside.pjlab.org.cn,10.140.97.32,10.140.96.147; export NO_PROXY=$no_proxy; env | grep -i "^http_proxy\|^https_proxy\|^no_proxy"; curl -I -L --max-time 30 https://www.google.com | sed -n "1,12p"; wget --spider --timeout=30 --tries=1 https://www.google.com; echo scieval_cpu_network_ok'
```

ai4sdata CPU worker 联网检查，历史模板；2026-06-05 当前 ai4sdata 无 CPU/GPU 资源时不要直接提交：

```bash
# 2026-06-05: ai4sdata 当前无 CPU/GPU 可用资源；仅在资源恢复并短测后使用。
rlaunch \
  --cpu=4 \
  --memory=16000 \
  --charged-group=ai4sdata_cpu_task \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=2m \
  -- bash -lc 'source /jobutils/scripts/worker_init.sh 2>/dev/null || true; source <(curl -sSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh); export no_proxy=10.140.158.153,100.100.125.235,10.0.0.0/8,100.96.0.0/12,0.0.0.0,127.0.0.1,localhost,10.140.213.96,10.140.213.145,.pjlab.org.cn,10.140.14.204,10.140.2.204,10.140.31.254,10.140.14.254,p-ceph-norm-outside.pjlab.org.cn,p-ceph-norm-inside.pjlab.org.cn,10.140.97.32,10.140.96.147; env | grep -i "^http_proxy\|^https_proxy\|^no_proxy"; curl -I --max-time 20 https://www.google.com | sed -n "1,5p"'
```

进入交互 CPU worker 后，需要联网时用这一组命令。不要依赖 `.bashrc` alias：

```bash
source /jobutils/scripts/worker_init.sh 2>/dev/null || true
source <(curl -sSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh)
export no_proxy=10.140.158.153,100.100.125.235,10.0.0.0/8,100.96.0.0/12,0.0.0.0,127.0.0.1,localhost,10.140.213.96,10.140.213.145,.pjlab.org.cn,10.140.14.204,10.140.2.204,10.140.31.254,10.140.14.254,p-ceph-norm-outside.pjlab.org.cn,p-ceph-norm-inside.pjlab.org.cn,10.140.97.32,10.140.96.147
env | grep -i proxy
curl -I --max-time 20 https://www.google.com
wget --spider https://www.google.com
```

## rlaunch GPU Worker

以下命令用于申请 GPU worker。真实交互使用时把末尾命令写成 `-- bash`，进入 worker 后先运行 `hostname`、`nvidia-smi -L` 和挂载检查；如果调度器提示资源不足或 pending unschedulable，不要反复提交。

2026-08-11 当前默认 GPU worker 使用 `ai4solver_gpu` + `--namespace=ailab-ai4solver`。旧 `ai4sdata_gpu` 和 `scieval_gpu` 模板只作为历史备份保留，不要删除。

ai4solver_gpu 1 GPU，当前默认模板：

```bash
rlaunch \
  --gpu=1 \
  --cpu=22 \
  --memory=230000 \
  --charged-group=ai4solver_gpu \
  --private-machine=group \
  --namespace=ailab-ai4solver \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=5m \
  -- bash -lc 'echo worker_host=$(hostname); nvidia-smi -L; test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok'
```

ai4solver_gpu 2 GPU，当前默认模板：

```bash
rlaunch \
  --gpu=2 \
  --cpu=44 \
  --memory=460000 \
  --charged-group=ai4solver_gpu \
  --private-machine=group \
  --namespace=ailab-ai4solver \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=5m \
  -- bash -lc 'echo worker_host=$(hostname); nvidia-smi -L; test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok'
```

ai4sdata 1 GPU，历史模板；2026-06-05 当前 ai4sdata 无 CPU/GPU 资源时不要直接提交：

```bash
# 2026-06-05: ai4sdata 当前无 CPU/GPU 可用资源；仅在资源恢复并短测后使用。
rlaunch \
  --gpu=1 \
  --cpu=22 \
  --memory=230000 \
  --charged-group=ai4sdata_gpu \
  --private-machine=group \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=2m \
  -- bash -lc 'echo worker_host=$(hostname); nvidia-smi -L; test -d /mnt/shared-storage-user/luoyidong && echo mount_luoyidong_ok'
```

ai4sdata 2 GPU，历史模板；2026-06-05 当前 ai4sdata 无 CPU/GPU 资源时不要直接提交：

```bash
# 2026-06-05: ai4sdata 当前无 CPU/GPU 可用资源；仅在资源恢复并短测后使用。
rlaunch \
  --gpu=2 \
  --cpu=44 \
  --memory=460000 \
  --charged-group=ai4sdata_gpu \
  --private-machine=group \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=30s \
  -- bash -lc 'echo worker_host=$(hostname); nvidia-smi -L'
```

scieval 1 GPU，历史备份；2026-08-11 起不作为默认命令：

```bash
# 2026-08-11: scieval 不再作为当前默认分区；仅在用户确认回退或资源恢复并短测后使用。
rlaunch \
  --gpu=1 \
  --cpu=22 \
  --memory=230000 \
  --charged-group=scieval_gpu \
  --private-machine=group \
  --namespace=ailab-scieval \
  --mount=gpfs://gpfs1/luoyidong:/mnt/shared-storage-user/luoyidong \
  --mount=gpfs://gpfs1/ai4solver:/mnt/shared-storage-user/ai4solver \
  --mount=gpfs://gpfs2/gpfs2-shared-public:/mnt/shared-storage-gpfs2/gpfs2-shared-public \
  --mount=gpfs://gpfs2/ai4solver:/mnt/shared-storage-gpfs2/ai4solver \
  --max-wait-duration=30s \
  -- bash -lc 'echo worker_host=$(hostname); nvidia-smi -L'
```

GPU worker 不可联网。不要在 GPU worker 中运行 `pip install`、`git clone`、外部 API 调用或联网评测。需要依赖时，提前在 CPU worker 或开发机准备到共享存储。
