"""
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import argparse
import oneflow as flow


def get_args(print_args=True):
    def str_list(x):
        return x.split(",")

    parser = argparse.ArgumentParser()

    parser.add_argument("--model_load_dir", type=str, default="")
    parser.add_argument("--model_save_dir", type=str, default="./checkpoint")
    parser.add_argument(
        "--save_initial_model",
        action="store_true",
        help="save initial model parameters or not.",
    )
    parser.add_argument(
        "--save_model_after_each_eval",
        action="store_true",
        help="save model after each eval.",
    )
    parser.add_argument(
        "--eval_after_training",
        action="store_true",
        help="do eval after_training",
    )
    parser.add_argument(
        "--dataset_format", type=str, default="ofrecord", help="ofrecord, onerec or synthetic"
    )
    parser.add_argument("--data_part_num", type=int, default=256)
    parser.add_argument(
        "--data_dir", type=str, default="/dataset/wdl_ofrecord/ofrecord"
    )
    parser.add_argument('--data_part_name_suffix_length', type=int, default=-1)
    parser.add_argument('--eval_batchs', type=int, default=20)
    parser.add_argument('--eval_interval', type=int, default=1000)    
    parser.add_argument("--batch_size", type=int, default=16384)
    parser.add_argument("--batch_size_per_proc", type=int, default=None)
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument("--wide_vocab_size", type=int, default=1603616)
    parser.add_argument("--deep_vocab_size", type=int, default=1603616)
    parser.add_argument("--deep_embedding_vec_size", type=int, default=16)
    parser.add_argument("--deep_dropout_rate", type=float, default=0.5)
    parser.add_argument("--num_dense_fields", type=int, default=13)
    parser.add_argument("--max_iter", type=int, default=30000)
    parser.add_argument("--loss_print_every_n_iter", type=int, default=100)
    parser.add_argument("--num_wide_sparse_fields", type=int, default=2)
    parser.add_argument("--num_deep_sparse_fields", type=int, default=26)
    parser.add_argument("--hidden_units_num", type=int, default=7)
    parser.add_argument("--hidden_size", type=int, default=1024)
    parser.add_argument(
        "--ddp", action="store_true", help="Run model in distributed data parallel mode"
    )
    parser.add_argument(
        "--execution_mode", type=str, default="eager", help="graph or eager"
    )
    parser.add_argument(
        "--test_name", type=str, default="noname_test"
    )

    args = parser.parse_args()

    world_size = flow.env.get_world_size()
    if args.batch_size_per_proc is None:
        assert args.batch_size % world_size == 0
        args.batch_size_per_proc = args.batch_size // world_size
    else:
        assert args.batch_size % args.batch_size_per_proc == 0

    if print_args and flow.env.get_rank() == 0:
        _print_args(args)
    return args


def _print_args(args):
    """Print arguments."""
    print("------------------------ arguments ------------------------", flush=True)
    str_list = []
    for arg in vars(args):
        dots = "." * (48 - len(arg))
        str_list.append("  {} {} {}".format(arg, dots, getattr(args, arg)))
    for arg in sorted(str_list, key=lambda x: x.lower()):
        print(arg, flush=True)
    print("-------------------- end of arguments ---------------------", flush=True)


if __name__ == "__main__":
    get_args()
