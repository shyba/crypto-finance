package xts

import "golang.org/x/crypto/xts"
import "crypto/aes"
import "crypto/rand"
import "fmt"
import "errors"

type XTSDevice struct {
	key            []byte
	sectorSize     uint64
	sectorTotal    uint64
	lastUsedSector uint64
	cipher         *xts.Cipher
}

//Creates a new XTS Device
//All values can be nil or 0, they will be initialized to:
//key := a random new one
//sectorSize := 16 (need a multiple of 16)
//sectorTotal := 3 (at least 3 blocks are needed for this ciphertext stealing implementation)
func NewDevice(key []byte, sectorSize uint64, sectorTotal uint64) (x *XTSDevice, err error) {
	if key == nil {
		key := make([]byte, 32)
		_, err := rand.Read(key)
		if err != nil {
			return nil, err
		}
	} else {
		if len(key) != 32 && len(key) != 64 {
			err := errors.New(fmt.Sprintf("Key is expected to have length 32 or 64, got %d", len(key)))
			return nil, err
		}
	}
	if sectorSize == 0 {
		sectorSize = 16
	} else if sectorSize%16 != 0 {
		return nil, errors.New(fmt.Sprintf("Sector size is expected to be a multiple of 16, got %d", sectorSize))
	}

	if sectorSize < 3 {
		sectorSize = 3
	}

	x = &XTSDevice{
		key:            key,
		sectorSize:     sectorSize,
		sectorTotal:    sectorTotal,
		lastUsedSector: 0,
	}
	if x.cipher, err = xts.NewCipher(aes.NewCipher, key); err != nil {
		return nil, err
	}
	return x, nil
}

//For now, plaintext length needs to be equal to sector size
func (x *XTSDevice) Encrypt(plaintext []byte, sector uint64) (ciphertext []byte, err error) {
	if plaintext == nil || sector < 0 {
		return nil, errors.New("Invalid parameters. Plaintext can't be nil and sector can't be less than 0")
	}
	ciphertext = make([]byte, x.sectorSize)
	x.cipher.Encrypt(ciphertext, plaintext, sector)
	return ciphertext, nil
}

//For now, ciphertext length needs to be equal to sector size
func (x *XTSDevice) Decrypt(ciphertext []byte, sector uint64) (plaintext []byte, err error) {
	if ciphertext == nil || sector < 0 {
		return nil, errors.New("Invalid parameters. Ciphertext can't be nil and sector can't be less than 0")
	}
	plaintext = make([]byte, x.sectorSize)
	x.cipher.Decrypt(plaintext, ciphertext, sector)
	return plaintext, nil
}

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
