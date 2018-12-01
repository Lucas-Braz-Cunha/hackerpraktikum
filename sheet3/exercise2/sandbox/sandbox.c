#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <fcntl.h>
#include <unistd.h>


/* Function pointers to hold the value of the glibc functions */
static  ssize_t (*real_write)(int fd, const void *buf, size_t count) = NULL;
static  ssize_t (*real_read) (int fildes, void *buf, size_t nbyte) = NULL;

#define PATH_TO_BLACKLIST "/home/lucas/fau/hacker/sheet3/exercise2/sandbox/blacklist.txt"

/*
  Check for file name (with full path) in the blacklist file.
  Return:
  > 0: File is in the blacklist.
  = 0: File is not in the blacklist.
  < 0: Couldn't find find path.
*/
int check_blacklist(int fd){
  FILE *fp = fopen(PATH_TO_BLACKLIST, "r");;
  char filePath[PATH_MAX];
  char filePath_blacklist[PATH_MAX];
  int isValid = 0;
  char path_to_fd[PATH_MAX];
  sprintf(path_to_fd, "/proc/self/fd/%d", fd);


  if (readlink(path_to_fd, filePath, sizeof(filePath)) > 0)
  {
      printf("Checking if file is present in the blacklist:\n%s\n", filePath);
      //read from blacklist and see if the file is there.
      while(fgets(filePath_blacklist, PATH_MAX, fp) != NULL && !isValid){
        // printf("File from blacklist:\n%s\n", filePath_blacklist);
        if(!strncmp(filePath_blacklist, filePath, strlen(filePath))){
          isValid = 1;
        }
      }
  }else{
      //Couldn't find the file name.
      fprintf(stderr, "Error while finding file name\n");
      return -1;
  }
  fclose(fp);
  return isValid;
}

/* wrapping write function call */
ssize_t write(int fd, const void *buf, size_t count){
    printf("Wrapping function executed to check if file is accessable\n");
    /* Checking if file is okay */
    if(check_blacklist(fd) ==  0){
      /* resolve the real write function from glibc
      * and pass the arguments.
      */
      real_write = dlsym(RTLD_NEXT, "write");
      return real_write(fd, buf, count);
    }
    else{
      fprintf(stderr, "You have no access to the file\n");
      return 0;
    }
}

/* wrapping read function call */
ssize_t read(int fd, void *buf, size_t nbyte){
  printf("Wrapping function executed to check if file is accessable\n");
  /* Checking if file is okay */
  if(check_blacklist(fd) ==  0){
    /* resolve the real write function from glibc
    * and pass the arguments.
    */
    real_read = dlsym(RTLD_NEXT, "read");
    return real_read(fd, buf, nbyte);
  }
  else{
    fprintf(stderr, "You have no access to the file\n");
    return 0;
  }

}
