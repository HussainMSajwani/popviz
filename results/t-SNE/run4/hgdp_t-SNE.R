library(RDRToolbox)
library(maniTools)
library(bigsnpr)
library(Rtsne)
library(tidyverse)

myData <- snp_attach("/home/geb/Documents/hgdp_ceph/hgdp_plink_data/hgdp_bigsnpr/hgdp_QC.rds")

G <- myData$genotypes
CHR <- myData$map$chromosome
POS <- myData$map$physical.pos

hgdpData <- G[,1:ncol(G)]
hgdpData_unique <- unique(hgdpData) # Remove duplicates
set.seed(42)# Sets seed for reproducibility
tsne_out3 <- Rtsne(as.matrix(hgdpData_unique[,1:ncol(G)]), perplexity = 100) # Run TSNE 
write.csv(tsne_out3$Y, file = "t-SNE_out.csv", row.names =FALSE)
