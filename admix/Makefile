SHELL:=/bin/bash
ref=hgdp
target=habiba

merge: $(target)/merged_$(ref)/common_snps
	~/plink/plink-1.9/plink --bfile $(target)/plink \
							--extract $(target)/merged_$(ref)/common_snps \
							--snps-only just-acgt \
							--make-bed \
							--out $(target)/merged_$(ref)/extracted_$(target)
	ref_dir=`python utils/ref_dir.py $(ref)`; \
	echo $$ref_dir; \
	~/plink/plink-1.9/plink --bfile $$ref_dir/`basename $$ref_dir/*QC_IMP.bed .bed` \
							--extract $(target)/merged_$(ref)/common_snps \
							--make-bed \
							--out $(target)/merged_$(ref)/extracted_$(ref)

	~/plink/plink-1.9/plink --bfile $(target)/merged_$(ref)/extracted_$(target) \
							--bmerge $(target)/merged_$(ref)/extracted_$(ref) \
							--out $(target)/merged_$(ref)/merged

$(target)/merged_$(ref)/common_snps: 
	ref_dir=`python utils/ref_dir.py $(ref)`; \
	mkdir -p $(target)/merged_$(ref)/; \
	cut $(target)/plink.bim -f2 > $(target)/merged_$(ref)/$(target)_snps; \
	cut $$ref_dir/*QC_IMP.bim -f2 > $(target)/merged_$(ref)/$(ref)_snps; \
	cat $(target)/merged_$(ref)/$(ref)_snps | grep -w $(target)/merged_$(ref)/$(target)_snps > $(target)/merged_$(ref)/common_snps; \






