from llvmlite import ir


class Number:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        i = ir.Constant(ir.IntType(8), int(self.value))
        return i


class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self):
        i = self.builder.add(self.left.eval(), self.right.eval())
        return i


class Sub(BinaryOp):
    def eval(self):
        i = self.builder.sub(self.left.eval(), self.right.eval())
        return i


class Mul(BinaryOp):
    def eval(self):
        i = self.builder.mul(self.left.eval(), self.right.eval())
        return i


class Div(BinaryOp):
    def eval(self):
        i = self.builder.sdiv(self.left.eval(), self.right.eval())
        return i



## define a String class and a Print class for LLVM IR so that a value is printed to the console after compiling and running the code.
class String:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value[1:-1]  # remove the quotes from the string

    def eval(self):
        from llvmlite import ir, binding

        # Initialize LLVM
        binding.initialize()
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()

        # Create an LLVM module and a function
        module = ir.Module()
        func_ty = ir.FunctionType(ir.VoidType(), [])
        function = ir.Function(module, func_ty, name="main")
        block = function.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)

        # Create a constant string
        string_constant = ir.Constant(ir.ArrayType(ir.IntType(8), len("Hello, LLVM!")),
                                      bytearray("Hello, LLVM!", "utf-8"))

        # Create a global variable to hold the string
        global_var = ir.GlobalVariable(module, string_constant.type, name="my_string")
        global_var.initializer = string_constant
        global_var.global_constant = True
        global_var.linkage = "internal"

        # Call the `puts` function to print the string
        puts_func_ty = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()])
        puts_func = ir.Function(module, puts_func_ty, name="puts")

        builder.call(puts_func, [builder.bitcast(global_var, ir.IntType(8).as_pointer())])

        # Return 0 from the main function
        builder.ret(ir.Constant(ir.IntType(32), 0))

        # Print the generated LLVM IR code
        print(module)

        # Clean up LLVM
