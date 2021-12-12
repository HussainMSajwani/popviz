# This R code was run on euler. 

# Loading the required libraries
library(RDRToolbox)
library(maniTools)
library(bigsnpr)
library(tidyverse)

# Loading the data
myData <- snp_attach("/home/geb/Documents/hgdp_ceph/hgdp_plink_data/hgdp_bigsnpr/hgdp_QC.rds")

G <- myData$genotypes
CHR <- myData$map$chromosome
POS <- myData$map$physical.pos

# Computing the pca
pca_dr <- G[1:nrow(G), 1:ncol(G)] %>% center_and_standardise() %>% prcomp()
proj_data <- G[1:nrow(G), 1:ncol(G)] %*% pca_dr$rotation[,1:2]
write.csv(proj_data, file = "PCA_out.csv", row.names = FALSE)
