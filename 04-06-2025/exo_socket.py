import socket 

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(("example.com", 80)) 
s.sendall(b"GET / HTTP/1.1\r\nHost: example.comr\r\n\r\n") 

#Recevoir et afficher La réponse du serveur
response = s.recv(1024) 
print("sortie bruten\n", response),

#Afficher La réponse formatée 
print("\nInsortie formatéen") 
print(response.decode("utf-8"))

s.close()