ENTRY(Reset_Handler)
__ram_vector_table__ = 1;
__stack_size__ = 0x400;
__heap_size__ = 0x6000;
HEAP_SIZE = DEFINED(__heap_size__) ? __heap_size__ : 0x0400;
STACK_SIZE = DEFINED(__stack_size__) ? __stack_size__ : 0x0400;
M_VECTOR_RAM_SIZE = DEFINED(__ram_vector_table__) ? 0x0400 : 0x0;
MEMORY
{
  m_interrupts (RX) : ORIGIN = 0, LENGTH = 0x400
  m_flash_config (RX) : ORIGIN = 0 + 0x400, LENGTH = 0x10
  m_text (RX) : ORIGIN = 0 + 0x410, LENGTH = 0x100000 - 0x410
  m_data (RW) : ORIGIN = 0x1FFF0000, LENGTH = 0x00010000
  m_data_2 (RW) : ORIGIN = 0x20000000, LENGTH = 0x00030000
}
SECTIONS
{
  .interrupts :
  {
    __VECTOR_TABLE = .;
    . = ALIGN(4);
    KEEP(*(.isr_vector))
    . = ALIGN(4);
  } > m_interrupts
  .flash_config :
  {
    . = ALIGN(4);
    KEEP(*(.FlashConfig))
    . = ALIGN(4);
  } > m_flash_config
  __UVISOR_FLASH_OFFSET = 0x410;
  __UVISOR_FLASH_START = ORIGIN(m_interrupts) + __UVISOR_FLASH_OFFSET;
  .text __UVISOR_FLASH_START :
  {
    . = ALIGN(4);
    __uvisor_main_start = .;
    *(.uvisor.main)
    __uvisor_main_end = .;
    . = ALIGN(4);
    *(.text)
    *(.text*)
    *(.rodata)
    *(.rodata*)
    *(.glue_7)
    *(.glue_7t)
    *(.eh_frame)
    KEEP (*(.init))
    KEEP (*(.fini))
    . = ALIGN(4);
  } > m_text
  .ARM.extab :
  {
    *(.ARM.extab* .gnu.linkonce.armextab.*)
  } > m_text
  .ARM :
  {
    __exidx_start = .;
    *(.ARM.exidx*)
    __exidx_end = .;
  } > m_text
 .ctors :
  {
    __CTOR_LIST__ = .;
    KEEP (*crtbegin.o(.ctors))
    KEEP (*crtbegin?.o(.ctors))
    KEEP (*(EXCLUDE_FILE(*crtend?.o *crtend.o) .ctors))
    KEEP (*(SORT(.ctors.*)))
    KEEP (*(.ctors))
    __CTOR_END__ = .;
  } > m_text
  .dtors :
  {
    __DTOR_LIST__ = .;
    KEEP (*crtbegin.o(.dtors))
    KEEP (*crtbegin?.o(.dtors))
    KEEP (*(EXCLUDE_FILE(*crtend?.o *crtend.o) .dtors))
    KEEP (*(SORT(.dtors.*)))
    KEEP (*(.dtors))
    __DTOR_END__ = .;
  } > m_text
  .preinit_array :
  {
    PROVIDE_HIDDEN (__preinit_array_start = .);
    KEEP (*(.preinit_array*))
    PROVIDE_HIDDEN (__preinit_array_end = .);
  } > m_text
  .init_array :
  {
    PROVIDE_HIDDEN (__init_array_start = .);
    KEEP (*(SORT(.init_array.*)))
    KEEP (*(.init_array*))
    PROVIDE_HIDDEN (__init_array_end = .);
  } > m_text
  .fini_array :
  {
    PROVIDE_HIDDEN (__fini_array_start = .);
    KEEP (*(SORT(.fini_array.*)))
    KEEP (*(.fini_array*))
    PROVIDE_HIDDEN (__fini_array_end = .);
  } > m_text
  .interrupts_ram :
  {
    . = ALIGN(4);
    __VECTOR_RAM__ = .;
    __interrupts_ram_start__ = .;
    *(.m_interrupts_ram)
    . += M_VECTOR_RAM_SIZE;
    . = ALIGN(4);
    __interrupts_ram_end__ = .;
  } > m_data
  __UVISOR_SRAM_OFFSET = 0x400;
  __UVISOR_SRAM_START = ORIGIN(m_data) + __UVISOR_SRAM_OFFSET;
  .uvisor.bss __UVISOR_SRAM_START (NOLOAD):
  {
    . = ALIGN(32);
    __uvisor_bss_start = .;
    . = ALIGN(32);
    __uvisor_bss_main_start = .;
    KEEP(*(.keep.uvisor.bss.main))
    . = ALIGN(32);
    __uvisor_bss_main_end = .;
    . = ALIGN(32);
    __uvisor_bss_boxes_start = .;
    KEEP(*(.keep.uvisor.bss.boxes))
    . = ALIGN(32);
    __uvisor_bss_boxes_end = .;
    . = ALIGN(32);
    __uvisor_bss_end = .;
  } > m_data
  .page_heap (NOLOAD) :
  {
    . = ALIGN(32);
    __uvisor_page_start = .;
    KEEP(*(.keep.uvisor.page_heap))
    . = ALIGN(32);
    __uvisor_page_end = .;
  } > m_data_2
  __VECTOR_RAM = DEFINED(__ram_vector_table__) ? __VECTOR_RAM__ : ORIGIN(m_interrupts);
  __RAM_VECTOR_TABLE_SIZE_BYTES = DEFINED(__ram_vector_table__) ? (__interrupts_ram_end__ - __interrupts_ram_start__) : 0x0;
  .data :
  {
    PROVIDE(__etext = LOADADDR(.data));
    PROVIDE(__DATA_ROM = LOADADDR(.data));
    . = ALIGN(4);
    __DATA_RAM = .;
    __data_start__ = .;
    *(.data)
    *(.data*)
    KEEP(*(.jcr*))
    . = ALIGN(4);
    __data_end__ = .;
  } > m_data_2 AT > m_text
  __DATA_END = __DATA_ROM + (__data_end__ - __data_start__);
  text_end = ORIGIN(m_text) + LENGTH(m_text);
  ASSERT(__DATA_END <= text_end, "region m_text overflowed with text and data")
  .uvisor.secure :
  {
    . = ALIGN(32);
    __uvisor_secure_start = .;
    . = ALIGN(32);
    __uvisor_cfgtbl_start = .;
    KEEP(*(.keep.uvisor.cfgtbl))
    . = ALIGN(32);
    __uvisor_cfgtbl_end = .;
    __uvisor_cfgtbl_ptr_start = .;
    KEEP(*(.keep.uvisor.cfgtbl_ptr_first))
    KEEP(*(.keep.uvisor.cfgtbl_ptr))
    __uvisor_cfgtbl_ptr_end = .;
    __uvisor_register_gateway_ptr_start = .;
    KEEP(*(.keep.uvisor.register_gateway_ptr))
    __uvisor_register_gateway_ptr_end = .;
    . = ALIGN(32);
    __uvisor_secure_end = .;
  } > m_text
  .uninitialized (NOLOAD):
  {
    . = ALIGN(32);
    __uninitialized_start = .;
    *(.uninitialized)
    KEEP(*(.keep.uninitialized))
    . = ALIGN(32);
    __uninitialized_end = .;
  } > m_data_2
  USB_RAM_GAP = DEFINED(__usb_ram_size__) ? __usb_ram_size__ : 0x800;
  .bss :
  {
    . = ALIGN(4);
    __START_BSS = .;
    __bss_start__ = .;
    *(.bss)
    *(.bss*)
    . = ALIGN(512);
    USB_RAM_START = .;
    . += USB_RAM_GAP;
    *(COMMON)
    . = ALIGN(4);
    __bss_end__ = .;
    __END_BSS = .;
  } > m_data_2
  .heap :
  {
    . = ALIGN(8);
    __uvisor_heap_start = .;
    __end__ = .;
    PROVIDE(end = .);
    __HeapBase = .;
    . += HEAP_SIZE;
    __HeapLimit = .;
    __heap_limit = .;
    __uvisor_heap_end = .;
  } > m_data_2
  m_usb_bdt USB_RAM_START (NOLOAD) :
  {
    *(m_usb_bdt)
    USB_RAM_BDT_END = .;
  }
  m_usb_global USB_RAM_BDT_END (NOLOAD) :
  {
    *(m_usb_global)
  }
  __StackTop = ORIGIN(m_data_2) + LENGTH(m_data_2);
  __StackLimit = __StackTop - STACK_SIZE;
  PROVIDE(__stack = __StackTop);
  .ARM.attributes 0 : { *(.ARM.attributes) }
  ASSERT(__StackLimit >= __HeapLimit, "Region m_data_2 overflowed with stack and heap")
  __uvisor_flash_start = ORIGIN(m_interrupts);
  __uvisor_flash_end = ORIGIN(m_text) + LENGTH(m_text);
  __uvisor_sram_start = ORIGIN(m_data);
  __uvisor_sram_end = ORIGIN(m_data_2) + LENGTH(m_data_2);
  __uvisor_public_sram_start = __uvisor_sram_start;
  __uvisor_public_sram_end = __uvisor_sram_end;
}
