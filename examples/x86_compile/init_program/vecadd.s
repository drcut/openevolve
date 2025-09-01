	.text
	.file	"vecadd.c"
	.globl	vecadd                          # -- Begin function vecadd
	.p2align	4, 0x90
	.type	vecadd,@function
# EVOLVE-BLOCK-START
vecadd:                                 # @vecadd
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	%rdx, -24(%rbp)
	movl	%ecx, -28(%rbp)
	movl	$0, -32(%rbp)
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	movl	-32(%rbp), %eax
	cmpl	-28(%rbp), %eax
	jge	.LBB0_4
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movq	-8(%rbp), %rax
	movslq	-32(%rbp), %rcx
	movss	(%rax,%rcx,4), %xmm0            # xmm0 = mem[0],zero,zero,zero
	movq	-16(%rbp), %rax
	movslq	-32(%rbp), %rcx
	addss	(%rax,%rcx,4), %xmm0
	movq	-24(%rbp), %rax
	movslq	-32(%rbp), %rcx
	addss	(%rax,%rcx,4), %xmm0
	movss	%xmm0, (%rax,%rcx,4)
# %bb.3:                                #   in Loop: Header=BB0_1 Depth=1
	movl	-32(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -32(%rbp)
	jmp	.LBB0_1
.LBB0_4:
	popq	%rbp
	retq
# EVOLVE-BLOCK-END
.Lfunc_end0:
	.size	vecadd, .Lfunc_end0-vecadd
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
	.addrsig
