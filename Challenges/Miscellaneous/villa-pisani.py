import socket
import dns.resolver

resolver = dns.resolver.Resolver()
resolver.nameservers = [socket.gethostbyname("pisani.challs.olicyber.it")]
resolver.port = 10500

directions = ["up.", "right.", "down.", "left."]
visited = set()

def dir(curr_domain):
    if curr_domain in visited:
        return
    visited.add(curr_domain)
    
    print(f"Trying: {curr_domain} ", end="")

    for i in directions:
        try:
            answer = resolver.resolve(i + curr_domain, "CNAME")
        except Exception:
            continue
        
        next_room = answer[0].to_text()
        try:
            check = resolver.resolve(i + curr_domain, "TXT")[0].to_text()
            found = True
        except:
            found = False

        if found and "flag" in check:
            print(f"\nFound: {check}")
            exit(0)

        dir(next_room)

dir("00000000-0000-4000-0000-000000000000.maze.localhost.")