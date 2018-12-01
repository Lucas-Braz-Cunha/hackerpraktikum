#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <string.h>


int main(){

  FILE *fp;
  int fd;
  char buff[255];
  size_t nbytes;
  ssize_t bytes_read;
  printf("Using Read/Write test....\n");
  /* Using open and read functions */
  // I had some problems when trying to open for READ/WRITE, so I'm doing each once.

  // Test for writing
  fd = open("/home/lucas/fau/hacker/sheet3/exercise2/test_program/blocked_file.txt", O_WRONLY | O_APPEND);
  if(!fd){
    printf("Failed to open file...\n");
  }
  char *text = "Hello, File!\n";
  printf("Trying to write() to file: function returned %d\n",write(fd, text, strlen(text)));
  close(fd);

  // Test for reading
  fd = open("/home/lucas/fau/hacker/sheet3/exercise2/test_program/blocked_file.txt", O_RDONLY);
  if(!fd){
    printf("Failed to open file...\n");
  }
  nbytes = sizeof(buff);
  bytes_read = read(fd, buff, nbytes - 1);
  //Making sure the "string" has the end marker.
  buff[bytes_read] = '\0';
  printf("Number of bytes read:%d\ntext:%s\n", bytes_read);
  close(fd);

  return 0;
}
