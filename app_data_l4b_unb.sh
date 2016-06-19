#!/bin/zsh
#
#
#os systme
#$ -l os=sl5
#
# execution time
#$ -l h_cpu=03:29:00
#
# max memory consumption
#$ -l h_vmem=1000M
#
#Temp directory must have at least 20G
#$ -l tmpdir_size=20G
# mail on aboard
# -m ae
# -M lotfiben@ifh.de
# combine std.err and std.out
#$ -j y
#$ -o /dev/null
# priority
# -P z_nuastr
exec > "$TMPDIR"/stdout.txt 2>"$TMPDIR"/stderr.txt

echo 'the job starts at ' `date`
start=$(date +%s)

year=$1
date=$2
run=$3
beta=$4
mfp=$5

echo 'the year'
echo $year
echo 'the date'
echo $date
echo 'the run'
echo $run

#dir_in=/lustre/fs6/group/i3/lotfiben/${year}/data_ic59/level4b/$date/beta_1e-3/lambda_1mm/
if [[ ${mfp} ==  "lambda_1mm" ]]
then
    new_mfp="lambda_1mm_fin"

    dir_in=/lustre/fs6/group/i3/lotfiben/${year}/data_ic59/level4b/${date}
    ### This for [  Basho's part ]
    #dir_in=/lustre/fs7/group/i3/kaminsky/lotfiben/${year}/data_ic59/level4b/${date}
    mkdir -p /lustre/fs6/group/i3/lotfiben/${year}/data_ic59/level4b/${date}/${beta}/${mfp}
    dir_out=/lustre/fs6/group/i3/lotfiben/${year}/data_ic59/level4b/${date}/${beta}/${mfp}
    output_all=Level4b_Data_${beta}_${mfp}_Application_All_Vondata_${date}_${run}.hdf
else
    
    new_mfp="lambda_1cm_fin"
  
    dir_in=/lustre/fs6/group/i3/lotfiben/${year}/data_ic59/level4b/${date}
    ### This for [  Basho's part ]
    #dir_in=/lustre/fs7/group/i3/kaminsky/lotfiben/${year}/data_ic59/level4b/${date}

    mkdir -p /lustre/fs6/group/i3/lotfiben/${year}/data_ic59/level4b/$date/${beta}/${mfp}
    dir_out=/lustre/fs6/group/i3/lotfiben/${year}/data_ic59/level4b/$date/${beta}/${mfp}
    output_all=Level4b_Data_${beta}_${mfp}_Application_All_Vondata_${date}_${run}.hdf
    
fi


mkdir -p $dir_out 

echo 'the directory is'

cd $TMPDIR

mkdir hdffiles
cp -r  /afs/ifh.de/user/l/lotfiben/scratch/TMVA/ $TMPDIR


if [[ ${mfp} == "lambda_1mm" ]]
then
    #infile=`ls -1 ${dir_in}/Level4b_Data*_"${date}".hdf`

    ### This for [  Basho's part ]
    infile=`ls -1 ${dir_in}/Level4b_"${date}"_"${run}".hdf`
    cp -v ${infile} $TMPDIR/hdffiles/
else
    #infile=`ls -1 ${dir_in}/Level4b_Data*_"${date}".hdf`

    ### This for [  Basho's part ]
    infile=`ls -1 ${dir_in}/Level4b_"${date}"_"${run}".hdf`
    cp -v ${infile} $TMPDIR/hdffiles/

fi
cd $TMPDIR/TMVA/${beta}/${new_mfp}
pwd

echo "beta "$beta" "
echo "lambda "$mfp" "
echo 'the job has run till now1' `date`

ls weights/*xml

ls -hrlt $TMPDIR/hdffiles

BDTS="`ls weights/*xml | cut -d "/" -f 2 | cut -d "." -f 1 | cut -c20-38 | tr '\n' ' '`"

echo $BDTS
python TMVApplication.py -m "$BDTS" -d $TMPDIR/hdffiles

echo 'the job has run till now2' `date`
if [[ ${mfp} ==  "lambda_1mm" ]]
then
    cp  -v $TMPDIR/hdffiles/Level4b_${date}_${run}.hdf ${dir_out}/${output_all}
else
    cp -v  $TMPDIR/hdffiles/Level4b_${date}_${run}.hdf ${dir_out}/${output_all}
fi

cp -v  $TMPDIR/stdout.txt /lustre/fs6/group/i3/lotfiben/output/stdout_BDT_${beta}_${mfp}_${run}_${date}.txt
cp -v  $TMPDIR/stderr.txt /lustre/fs6/group/i3/lotfiben/output/stderr_BDT_${beta}_${mfp}_${run}_${date}.txt
end=$(date +%s)

echo "The job finishs at" `date`
DIFF=$(( $end - $start ))
echo "It took "$DIFF" seconds"



