---
title: "Bitácora"
author: "abi :)"
output:
  html_document:
    theme: lumen
    toc: true
    toc_float: true
    code_folding: show
---

# 🛠️ Repositorio de Comandos Útiles {.tabset .tabset-fade .tabset-pills}

Aquí guardo los comandos que uso frecuentemente para no tener que buscarlos en el historial.

## Antes de irte NO OLVIDES 

**Actualizar repo remoto**
```text
git status
git add .
git commit -m "descripción de los cambios"
git push origin main
git push origin master
```
**Actualizar mi copia del labo**
```text
git pull origin main
git push lab main

```

## Comandos útilies
* **Revisar estado de mis trabajos:** `squeue -u mi_usuario`
* **Cancelar un trabajo:** `scancel ID_TRABAJO`
* **Ver uso de memoria en tiempo real:** `sstat --format=JobID,MaxVMSize`

## Bitácora

```text 
for amino in *.faa; do
    bacteria=$(basename "$amino" .faa)

    echo "Modelo en proceso: $bacteria"

    carve "$amino" \
    --g MM \
    --mediadb ~/Documents/proyecto_tesis/01_data/media/mm_carveme.tsv \
    --o ./cc_pk_cv_mm_"$bacteria".xml
done
```
for nucleo in 2*.fna; do
    bacteria="${nucleo%.fna}"

    echo "Modelo en proceso para: $bacteria"

    carve "$nucleo" --dna \
        --g LB \
        --o ~/Documents/proyecto_tesis/02_resultados/models/rz_na_cv_na_"$bacteria".xml
done





python3 /home/abigaylmontantearenas/Documents/proyecto_tesis/04_scr/modelajemetabolico2026/scr/sim_syncom_comets.py \
--gem_path /home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/modelos_core \
--strains mergem_ec_na_cv_na_ecoli_kb_na_ecoli \
--initial_mass 1e-5 \
--cycles 100 \
--media m9 \
--outdir /home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/modelos_core/merge





JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
            234251      defq gapseq_f mmontant  R    4:41:11      1 node03
[mmontante@login01 mmontante]$ scontrol show job 234251
JobId=234251 JobName=gapseq_full_pipe
   UserId=mmontante(100095) GroupId=sur(100006) MCS_label=N/A
   Priority=4294832566 Nice=0 Account=root QOS=limit64
   JobState=RUNNING Reason=None Dependency=(null)
   Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
   RunTime=04:41:50 TimeLimit=10-00:00:00 TimeMin=N/A
   SubmitTime=2026-06-17T13:39:48 EligibleTime=2026-06-17T13:39:48
   AccrueTime=2026-06-17T13:39:48
   StartTime=2026-06-17T13:39:48 EndTime=2026-06-27T13:39:48 Deadline=N/A
   SuspendTime=None SecsPreSuspend=0 LastSchedEval=2026-06-17T13:39:48 Scheduler=Main
   Partition=defq AllocNode:Sid=login01:3075565
   ReqNodeList=(null) ExcNodeList=(null)
   NodeList=node03
   BatchHost=node03
   NumNodes=1 NumCPUs=8 NumTasks=1 CPUs/Task=8 ReqB:S:C:T=0:0:*:*
   ReqTRES=cpu=8,mem=20G,node=1,billing=8
   AllocTRES=cpu=8,mem=20G,node=1,billing=8
   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*
   MinCPUsNode=8 MinMemoryNode=20G MinTmpDiskNode=0
   Features=(null) DelayBoot=00:00:00
   OverSubscribe=OK Contiguous=0 Licenses=(null) LicensesAlloc=(null) Network=(null)
   Command=/mnt/data/sur/users/mmontante/gapseq_prueba/gapseq120616.slurm
   SubmitLine=sbatch gapseq_prueba/gapseq120616.slurm
   WorkDir=/mnt/data/sur/users/mmontante
   StdErr=/mnt/data/sur/users/mmontante/gapseq_full_pipe.error
   StdIn=/dev/null
   StdOut=/mnt/data/sur/users/mmontante/gapseq_full_pipe.log
   TresPerTask=cpu=8
