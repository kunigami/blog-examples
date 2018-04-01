#!/usr/bin/env zsh

# Make sure cargo is installed
hash cargo 2> /dev/null
if [ $? -ne 0 ]; then
   echo "You need to install cargo before running this script";
   exit 1;
fi

# Build the program
cd hyperloglog/
cargo build --release
cd -

# Run experiments

# try different values of m
i=0
results=''

echo "b,error"
for b in `seq 4 16`
do
  i=0
  while [ $i -lt 10 ]; do
    stdout="$(hyperloglog/target/release/./hyperloglog -n 10000 -r 10000 -b $b)"
    # Split the results into multiple lines
    lines=(${(@f)stdout})
    # echo ${results2[1]}

    row=(${(s/ /)lines[2]})
    error=$row[3]
    echo "$b,$error"
    # parse results
    let i=i+1
  done
done
