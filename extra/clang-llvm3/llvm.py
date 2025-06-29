from llvmlite import ir

# Declare short aliases for common LLVM types
void = ir.VoidType()
i32  = ir.IntType(32)
i8   = ir.IntType(8)
i1   = ir.IntType(1)
f64  = ir.DoubleType()

# Add LLVM module
llvm_module = ir.Module("Module")

# Declare a global variable and initialize it
global_pi = ir.GlobalVariable(llvm_module, f64, "pi")
global_pi.initializer = ir.Constant(f64, 3.141592)

# Load some external functions (defined in C)
print_i32 = ir.Function(llvm_module, ir.FunctionType(void, [i32]), name = "print_i32")
print_f64 = ir.Function(llvm_module, ir.FunctionType(void, [f64]), name = "print_f64")

# Add a function
distance_function = ir.Function(llvm_module, ir.FunctionType(f64, []), "distance")

# Add a block to the function
start_block = distance_function.append_basic_block("start")
builder = ir.IRBuilder(start_block)

# Adding some variables
vel = builder.alloca(f64, name = "vel")
time = builder.alloca(f64, name = "time")

# Store something inside those variables
builder.store(ir.Constant(f64, 6.88), vel)
builder.store(ir.Constant(f64, 3.0), time)

# Computer the multiplication of vel * time
r1 = builder.load(vel)    # r1 = vel
r2 = builder.load(time)   # r2 = vel
r3 = builder.fmul(r1, r2) # r3 = r1 * r2

# Store the result from r3 into "dist"
dist = builder.alloca(f64, name = "dist")
builder.store(r3, dist)

# Call external function print_f64()
builder.call(print_f64, [builder.load(dist)])

# Return the value at the end of the function
builder.ret(builder.load(dist))

# Print the LLVM module
print(llvm_module)
