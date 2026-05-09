/* Auto-generated linker script fragment for LLEXT
 * Separates .rodata sections based on relocation status
 */

SECTIONS
{
    /* Read-only data WITH relocations - will be copied to RAM by LLEXT */
    .rodata : {
        *(.rodata._ZL12arduino_pins)
        *(.rodata._ZTV13BridgeMonitorILj512EE)
        *(.rodata._ZTV14ModulinoBuzzer)
        *(.rodata._ZTV14ModulinoPixels)
        *(.rodata._ZTV15SerialTransport)
        *(.rodata._ZTV16ModulinoDistance)
        *(.rodata._ZTV8VL53L4CD)
        *(.rodata._ZTV8VL53L4ED)
        *(.rodata._ZTVN7arduino12ZephyrSerialE)
        *(.rodata._ZTVN7arduino9ZephyrI2CE)
        *(.rodata._ZTVN7arduino9ZephyrSPIE)
    }

    /* Read-only data WITHOUT relocations - kept in flash by LLEXT */
    .llext.rodata.noreloc : {
        *(.rodata)
        *(.rodata._GLOBAL__sub_I_distance.str1.1)
        *(.rodata._Z11getDistancev.str1.1)
        *(.rodata._ZL30VL53L4CD_DEFAULT_CONFIGURATION)
        *(.rodata._ZL30VL53L4ED_DEFAULT_CONFIGURATION)
        *(.rodata._ZN10RpcDecoderILj1024EE12get_responseIN7arduino7msgpack6object5nil_tEEEbjRT_R8RpcError.str1.1)
        *(.rodata._ZN10RpcDecoderILj1024EE12get_responseIbEEbjRT_R8RpcError.str1.1)
        *(.rodata._ZN11BridgeClass11update_safeEv.str1.1)
        *(.rodata._ZN11BridgeClass5beginEm.str1.1)
        *(.rodata._ZN13BridgeMonitorILj512EE5_readEj.str1.1)
        *(.rodata._ZN13BridgeMonitorILj512EE5beginEmt.isra.0.str1.1)
        *(.rodata._ZN13BridgeMonitorILj512EE5writeEPKhj.str1.1)
        *(.rodata._ZN7RpcCallIJEE6resultIbEEbRT_.part.0.str1.1)
        *(.rodata._ZN7RpcCallIJEEC2ERKN7arduino6StringEP9RPCClientP7k_mutexS8_.str1.1)
        *(.rodata._ZN7arduino5Print7printlnEv.str1.1)
        *(.rodata._ZN7arduino7msgpack6object3extC2EaPKhj.str1.1)
        *(.rodata._ZN8RpcErrorC2Ev.str1.1)
        *(.rodata._ZNSt6vectorIjSaIjEE17_M_realloc_insertIJRjEEEvN9__gnu_cxx17__normal_iteratorIPjS1_EEDpOT_.str1.1)
        *(.rodata.str1.1)
    }

    /* Merge all .rel.rodata.* sections into .rel.rodata */
    .rel.rodata : {
        *(.rel.rodata)
        *(.rel.rodata.*)
    }

    /* Merge all .rela.rodata.* sections into .rela.rodata */
    .rela.rodata : {
        *(.rela.rodata)
        *(.rela.rodata.*)
    }

}
