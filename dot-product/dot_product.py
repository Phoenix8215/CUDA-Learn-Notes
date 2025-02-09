import torch
import time 
from torch.utils.cpp_extension import load

torch.set_grad_enabled(False)

# Load the CUDA kernel as a python module
lib = load(name='dot_product_lib', 
           sources=['dot_product.cu'], 
           extra_cuda_cflags=[
               "-O3",
                "-U__CUDA_NO_HALF_OPERATORS__",
                "-U__CUDA_NO_HALF_CONVERSIONS__",
                "-U__CUDA_NO_HALF2_OPERATORS__",
                "-U__CUDA_NO_BFLOAT16_CONVERSIONS__",
                "--expt-relaxed-constexpr",
                "--expt-extended-lambda",
                "--use_fast_math",
            ], 
           extra_cflags=['-std=c++17'])


def run_benchmark(perf_func: callable, a: torch.Tensor, b: torch.Tensor, tag: str, 
                  warmup: int = 10, iters: int = 1000):
    # torch.dot vs custom dot_prod kernel
    for i in range(warmup):
        out = perf_func(a, b) # warmup
    torch.cuda.synchronize()
    start = time.time()
    for i in range(iters):
        out = perf_func(a, b)
    torch.cuda.synchronize()
    end = time.time()
    total_time = (end - start) * 1000 # ms
    mean_time = total_time / iters
    out_info = f"out_{tag}"
    out_val = out.item()
    if tag.startswith("i8"):
        print(f"{out_info:>17}: {out_val:<15}, time:{mean_time:.8f}ms")
    else:
        print(f"{out_info:>17}: {out_val:<15.8f}, time:{mean_time:.8f}ms")
    return out, mean_time


print("-" * 80)
N_ELEMENTS = 256*92*16
a = torch.randn((N_ELEMENTS)).cuda().float()
b = torch.randn((N_ELEMENTS)).cuda().float()
run_benchmark(lib.dot_prod_f32_f32,   a, b, "f32f32")
run_benchmark(lib.dot_prod_f32x4_f32, a, b, "f32x4f32")
run_benchmark(torch.dot, a, b , "f32f32_th")

print("-" * 80)
a_f16 = a.half()
b_f16 = b.half()
run_benchmark(lib.dot_prod_f16_f32,   a_f16, b_f16, "f16f32")
run_benchmark(lib.dot_prod_f16x2_f32, a_f16, b_f16, "f16x2f32")
run_benchmark(torch.dot, a_f16, b_f16 , "f16f16_th")

print("-" * 80)
