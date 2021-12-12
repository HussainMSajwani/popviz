library(bigsnpr)

hgdp <- snp_attach("/home/shussain/popviz/genomic_data/hgdp_QC_IMP.rds")
G <- hgdp$genotypes

jpeg(file="saving_plot1.jpeg")
hist(G[1:nrow(G), 1:ncol(G)])
dev.off()