package main

import "golang.org/x/crypto/xts"
import "crypto/aes"
import "crypto/rand"
import "fmt"

func main() {
	//Learning how to use and checking implementation
	key := make([]byte, 32)
	rand.Read(key)
	c, err := xts.NewCipher(aes.NewCipher, key)

	if err != nil {
		fmt.Printf("#failed to create cipher: %s", err)
		return
	}

	msg := make([]byte, 16)
	ciphertext := make([]byte, 160)
	for i := 0; i < 9; i++ {
		rand.Read(msg)
		fmt.Printf("message %d\n", i)
		fmt.Println(msg)
		c.Encrypt(ciphertext[i*16:(i*16+16)], msg, uint64(i))
		fmt.Println("ciphertext")
		fmt.Println(ciphertext)
	}

	decrypted := make([]byte, len(msg))
	for i := 0; i < 10; i++ {
		c.Decrypt(decrypted, ciphertext[i*16:(i*16+16)], uint64(i))
		fmt.Printf("message %d\n", i)
		fmt.Println(decrypted)
	}

}
