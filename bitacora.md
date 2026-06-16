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

