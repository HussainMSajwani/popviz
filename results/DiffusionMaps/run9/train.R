library("diffusionMap")
library("bigsnpr")
library("readr")
args <- commandArgs(trailingOnly = TRUE)
t = strtoi(args[1])
myData <- snp_attach("/l/proj/kuin0009/genomic_data/hgdp/hgdp_QC.rds")

HGDP <- myData$genotypes
diffMap_proj_data <- diffusionMap::diffuse(dist(HGDP[ , 1:ncol(HGDP)]),
                                           neigen = 50, t=t)
write.csv(diffMap_proj_data$X, file = paste("DiffusionMaps", t,"_out.csv"), row.names = FALSE)
write.csv(diffMap_proj_data$eigenvals, file = paste("DiffusionMaps", t,"_Eigenvals_out.csv"))