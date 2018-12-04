KDIR := /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

obj-m := harmless_module.o

all:
	make -C $(KDIR) M=$(PWD) modules
clean:
	make -C $(KDIR) M=$(PWD) clean

test:
	# We put a — in front of the rmmod command to tell make to ignore
  # an error in case the module isn’t loaded.
	-sudo rmmod harmless_module
  # Clear the kernel log without echo
	sudo dmesg -C
  # Insert the module
	sudo insmod harmless_module.ko
  # Display the kernel log
	dmesg
