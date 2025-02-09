# RMSNorm

## 0x00 说明

包含以下内容：

- [X] rms_norm_f32_kernel 
- [X] rms_norm_f32x4_kernel
- [X] rms_norm_f16_f16_kernel
- [X] rms_norm_f16x2_f16_kernel
- [X] rms_norm_f16x8_f16_kernel
- [X] rms_norm_f16x8_f32_kernel
- [X] rms_norm_f16x16_f16_kernel
- [X] rms_norm_f16x16_f32_kernel
- [X] rms_norm_f16_f32_kernel
- [X] PyTorch bindings

## 测试

```bash
# 只测试Ada架构 不指定默认编译所有架构 耗时较长
export TORCH_CUDA_ARCH_LIST=Ada 
python3 rms_norm.py
```

输出:

```bash
--------------------------------------------------------------------------------
      out_f32: [0.92419142, -0.08846965, 1.06359947], time:0.03389192ms
    out_f32x4: [0.92419147, -0.08846966, 1.06359959], time:0.00855207ms
   out_f32_th: [0.92419606, -0.08847010, 1.06360483], time:0.04171062ms
--------------------------------------------------------------------------------
   out_f16f16: [0.92431641, -0.08843994, 1.06347656], time:0.03518176ms
 out_f16x2f16: [0.92431641, -0.08843994, 1.06347656], time:0.01200986ms
 out_f16x8f16: [0.92431641, -0.08843994, 1.06347656], time:0.00625682ms
 out_f16x8f32: [0.92431641, -0.08843994, 1.06347656], time:0.00625014ms
out_f16x16f16: [0.92431641, -0.08843994, 1.06347656], time:0.02620339ms
out_f16x16f32: [0.92431641, -0.08843994, 1.06347656], time:0.01505637ms
   out_f16f32: [0.92431641, -0.08843994, 1.06347656], time:0.03300810ms
   out_f16_th: [0.92431641, -0.08843994, 1.06347656], time:0.04187107ms
--------------------------------------------------------------------------------
```
