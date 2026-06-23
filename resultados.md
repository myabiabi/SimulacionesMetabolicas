---
title: "Untitled"
author: "abi :)"
date: "2026-06-17"
output: html_document
---
Cargar paquetes
```{r}
library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(cowplot)
library(growthcurver)
library(tidyverse)
library(pracma)

```
Rutas
```{r}
variables_file <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/evaluacion/variables_totales.csv"
```
Comparar las variables
```{r}
df <- read_csv(variables_file)

names(df) <- trimws(names(df))

df$Method <- factor(
  df$Method,
  levels = c("CV", "KB", "GP")
)

df_long <- df %>%
  pivot_longer(
    cols = c(
      Reactions,
      Metabolites,
      Genes
    ),
    names_to = "Variable",
    values_to = "Value"
  )

general <- ggplot(
  df_long,
  aes(
    x = Variable,
    y = Value,
    fill = Method
  )
) +
  geom_boxplot(
    alpha = 0.4,
    outlier.shape = NA,
    position = position_dodge(width = 0.8)
  ) +
  geom_jitter(
    aes(color = Method),
    position = position_jitterdodge(
      jitter.width = 0.15,
      dodge.width = 0.8
    ),
    size = 2,
    alpha = 0.9
  ) +
  scale_fill_manual(
    values = c(
      CV = "#79CDCD",
      KB = "#BCEE68",
      GP = "#FFC0CB"
    ),
    labels = c(
      CV = "CarveMe",
      KB = "KBase",
      GP = "gapseq"
    )
  ) +
  scale_color_manual(
    values = c(
      CV = "#528B8B",
      KB = "#6E8B3D",
      GP = "#C71585"
    ),
    labels = c(
      CV = "CarveMe",
      KB = "KBase",
      GP = "gapseq"
    )
  ) +
  labs(
    fill = "Method",
    color = "Method",
    x = "",
    y = "Count"
  ) +
  guides(color = "none") +
  theme_bw()

ggsave(
  filename = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/graficas/metodos.png", 
  plot = general, 
  width = 18,           # Mayor ancho para que los 3 paneles respiren bien
  height = 7,           # Alto proporcional
  units = "in",         # Unidades: "in" (pulgadas), "cm" (centímetros) o "mm"
  dpi = 600             # 600 DPI es una calidad extremadamente alta (ideal para impresión/publicación)
)
print(general)

# Metodos CarveMe
# Filtrar únicamente los métodos de KBase
df_long_cv <- df_long %>%
  filter(Reconstruction %in% c("CV", "PK_CV"))

# Definir el orden de los grupos
df_long_cv$Reconstruction <- factor(
  df_long_cv$Reconstruction,
  levels = c("CV", "PK_CV")
)

carve <- ggplot(
  df_long_cv,
  aes(
    x = Variable,
    y = Value,
    fill = Reconstruction
  )
) +
  geom_boxplot(
    alpha = 0.5,
    outlier.shape = NA,
    position = position_dodge(width = 0.8),
    width = 0.7
  ) +
  geom_jitter(
    aes(color = Reconstruction),
    position = position_jitterdodge(
      jitter.width = 0.15,
      dodge.width = 0.8
    ),
    size = 2.5,
    alpha = 0.8
  ) +
  scale_fill_manual(
    values = c(
      "CV"    = "#000080",  
      "PK_CV" = "#4169E1"   
    ),
    labels = c(
      "CarveMe",
      "Prokka + CarveMe"
    )
  ) +
  scale_color_manual(
    values = c(
      "CV"    = "#191970",
      "PK_CV" = "#1E90FF"
    ),
    labels = c(
      "CarveMe",
      "Prokka + CarveMe"
    )
  ) +
  labs(
    x = "",
    y = "Count",
    fill = "Method",
    color = "Method"
  ) +
  theme_bw() +
  theme(
    panel.grid.major.x = element_blank(),
    legend.position = "top",
    axis.text.x = element_text(
      size = 12,
      face = "bold"
    )
  )

print(carve)

# Metodo kbase
library(dplyr)
library(ggplot2)

# Filtrar únicamente los métodos de KBase
df_long_kb <- df_long %>%
  filter(Reconstruction %in% c("RT_KB", "PK_RT_KB"))

# Definir el orden de los grupos
df_long_kb$Reconstruction <- factor(
  df_long_kb$Reconstruction,
  levels = c("RT_KB", "PK_RT_KB")
)

# Gráfica
kbase <- ggplot(
  df_long_kb,
  aes(
    x = Variable,
    y = Value,
    fill = Reconstruction
  )
) +
  geom_boxplot(
    alpha = 0.5,
    outlier.shape = NA,
    position = position_dodge(width = 0.8),
    width = 0.7
  ) +
  geom_jitter(
    aes(color = Reconstruction),
    position = position_jitterdodge(
      jitter.width = 0.15,
      dodge.width = 0.8
    ),
    size = 2.5,
    alpha = 0.8
  ) +
  scale_fill_manual(
    values = c(
      "RT_KB"    = "#F0FFF0",
      "PK_RT_KB" = "#98FB98"
    ),
    labels = c(
      "KBase",
      "Prokka + KBase"
    )
  ) +
  scale_color_manual(
    values = c(
      "RT_KB"    = "#2E8B57",
      "PK_RT_KB" = "#006400"
    ),
    labels = c(
      "KBase",
      "Prokka + KBase"
    )
  ) +
  labs(
    x = "",
    y = "Count",
    fill = "Method",
    color = "Method"
  ) +
  theme_bw() +
  theme(
    panel.grid.major.x = element_blank(),
    legend.position = "top",
    axis.text.x = element_text(
      size = 12,
      face = "bold"
    )
  )

print(kbase)


# Filtrar únicamente los métodos de KBase
df_long_gp <- df_long %>%
  filter(Reconstruction %in% c("GP", "PK_GP"))

# Definir el orden de los grupos
df_long_gp$Reconstruction <- factor(
  df_long_gp$Reconstruction,
  levels = c("GP", "PK_GP")
)

# Gráfica
gapseq <- ggplot(
  df_long_gp,
  aes(
    x = Variable,
    y = Value,
    fill = Reconstruction
  )
) +
  geom_boxplot(
    alpha = 0.5,
    outlier.shape = NA,
    position = position_dodge(width = 0.8),
    width = 0.7
  ) +
  geom_jitter(
    aes(color = Reconstruction),
    position = position_jitterdodge(
      jitter.width = 0.15,
      dodge.width = 0.8
    ),
    size = 2.5,
    alpha = 0.8
  ) +
  scale_fill_manual(
    values = c(
      "GP"    = "#FFE4E1",
      "PK_GP" = "#E75480"
    ),
    labels = c(
      "Gapseq",
      "Prokka + Gapseq"
    )
  ) +
  scale_color_manual(
    values = c(
      "GP"    = "#C71585",
      "PK_GP" = "#FFB6C1"
    ),
    labels = c(
      "Gapseq",
      "Prokka + Gapseq"
    )
  ) +
  labs(
    x = "",
    y = "Count",
    fill = "Method",
    color = "Method"
  ) +
  theme_bw() +
  theme(
    panel.grid.major.x = element_blank(),
    legend.position = "top",
    axis.text.x = element_text(
      size = 12,
      face = "bold"
    )
  )

print(gapseq)

install.packages("cowplot")
# Cargar la librería
library(cowplot)

# Combinar las gráficas en 3 columnas
grafica_final <- plot_grid(
  carve, kbase, gapseq, 
  labels = c("A", "B", "C"), # Etiquetas para cada panel
  ncol = 3,                  # Número de columnas
  align = "h"                # Alinea horizontalmente los ejes de las gráficas
)

# Suponiendo que usaste 'patchwork' o 'cowplot' para crear 'grafica_final'
# Modifica los valores de width y height a tu gusto (están en pulgadas por defecto)

ggsave(
  filename = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_resultados/graficas/metodos_reconstruccion.png", 
  plot = grafica_final, 
  width = 18,           # Mayor ancho para que los 3 paneles respiren bien
  height = 7,           # Alto proporcional
  units = "in",         # Unidades: "in" (pulgadas), "cm" (centímetros) o "mm"
  dpi = 600             # 600 DPI es una calidad extremadamente alta (ideal para impresión/publicación)
)

# Mostrar la gráfica
print(grafica_final)
```

```{r}
all_biomass <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/toy/com1/biomass.txt"
my_data <- read.table(all_biomass, header = TRUE) 
head(my_data)


# Syntax: rename(dataframe, new_name = old_name)
colnames(my_data)[1] <- "cicles" 
colnames(my_data)[4] <- "name"
colnames(my_data)[5] <- "biomass" 

print(my_data)

# Calculate the Area Under the Curve
growth_auc <- trapz(my_data$cicles, my_data$biomass)

# Print the result
print(growth_auc)


```