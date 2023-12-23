#!/bin/bash
CURRENTDIR=$(dirname "$0")
echo "Running $1"
case $1 in
  uvirun)
    uvicorn main:app --reload --host 0.0.0.0 --port 8101
    ;;

  *)
    echo "unknown command received."
    exit 1;;
esac
