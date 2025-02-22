DEVICE_NUM_PER_NODE=1
MASTER_ADDR=127.0.0.1
NUM_NODES=1
NODE_RANK=0
DATA_DIR=/dataset/wdl_ofrecord/ofrecord
EMBD_SIZE=2322444
BATHSIZE=2048

python3 -m oneflow.distributed.launch \
    --nproc_per_node $DEVICE_NUM_PER_NODE \
    --nnodes $NUM_NODES \
    --node_rank $NODE_RANK \
    --master_addr $MASTER_ADDR \
    train.py \
    --learning_rate 0.001 \
    --batch_size $BATHSIZE \
    --data_dir $DATA_DIR \
    --loss_print_every_n_iter 100 \
    --eval_interval 0 \
    --deep_dropout_rate 0.5 \
    --max_iter 310 \
    --hidden_units_num 7 \
    --hidden_size 1024 \
    --wide_vocab_size $EMBD_SIZE \
    --deep_vocab_size $EMBD_SIZE \
    --data_part_num 256 \
    --data_part_name_suffix_length 5 \
    --execution_mode 'eager' \
    --test_name 'train_eager_conisitent_'$DEVICE_NUM_PER_NODE'gpu'
