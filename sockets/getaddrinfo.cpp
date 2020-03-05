#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <arpa/inet.h>

/**
 * Example using getaddrinfo() to fetch the IP for www.google.com
 * Modified from https://beej.us/guide/bgnet/examples/showip.c
 */
int main() {
    int status;
    struct addrinfo hints;
    struct addrinfo *servinfo;  // will point to the results

    memset(&hints, 0, sizeof hints); // make sure the struct is empty
    hints.ai_family = AF_INET6;      // IPv6
    hints.ai_socktype = SOCK_STREAM; // TCP stream sockets
    hints.ai_flags = AI_PASSIVE;     // fill in my IP for me

    if ((status = getaddrinfo("www.google.com", "https", &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(status));
        exit(1);
    }

    struct sockaddr_in6 *ipv6 = (struct sockaddr_in6 *)servinfo->ai_addr;
    void *addr = &(ipv6->sin6_addr);
    char ipstr[INET6_ADDRSTRLEN];

    inet_ntop(servinfo->ai_family, addr, ipstr, sizeof ipstr);
    printf("IP: %s\n", ipstr);

    freeaddrinfo(servinfo);
    return 0;
}