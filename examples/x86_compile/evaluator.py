import re
import subprocess
import time
import traceback
import ctypes
import numpy as np
import time
import subprocess
import os

def compile_asm(asm_file, func_name):
    
    if asm_file.endswith('.py'):
        new_asm_file = asm_file.replace('.py', '.s')
        subprocess.run(['cp', asm_file, new_asm_file])
        asm_file = new_asm_file
    obj_file = asm_file.replace('.s', '.o')
    lib_file = asm_file.replace('.s', '.so')

    try:
        print(f"[*] Assembling {asm_file} with clang...")
        print(f"[*] Command: clang -c {asm_file} -o {obj_file}")
        subprocess.run(['clang', '-c', asm_file, '-o', obj_file], check=True)

        print(f"[*] Linking {obj_file} into {lib_file} with clang...")
        print(f"[*] Command: clang -shared {obj_file} -o {lib_file}")
        subprocess.run(['clang', '-shared', obj_file, '-o', lib_file], check=True)

        lib = ctypes.CDLL(os.path.abspath(lib_file))
        compiled_func = lib[func_name]

        return compiled_func

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while compiling assembly: {e}")
        return None

def evaluate(asm_file):
    vector_add_func = compile_asm(asm_file, 'vecadd')

    if vector_add_func is None:
        print("Failed to compile assembly.")
        return {
            "combined_score": 0,
            "compile": False,
            "correct": False,
        }
    else:
        vector_add_func.argtypes = [
                np.ctypeslib.ndpointer(dtype=np.float32, flags='C_CONTIGUOUS'),
                np.ctypeslib.ndpointer(dtype=np.float32, flags='C_CONTIGUOUS'),
                np.ctypeslib.ndpointer(dtype=np.float32, flags='C_CONTIGUOUS'),
                ctypes.c_size_t
            ]
        vector_add_func.restype = None

        vec_size = 8 * 1024 * 1024  # 8 million floats
        vec_out = np.zeros(vec_size, dtype=np.float32)
        vec1 = np.random.rand(vec_size).astype(np.float32)
        vec2 = np.random.rand(vec_size).astype(np.float32)

        print("[*] Executing assembly function...")
        start_time = time.perf_counter()
        vector_add_func(vec1, vec2, vec_out, vec_size)
        end_time = time.perf_counter()

        # Verify correctness
        if np.allclose(vec_out, vec1 + vec2):
            return {
                "combined_score": 1/(end_time - start_time),
                "compile": True,
                "correct": True,
            }
        else:
            return {
                "combined_score": 0,
                "compile": True,
                "correct": False,
            }

if __name__ == "__main__":
    eval_res = evaluate('init_program/vecadd.s')
    print(eval_res)