#!/bin/bash

if [ ! -d "GeneralMetapop" ]; then
  echo "GeneralMetapop does not exist."
  echo "Are you running this from the main directory?"
  exit 1
fi

cd GeneralMetapop

mkdir build
cd build

cmake ..

cmake --build .
