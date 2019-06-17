#!/bin/bash

DIR=${PWD}

ROOT_DIR=${HOME}/research/grasp/write_up
BIB_DIR=bib
DATA_DIR=data
IMAGES_DIR=images

MY_PROJ_DIR=${ROOT_DIR}
MY_BIB_DIR=${ROOT_DIR}/${BIB_DIR}
MY_DATA_DIR=${ROOT_DIR}/${DATA_DIR}
MY_IMAGE_DIR=${ROOT_DIR}/${IMAGES_DIR}

PROJ_TITLE=grasp_report
OCT_FILE=convert_disp_file.m

TEX_EXTENSION=.tex
AUX_EXTENSION=.aux
PDF_EXTENSION=.pdf

WORKSPACE=${DIR}/workspace

TARGET=${PROJ_TITLE}
TARGET_DIR=${MY_PROJ_DIR}

cd $WORKSPACE
rm -r $WORKSPACE/*

cat $MY_BIB_DIR/*          >> ${WORKSPACE}/monolith.bib
cp -r ${MY_DATA_DIR}          ${WORKSPACE}/${DATA_DIR}
cp -r ${MY_IMAGE_DIR}         ${WORKSPACE}/${IMAGES_DIR}

cp ${TARGET_DIR}/${OCT_FILE} ${WORKSPACE}/${DATA_DIR}/${OCT_FILE}
cd ${WORKSPACE}/${DATA_DIR}
echo "convert_disp_file( 8, 8)" | octave --silent
cd ${WORKSPACE}

cp ${TARGET_DIR}/${TARGET}${TEX_EXTENSION} ${WORKSPACE}/${TARGET}${TEX_EXTENSION}

LOCAL_TEX=${TARGET}${TEX_EXTENSION}
LOCAL_AUX=${TARGET}${AUX_EXTENSION}
LOCAL_PDF=${TARGET}${PDF_EXTENSION}

pdflatex $LOCAL_TEX
bibtex   $LOCAL_AUX
pdflatex $LOCAL_TEX
pdflatex $LOCAL_TEX

gnome-open ${LOCAL_PDF}

cd ${DIR}
