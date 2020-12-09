# code pulled from vignette: http://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#quick-start

# install packages
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("DESeq2")
BiocManager::install("pasilla")
BiocManager::install("apeglm")

# ---------------- IMPORTS ---------------- #

# import packages
library("pasilla")
library("DESeq2")

# ---------------- DATA ---------------- #

# get data
pasCts <- system.file("extdata",
                      "pasilla_gene_counts.tsv",
                      package="pasilla", mustWork=TRUE)
pasAnno <- system.file("extdata",
                       "pasilla_sample_annotation.csv",
                       package="pasilla", mustWork=TRUE)
print(pasAnno)
cts <- as.matrix(read.csv(pasCts,sep="\t",row.names="gene_id"))
coldata <- read.csv(pasAnno, row.names=1)
coldata <- coldata[,c("condition","type")]
coldata$condition <- factor(coldata$condition)
coldata$type <- factor(coldata$type)

# our data
temp <- as.matrix(read.csv("./data/SraRunTable.csv"))
our_cts <- as.matrix(read.csv("./data/deseq_cts.tsv", sep="\t"), row.names("target_id"))

# look at the data
head(cts,2)
coldata

# not in same order! 
rownames(coldata) <- sub("fb", "", rownames(coldata))

# the same samples
all(rownames(coldata) %in% colnames(cts))
# but not the same order!
all(rownames(coldata) == colnames(cts))

# sort to be in the same order
cts <- cts[, rownames(coldata)]
all(rownames(coldata) == colnames(cts))

# ---------------- DESeqDataSet ---------------- #

# create DESeqDataSet object
dds <- DESeqDataSetFromMatrix(countData = cts,
                              colData = coldata,
                              design = ~ condition)
dds

# set up metadata
featureData <- data.frame(gene=rownames(cts))
mcols(dds) <- DataFrame(mcols(dds), featureData)
mcols(dds)

# ---------------- FILTERING ---------------- #

# pre-filter
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep,]

# factors in R!
dds$condition <- factor(dds$condition, levels = c("untreated","treated"))

# ---------------- DEA ---------------- #

# Differential expression analysis
?DESeq
# carries out: estimation of size factors, estimation of dispersion: neg. binomial GLM
dds <- DESeq(dds)
res <- results(dds)
res

# Log fold change
resLFC <- lfcShrink(dds, coef="condition_treated_vs_untreated", type="apeglm")
resLFC

resOrdered <- resLFC[order(resLFC$pvalue),]
sum(resOrdered$padj < 0.1, na.rm=TRUE)

res05 <- results(dds, alpha=0.05)
summary(res05)

# ---------------- PAPER ---------------- #

# the paper approach:

# LRT
dds <- DESeq(dds, test="LRT", reduced=~1)
res <- results(dds)

## variance stabilizing
vsd <- vst(dds, blind=FALSE)

