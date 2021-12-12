# This code was used to generate the PHATE. 

# Loading the required packages
library(RDRToolbox)
library(maniTools)
library(bigsnpr)
library(phateR)
library(tidyverse)

# Loading the data (The code was run on euler. You can also acess the data from /l/proj/kuin0009/genomic_data on hpc)
myData <- snp_attach("/home/geb/Documents/hgdp_ceph/hgdp_plink_data/hgdp_bigsnpr/hgdp_QC.rds")

G <- myData$genotypes
CHR <- myData$map$chromosome
POS <- myData$map$physical.pos

# Computing PHATE
phateData <- G[,1:ncol(G)]
phate_out <- phate(phateData)
write.csv(phate_out, file = "PHATE_out.csv", row.names = FALSE)
