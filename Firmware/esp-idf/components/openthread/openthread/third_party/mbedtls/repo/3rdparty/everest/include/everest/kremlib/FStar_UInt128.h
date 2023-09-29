/* Copyright (c) INRIA and Microsoft Corporation. All rights reserved.
   Licensed under the Apache 2.0 License. */

/* This file was generated by KreMLin <https://github.com/FStarLang/kremlin>
 * KreMLin invocation: ../krml -fc89 -fparentheses -fno-shadow -header /mnt/e/everest/verify/hdrB9w -minimal -fparentheses -fcurly-braces -fno-shadow -header copyright-header.txt -minimal -tmpdir dist/uint128 -skip-compilation -extract-uints -add-include <inttypes.h> -add-include <stdbool.h> -add-include "kremlin/internal/types.h" -bundle FStar.UInt128=* extracted/prims.krml extracted/FStar_Pervasives_Native.krml extracted/FStar_Pervasives.krml extracted/FStar_Mul.krml extracted/FStar_Squash.krml extracted/FStar_Classical.krml extracted/FStar_StrongExcludedMiddle.krml extracted/FStar_FunctionalExtensionality.krml extracted/FStar_List_Tot_Base.krml extracted/FStar_List_Tot_Properties.krml extracted/FStar_List_Tot.krml extracted/FStar_Seq_Base.krml extracted/FStar_Seq_Properties.krml extracted/FStar_Seq.krml extracted/FStar_Math_Lib.krml extracted/FStar_Math_Lemmas.krml extracted/FStar_BitVector.krml extracted/FStar_UInt.krml extracted/FStar_UInt32.krml extracted/FStar_Int.krml extracted/FStar_Int16.krml extracted/FStar_Preorder.krml extracted/FStar_Ghost.krml extracted/FStar_ErasedLogic.krml extracted/FStar_UInt64.krml extracted/FStar_Set.krml extracted/FStar_PropositionalExtensionality.krml extracted/FStar_PredicateExtensionality.krml extracted/FStar_TSet.krml extracted/FStar_Monotonic_Heap.krml extracted/FStar_Heap.krml extracted/FStar_Map.krml extracted/FStar_Monotonic_HyperHeap.krml extracted/FStar_Monotonic_HyperStack.krml extracted/FStar_HyperStack.krml extracted/FStar_Monotonic_Witnessed.krml extracted/FStar_HyperStack_ST.krml extracted/FStar_HyperStack_All.krml extracted/FStar_Date.krml extracted/FStar_Universe.krml extracted/FStar_GSet.krml extracted/FStar_ModifiesGen.krml extracted/LowStar_Monotonic_Buffer.krml extracted/LowStar_Buffer.krml extracted/Spec_Loops.krml extracted/LowStar_BufferOps.krml extracted/C_Loops.krml extracted/FStar_UInt8.krml extracted/FStar_Kremlin_Endianness.krml extracted/FStar_UInt63.krml extracted/FStar_Exn.krml extracted/FStar_ST.krml extracted/FStar_All.krml extracted/FStar_Dyn.krml extracted/FStar_Int63.krml extracted/FStar_Int64.krml extracted/FStar_Int32.krml extracted/FStar_Int8.krml extracted/FStar_UInt16.krml extracted/FStar_Int_Cast.krml extracted/FStar_UInt128.krml extracted/C_Endianness.krml extracted/FStar_List.krml extracted/FStar_Float.krml extracted/FStar_IO.krml extracted/C.krml extracted/FStar_Char.krml extracted/FStar_String.krml extracted/LowStar_Modifies.krml extracted/C_String.krml extracted/FStar_Bytes.krml extracted/FStar_HyperStack_IO.krml extracted/C_Failure.krml extracted/TestLib.krml extracted/FStar_Int_Cast_Full.krml
 * F* version: 059db0c8
 * KreMLin version: 916c37ac
 */



#ifndef __FStar_UInt128_H
#define __FStar_UInt128_H


#include <inttypes.h>
#include <stdbool.h>
#include "kremlin/internal/types.h"

uint64_t FStar_UInt128___proj__Mkuint128__item__low(FStar_UInt128_uint128 projectee);

uint64_t FStar_UInt128___proj__Mkuint128__item__high(FStar_UInt128_uint128 projectee);

typedef FStar_UInt128_uint128 FStar_UInt128_t;

FStar_UInt128_uint128 FStar_UInt128_add(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128
FStar_UInt128_add_underspec(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_add_mod(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_sub(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128
FStar_UInt128_sub_underspec(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_sub_mod(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_logand(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_logxor(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_logor(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_lognot(FStar_UInt128_uint128 a);

FStar_UInt128_uint128 FStar_UInt128_shift_left(FStar_UInt128_uint128 a, uint32_t s);

FStar_UInt128_uint128 FStar_UInt128_shift_right(FStar_UInt128_uint128 a, uint32_t s);

bool FStar_UInt128_eq(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

bool FStar_UInt128_gt(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

bool FStar_UInt128_lt(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

bool FStar_UInt128_gte(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

bool FStar_UInt128_lte(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_eq_mask(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_gte_mask(FStar_UInt128_uint128 a, FStar_UInt128_uint128 b);

FStar_UInt128_uint128 FStar_UInt128_uint64_to_uint128(uint64_t a);

uint64_t FStar_UInt128_uint128_to_uint64(FStar_UInt128_uint128 a);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Plus_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Plus_Question_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Plus_Percent_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Subtraction_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Subtraction_Question_Hat)(
  FStar_UInt128_uint128 x0,
  FStar_UInt128_uint128 x1
);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Subtraction_Percent_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Amp_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Hat_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Bar_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Less_Less_Hat)(FStar_UInt128_uint128 x0, uint32_t x1);

extern FStar_UInt128_uint128
(*FStar_UInt128_op_Greater_Greater_Hat)(FStar_UInt128_uint128 x0, uint32_t x1);

extern bool (*FStar_UInt128_op_Equals_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern bool
(*FStar_UInt128_op_Greater_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern bool (*FStar_UInt128_op_Less_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern bool
(*FStar_UInt128_op_Greater_Equals_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

extern bool
(*FStar_UInt128_op_Less_Equals_Hat)(FStar_UInt128_uint128 x0, FStar_UInt128_uint128 x1);

FStar_UInt128_uint128 FStar_UInt128_mul32(uint64_t x, uint32_t y);

FStar_UInt128_uint128 FStar_UInt128_mul_wide(uint64_t x, uint64_t y);

#define __FStar_UInt128_H_DEFINED
#endif
